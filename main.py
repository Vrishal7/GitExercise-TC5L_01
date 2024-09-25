import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk, ImageFilter
import io
import random
from io import BytesIO
import os
import pygame
from tkinter import simpledialog

class KidsDrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kids Drawing App")

        # Bind the close event to warn the user about unsaved progress
        self.root.protocol("WM_DELETE_WINDOW", self.save_warning)

        # Canvas dimensions
        self.canvas_width = 680
        self.canvas_height = 800

        # Coin system
        self.coins = 0

        # Timer variables
        self.timer_duration = 30 * 60  # Default to 30 minutes (in seconds)
        self.time_left = self.timer_duration
        self.timer_running = False
        self.timer = "30:00"

        # Create canvas
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack(side=tk.LEFT)

        # Variables to store previous position
        self.last_x, self.last_y = None, None

        # Draw Variables
        self.color = 'black'
        self.brush_size = 5
        self.eraser_size = 10  # Default eraser size
        self.drawing = False
        self.eraser_mode = False  # Initialize eraser mode
        self.previous_x = None
        self.previous_y = None
        self.mode = 'brush'  # Track mode: 'brush' or 'text' 

        self.text_items = {}  # Dictionary to hold text IDs
        self.last_text_id = None  # Keep track of the last text ID for editing

        # Create image and draw objects
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

        # History stack for undo and redo
        self.undo_stack = []
        self.redo_stack = []

        # Directory for assets
        self.assets_directory = 'Assets'  # Update to your 'Assets' folder

        # Buttons and Options
        self.create_widgets()

        # Bind mouse events to the canvas
        self.canvas.bind("<ButtonPress-1>", self.start_drawing)    # Start drawing when mouse button is pressed
        self.canvas.bind("<B1-Motion>", self.draw_on_canvas)       # Draw while the mouse is moving (drag)
        self.canvas.bind("<ButtonRelease-1>", self.finalize_shape) # Finalize shape when the mouse button is released

        # Bind keyboard event to the root window
        self.root.bind("<e>", self.edit_text)  # Bind the "E" key for editing text


        # Track completed pages
        self.completed_pages = {"Level 1 - Easy": [False] * 6,
                                "Level 2 - Normal":[False]*6,
                                "Level 3 - Hard": [False]*6,
                                "Level 4 - Insane": [False]*6,
                                "Level 5 - Impossible":[False]*6} 
        
        #initialize complete buttons
        self.complete_buttons={}
        
        # initialize pygame mixer
        pygame.mixer.init()
        
    def create_widgets(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Load and resize the coin icon using PIL (make sure to use the correct file path)
        coin_img = Image.open("coin_icon2.jpg").resize((30, 25), Image.Resampling.LANCZOS)
        self.coin_icon = ImageTk.PhotoImage(coin_img)

        # Create a label to display coins with the icon
        self.coins_label = tk.Label(toolbar, image=self.coin_icon, text=f"Coins: {self.coins}", compound=tk.LEFT, font=("Arial", 14))
        self.coins_label.pack(side=tk.TOP, padx=1)

        # Open Folder Button
        gallery_button = tk.Button(toolbar, text="Open Folder", command=self.open_gallery)
        gallery_button.pack(side=tk.LEFT, padx=1)

        # Load and resize the timer icon using PIL
        timer_img = Image.open("timer_icon.png").resize((20, 20), Image.LANCZOS)
        self.timer_icon = ImageTk.PhotoImage(timer_img)

        # Create a timer label with the icon
        self.timer_label = tk.Label(toolbar, image=self.timer_icon, text=f"Timer: {self.timer}", compound=tk.LEFT, font=("Arial", 14))
        self.timer_label.pack(side=tk.TOP, padx=1)

        # Button to set custom time
        self.set_time_button = tk.Button(toolbar, text="Set Timer", command=self.set_custom_timer)
        self.set_time_button.pack(side=tk.LEFT, padx=1)

        # Brush Size Slider
        size_slider = tk.Scale(toolbar, from_=1, to=10, orient=tk.HORIZONTAL, label="Brush Size")
        size_slider.set(self.brush_size)
        size_slider.pack(side=tk.LEFT, padx=1)
        size_slider.bind("<Motion>", self.change_brush_size)

        # Color Button
        color_img = Image.open("choosecolor_icon.png").resize((20, 20), Image.LANCZOS)  # Load and resize the color icon
        self.color_icon = ImageTk.PhotoImage(color_img)  # Create PhotoImage object

        color_button = tk.Button(toolbar, image=self.color_icon, command=self.choose_color)  # Create the button with the icon
        color_button.pack(side=tk.LEFT, padx=1)  # Pack the button in the toolbar

        # Shape Buttons
        circle_button = tk.Button(toolbar, text="Circle", command=lambda: self.select_shape('circle'))
        circle_button.pack(side=tk.LEFT, padx=1)

        rectangle_button = tk.Button(toolbar, text="Rectangle", command=lambda: self.select_shape('rectangle'))
        rectangle_button.pack(side=tk.LEFT, padx=1)

        line_button = tk.Button(toolbar, text="Line", command=lambda: self.select_shape('line'))
        line_button.pack(side=tk.LEFT, padx=1)

        # Load and resize the eraser icon using PIL (with the correct resampling method)
        eraser_img = Image.open("eraser_icon.png").resize((20, 20), Image.Resampling.LANCZOS)
        self.eraser_icon = ImageTk.PhotoImage(eraser_img)

        # Create the Eraser button with the icon
        self.eraser_button = tk.Button(toolbar, image=self.eraser_icon, command=self.toggle_eraser)
        self.eraser_button.pack(side=tk.LEFT, padx=1)

        # Save Button
        save_img = Image.open("save_icon.png").resize((20, 20), Image.LANCZOS)  # Load and resize the save icon
        self.save_icon = ImageTk.PhotoImage(save_img)  # Create PhotoImage object

        save_button = tk.Button(toolbar, image=self.save_icon, command=self.save_drawing)  # Create the button with the icon
        save_button.pack(side=tk.LEFT, padx=1)  # Pack the button in the toolbar

        # Clear Button
        clear_button = tk.Button(toolbar, text="Clear", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT, padx=1)

        # Undo Button
        undo_img = Image.open("undo_icon.png").resize((20, 20), Image.LANCZOS)  # Load and resize the undo icon
        self.undo_icon = ImageTk.PhotoImage(undo_img)  # Create PhotoImage object

        undo_button = tk.Button(toolbar, image=self.undo_icon, command=self.undo)  # Create the button with the icon
        undo_button.pack(side=tk.LEFT, padx=1)  # Pack the button in the toolbar

        # Brush Button
        brush_img = Image.open("brush_icon2.png").resize((20, 20), Image.LANCZOS)  # Load and resize the brush icon
        self.brush_icon = ImageTk.PhotoImage(brush_img)  # Create PhotoImage object

        brush_button = tk.Button(toolbar, image=self.brush_icon, command=lambda: self.set_shape_mode(None))  # Create the button with the icon
        brush_button.pack(side=tk.LEFT, padx=1)  # Pack the button in the toolbar

        brush_button = tk.Button(root, text="Brush Mode", command=self.activate_brush_mode)  # Create the button with the icon
        brush_button.pack(side=tk.LEFT, padx=1)  # Pack the button in the toolbar

        # Text Mode Button
        text_img = Image.open("text_icon.png").resize((20, 20), Image.LANCZOS)  # Load and resize the text icon
        self.text_icon = ImageTk.PhotoImage(text_img)  # Create PhotoImage object

        self.text_button = tk.Button(root, image=self.text_icon, command=self.activate_text_mode)  # Create the button with the icon
        self.text_button.pack(side=tk.LEFT, padx=1)  # Pack the button in the toolbar

        # Music Button
        music_img=Image.open("music.png").resize((20,20), Image.LANCZOS)
        self.music_icon=ImageTk.PhotoImage(music_img)

        music_button=tk.Button(toolbar,image=self.music_icon,command=self.play_music)
        music_button.pack(side=tk.LEFT,padx=1)

        # Theme Button
        theme_img= Image.open("mode.png").resize((20,20), Image.LANCZOS)
        self.theme_icon=ImageTk.PhotoImage(theme_img)

        theme_button=tk.Menubutton(toolbar,image=self.theme_icon)
        theme_button.pack(side=tk.LEFT,padx=1)

        theme_menu=tk.Menu(theme_button,tearoff=0)
        theme_menu.add_command(label="Light Mode",command=self.light_mode)
        theme_menu.add_command(label="Dark Mode",command=self.dark_mode)

        theme_button.config(menu=theme_menu)

        # Blank Page Button
        blank_page_button = tk.Button(toolbar, text="Blank Page", command=self.blank_page)
        blank_page_button.pack(side=tk.LEFT)

        # Button to set custom time
        self.set_time_button = tk.Button(toolbar, text="Set Timer", command=self.set_custom_timer)
        self.set_time_button.pack(side=tk.LEFT, padx=1)
        
        # Background Button
        bg_button = tk.Button(root, text="Change Background", command=self.change_background)
        bg_button.pack(side=tk.LEFT, padx=1)

        # Mini Picture Section
        right_frame = tk.Frame(self.root, bd=2, relief=tk.RAISED)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.mini_pics_frame = tk.Frame(right_frame)
        self.mini_pics_frame.pack(side=tk.TOP, fill=tk.X)

        self.selected_frame = tk.Frame(right_frame)
        self.selected_frame.pack(side=tk.BOTTOM, fill=tk.X) #Make outline images

        self.load_mini_pictures()

    def save_state(self):
        """ Save the current state of the image to the undo stack """
        state = io.BytesIO()
        self.image.save(state, format="PNG")
        self.undo_stack.append(state.getvalue())
        self.redo_stack.clear()  # Clear redo stack on new action

    def select_shape(self, shape):
        """ Select the shape tool to draw """
        self.shape_mode = shape  # Set the shape mode
        self.drawing = False  # Disable drawing mode when selecting shape

    def play_music(self):
        self.music_window=tk.Toplevel(self.root)   
        self.music_window.title("Music Options")

        music_options=["music 1.mp3","music 2.mp3","music 3.mp3", "music 4.mp3"]
        self.music_var=tk.StringVar(self.music_window)
        self.music_var.set(music_options[0])

        music_menu=tk.OptionMenu(self.music_window,self.music_var,*music_options)
        music_menu.pack()

        play_button=tk.Button(self.music_window,text="Play",command=self.start_music)
        play_button.pack()

        pause_button=tk.Button(self.music_window,text="Pause",command=self.pause_music)
        pause_button.pack() 

        resume_button=tk.Button(self.music_window,text="Resume",command=self.resume_music)
        resume_button.pack()

        stop_button=tk.Button(self.music_window,text="Stop",command=self.stop_music)
        stop_button.pack()

    def start_music(self):
        music_file = self.music_var.get()
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)  # -1 to loop the music

    def pause_music(self):
        pygame.mixer.music.pause()

    def resume_music(self):
        pygame.mixer.music.unpause()

    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_window.destroy()

    def light_mode(self):
        self.root.config(bg="#f0f0f0")
        for widget in self.root.winfo_children():
            if isinstance(widget,tk.Frame):
                widget.config(bg="#f0f0f0")
            elif isinstance(widget,tk.Label):
                widget.config(bg="#f0f0f0",fg="black")
            elif isinstance(widget,tk.Button):
                widget.config(bg="#f0f0f0",fg="black")
            elif isinstance(widget,tk.Menubutton):
                widget.config(bg="#f0f0f0",fg="black")
            elif isinstance(widget,tk.Scale):
                widget.config(bg="#f0f0f0",fg="black",throughcolor="#f0f0f0")   

        self.coins_label.config(bg="#f0f0f0",fg="black") 
        self.timer_label.config (bg="#f0f0f0",fg="black")

        #update the colours in mini it frames
        self.mini_pics_frame.config(bg="#f0f0f0")
        for widget in self.mini_pics_frame.winfo_children():
            widget.config(bg="#f0f0f0")
            for child in widget.winfo_children():
                child.config(bg="#f0f0f0")
                for grandchild in child.winfo_children():
                    grandchild.config(bg="#f0f0f0")       

       #update colours of selected frames
        self.selected_frame.config(bg="#white")
        for widget in self.selected_frame.winfo_children():
            widget.config(bg="f0f0f0")

            #canvas colour
        self.canvas.config(bg="white")    
        
    def dark_mode(self):
        self.root.config(bg="black")
        for widget in self.root.winfo_children():
            if isinstance(widget,tk.Frame):
                widget.config(bg="black")
            elif isinstance(widget,tk.Label):
                widget.config(bg="black",fg="white")
        self.coins_label.config(bg="black",fg="white")
        self.timer_label.config(bg="black",fg="white")            
                
      
    def place_text(self, event, text):
        x, y = event.x, event.y
        font_size = 20
        font = ("Arial", font_size)

        # Draw the text on the canvas
        self.last_text_id = self.canvas.create_text(x, y, text=text, font=font, fill=self.color)

        # Also draw the text on the image to ensure it's saved
        self.draw.text((x, y), text, font=None, fill=self.color)

        # Unbind the click event after placing the text (Text mode ends)
        self.canvas.unbind("<Button-1>")

        # Rebind the brush tool (Enable brush mode again)
        self.bind_brush()

    def edit_text(self, event):
        if self.last_text_id is not None:
            current_text = self.canvas.itemcget(self.last_text_id, 'text')
            new_text = simpledialog.askstring("Edit Text", "Enter new text:", initialvalue=current_text)

            if new_text is not None:
                # Update the text on the canvas
                self.canvas.itemconfig(self.last_text_id, text=new_text)

                # Also update the drawn image if needed
                self.draw.text((self.canvas.coords(self.last_text_id)[0], self.canvas.coords(self.last_text_id)[1]), new_text, font=None, fill=self.color)

    def open_gallery(self):
        # Open a folder with saved drawings
         file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
         if file_path:
           self.load_outline(file_path)

    def activate_brush_mode(self):
        # Switch to brush mode
        self.mode = 'brush'
        # Unbind text insertion handlers
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Key>")
        # Bind brush handlers
        self.canvas.bind("<B1-Motion>", self.draw_on_canvas)
        self.canvas.bind("<ButtonPress-1>", self.start_drawing)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def activate_text_mode(self):
        # Switch to text mode
        self.mode = 'text'
        # Unbind brush handlers
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        # Bind text insertion handlers
        self.canvas.bind("<Button-1>", self.insert_text)

    def save_progress(self):
        # Ask the user where they want to save the file
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            try:
                self.image.save(file_path, "PNG")
                messagebox.showinfo("Progress Saved", f"Your progress has been saved as {file_path}.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save progress: {e}")
        else:
            messagebox.showinfo("Save Cancelled", "Your progress was not saved.")

    def save_warning(self):
        # Display a warning when the user attempts to close the app without saving
        if messagebox.askyesno("Save Progress", "Do you want to save your progress before exiting?"):
            self.save_progress()
        self.root.destroy()  # Close the app after saving or if the user chooses not to save

    def insert_text(self):
        # Prompt the user to input the text
        text = tk.simpledialog.askstring("Insert Text", "Enter the text:")
    
        if text:
           # Wait for the user to click on the canvas to position the text
           self.canvas.bind("<Button-1>", lambda event: self.place_text(event, text))

    def change_background(self):
        color = colorchooser.askcolor()[1]
        if color:
         self.canvas.config(bg=color)

    def open_gallery(self):
        # Open a folder with saved drawings
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file_path:
         self.load_outline(file_path)

    def undo(self):
        if self.undo_stack:
            state = self.undo_stack.pop()
            self.redo_stack.append(self.image.tobytes())  # Save current state to redo stack
            self.image = Image.open(io.BytesIO(state))
            self.draw = ImageDraw.Draw(self.image)
            self.update_canvas()

    def redo(self):
        if self.redo_stack:
            state = self.redo_stack.pop()
            self.undo_stack.append(self.image.tobytes)
            self.image = Image.open(io.BytesIO(state))
            self.draw = ImageDraw.Draw(self.image)
            self.update_canvas()

    def bind_brush(self):
        # Bind the mouse event to the brush drawing function
        self.canvas.bind("<B1-Motion>", self.paint)

    def update_canvas(self):
        """ Update the canvas with the current image """
        self.canvas_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas_image)
        self.canvas.image = self.canvas_image  # Keep reference to avoid garbage collection

    def load_mini_pictures(self):
        self.widget_dict={} #create a dictionary to store labels and lock labels
        self.complete_buttons={} #dictionary for complete buttons

        levels = {
            "Level 1 - Easy" : [f"level1/outline{i}_level1.jpg" for i in range(1, 7)],
            "Level 2 - Normal": [f"level2/outline{i}_level2.jpg" for i in range(1, 7)],
            "Level 3 - Hard": [f"level3/outline{i}_level3.jpg" for i in range(1, 7)],
            "Level 4 - Insane": [f"level4/outline{i}_level4.jpg" for i in range(1, 7)],
            "Level 5 - Impossible": [f"level5/outline{i}_level5.jpg" for i in range(1, 7)],  # Add more levels as needed
        }
        
        start_y = 0
        row_height = 90 + 5  # Height of images plus padding

        for level, mini_pics in levels.items():
            # Create a label for the level
            level_label = tk.Label(self.mini_pics_frame, text=level, font=("Arial", 12, "bold"))
            level_label.pack(side=tk.TOP, anchor=tk.W, pady=5)

            # Create a frame for this level's images
            level_frame = tk.Frame(self.mini_pics_frame)
            level_frame.pack(side=tk.TOP, fill=tk.X)

            for i, pic in enumerate(mini_pics):
                pic_path = os.path.join(self.assets_directory, pic)
                print(f"Attempting to load image: {pic_path}")  # Debug: Print the image path

                try:
                    if not os.path.exists(pic_path):
                        print(f"Image not found: {pic_path}")  # Debug: Image not found
                        continue  # Skip to the next image

                    img = Image.open(pic_path).resize((80, 75), Image.LANCZOS)  # Resize to fit
                    img_tk = ImageTk.PhotoImage(img)
                    label = tk.Label(level_frame, image=img_tk)
                    label.image = img_tk  # Keep a reference to avoid garbage collection
                    label.grid(row=i // 6, column=i % 6, padx=5, pady=5)  # Use grid for layout

                     # Bind click event to load the outline on the canvas
                    label.bind("<Button-1>", lambda event, image_path=pic_path: self.load_outline(image_path))
                    print(f"Loaded image successfully: {pic_path}")  # Debug: Successful load

                    self.widget_dict[(level,i)]=label

                    if level =="Level 1 - Easy" and i % 2 !=0:
                        complete_button=tk.Button(level_frame,text="Complete", command=lambda level=level, i=i:self.complete_page(level,i))
                        complete_button.grid(row=i // 6+1, column= i % 6, padx=5, pady=3)
                        self.complete_buttons[(level,i)]

                    #add lock icon to the locked outline pages
                    if level != "Level 1 - Easy" and i % 2 != 0 :
                        lock_img=Image.open("lock.png")
                        lock_img=lock_img.resize((80,80),Image.LANCZOS)
                        lock_icon=ImageTk.PhotoImage(lock_img)
                        lock_label=tk.Label(label,image=lock_icon)
                        lock_label.image=lock_icon
                        lock_label.place(relx=0.5,rely=0.5, anchor=tk.CENTER)

                     # store the lock label in the widget
                        self.widget_dict[(level,i,'lock')]=lock_label

                     #disable the label and button when the page is locked
                        label.config(state="disabled")      

                     # create unlock button
                        unlock_button=tk.Button(level_frame,text="Unlock Page", command=lambda level=level, i=i, level_frame=level_frame:self.unlock_page(level,i,level_frame))   
                        unlock_button.grid(row=i // 6 + 1, column=i % 6, padx=5, pady=3)
                        self.widget_dict[(level,i,'unlock')]= unlock_button #store the unlock button


                except Exception as e:
                    print(f"Failed to load mini picture: {e}")  # Debug: Print error details

                    print(self.widget_dict)
    
            # Update starting y position for the next level
            start_y += len(mini_pics) // 5 * row_height + row_height  # Move to the next row

    def unlock_page(self,level,i,level_frame):
        #coins neede per page in a certain level
        coins_needed={
            "Level 2 - Normal":10,
            "Level 3 - Hard":20,
            "Level 4 - Insane":30,
            "Level 5 - Impossible":40
        }       

        coins_required=coins_needed.get(level,0) 

        if self.coins >= coins_required:
            response=messagebox.askyesno("Confirm Purchase",f"Are you sure you want to unlock Page {i} in {level} for {coins_required} coins ?")
            if response:
              self.coins -= coins_required #decuts coins after purchase
              self.coins_label.config(text=f"Coins: {self.coins}")
                
              print(self.widget_dict)

        #get the label and lock label from dictionary
              label=self.widget_dict.get((level,i))
              lock_label=self.widget_dict.get((level,i,'lock'))   
              
               
              #disable the button after successfuly purchase
              unlock_button=self.widget_dict.get((level,i,'unlock'))
              if unlock_button:
                  unlock_button.grid_forget()
                  self.widget_dict.pop((level,i,'unlock'))

                  #create a complete button
                  complete_button=tk.Button(level_frame, text="Complete",command=lambda level=level, i=i: self.complete_page(level,i))
                  complete_button.grid(row=i//6 + 1, column=i % 6, padx=5, pady=3)
                  self.complete_buttons[(level,i)]=complete_button

                  
              if lock_label :
              #debug issues
               print(f"Lock label found for ({level},{i})")
               lock_label.destroy()
               print(f"Lock label destroyed for ({level,{i}})")
              else:
               print(f"No lock label found for ({level},{i})")

              if label:
               label.config(state="normal")
               message=f"Page {i} in {level} has been unlocked !\nCoins deducted:{coins_required}"
               messagebox.showinfo("Success",message)
              else:
               messagebox.showerror("Error","Page label not found")
            else:
              messagebox.showinfo("Cancelled","Unlock cancelled")
        else:
            challenge_response=messagebox.askyesno("Challenge",f"Do you want to complete a challenge to unlock Page {i} in {level} for free ?")

        if challenge_response:
            #display question
            self.generate_challenge()
            messagebox.showinfo("Challenge",f"Answer this question to unlock this page:\n\n{self.challenge_question}")   
            user_input=simpledialog.askstring("Challenge","Enter your response:") 

            if self.check_user_input(user_input):
                label=self.widget_dict.get((level,i))
                lock_label=self.widget_dict.get((level,i,'lock'))

                unlock_button=self.widget_dict.get((level,i,'unlock'))
                if unlock_button:
                    unlock_button.grid_forget()
                    self.widget_dict.pop((level,i,'unlock'))

                    # create complete button
                    complete_button=tk.Button(level_frame,text="Complete", command=lambda level=level,i=i:self.complete_page(level,i))
                    complete_button.grid(row=i // 6 + 1,column=i % 6, padx=5, pady=3)
                    self.complete_buttons[(level,i)]=complete_button

                if lock_label:
                  #debug issues
                    print(f"Lock label found for ({level},{i})")
                    lock_label.destroy()
                    print(f"Lock label destroyed for ({level,{i}})")
                else:
                    print(f"No lock label found for ({level},{i})")

                if label:
                        label.config(state="normal")
                        message=f"Page {i} in {level} has been unlocked !\nYou earned 10 coins for completing the challenge"
                        messagebox.showinfo("Success",message)
                        self.coins += 10
                        self.coins_label.config(text=f"Coins: {self.coins}")
                else:
                        messagebox.showerror("Error","Page label not found")
            else:
                       messagebox.showerror("Error", "Incorrect response.Try againn !")  
        else:
                messagebox.showerror("Not enough coins", f"You need {coins_required} coins to unlock this page !")         

    def generate_challenge(self):
        questions=[
            ("What has hands and a face,but can't hold anything or smile ?","clock"),
            ("I have a tail and a head,but no body.What am I ?","coin"),
            ("What has keys but can't open locks?","piano"),
            ("Write the word 'rainbow' ?","rainbow"),
            ("What comes down but never goes up ?","rain"),
            ("Spell the word 'bee' ? ", "bee")
        ]           
        question,answer=random.choice(questions) 
        self.challenge_question=question
        self.challenge_answer=answer

    def check_user_input(self,user_input):
        return user_input.strip() == self.challenge_answer.strip()
        

    def complete_page(self, level, i):
        if not self.completed_pages[level][i]:
            self.completed_pages[level][i] = True
            
            #coins earned
            if level == "Level 2 - Normal":
                coins_earned=30
            elif level =="Level 3 - Hard":
                coins_earned=40
            elif level == "Level 4 - Insane":
                coins_earned=50
            elif level == "Level 5 - Impossible":
                coins_earned=60    
            else:
                coins_earned=20            
            self.coins += coins_earned # default coins earned value for level 1
            self.coins_label.config(text=f"Coins: {self.coins}")
            messagebox.showinfo("Congratulations!", f"You have earned {coins_earned} coins !")

            # Disable button after clicking once
            complete_button = self.complete_buttons.get((level, i))
            if complete_button:
                complete_button.config(state="disabled")
                complete_button.grid_forget()
                self.complete_buttons.pop()
                
        else:
            messagebox.showinfo("Ooops","Looks like you have already completed this page!")
            

    def load_outline(self, image_path):
        try:
            self.save_state()  # Save the current state before loading a new outline

            # Load the original image
            original_image = Image.open(image_path)

            # Load the outline image
            outline_image = original_image

            # Resize images to fit the canvas
            original_image_resized = original_image.resize((self.canvas_width, self.canvas_height), Image.LANCZOS)
            outline_image_resized = outline_image.resize((self.canvas_width, self.canvas_height), Image.LANCZOS)

            # Display the outline on the canvas
            self.canvas_image = ImageTk.PhotoImage(outline_image_resized)
            self.canvas.create_image(1, 1, anchor=tk.NW, image=self.canvas_image)

            # Show the original and outline images on the right side
            self.show_selected_images(image_path, original_image_resized, outline_image_resized)

            # Update the image and draw object to the new outline
            self.image = outline_image_resized.copy()
            self.draw = ImageDraw.Draw(self.image)

            # Start the timer
            self.start_timer()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load outline: {e}")

    def place_text(self, event, text):
        x, y = event.x, event.y

        # Choose a font size (this can be made adjustable)
        font_size = 20
        font = ("Arial", font_size)

        # Draw the text on the canvas
        self.canvas.create_text(x, y, text=text, font=font, fill=self.color)
    
        # Also draw the text on the image to ensure it's saved
        self.draw.text((x, y), text, font=None, fill=self.color)

        # Unbind the click event after placing the text (Text mode ends)
        self.canvas.unbind("<Button-1>")

        # Rebind the brush tool (Enable brush mode again)
        self.bind_brush()

    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
    
        # Draw on the canvas
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.color, outline=self.color)

        # Also draw on the image for saving purposes
        self.draw.line([x1, y1, x2, y2], fill=self.color, width=self.brush_size)

    def resize_image(image_path, new_width, new_height):
        # Open the image
        image = Image.open(image_path)
    
        # Resize the image
        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
    
        # Return the resized image
        return resized_image
  
    def show_selected_images(self, image_path, original_image, outline_image):
        # Clear previous images
        for widget in self.selected_frame.winfo_children():
            widget.destroy()

        try:
            # Display the original image
            original_image_tk = ImageTk.PhotoImage(original_image.resize((100, 100), Image.LANCZOS))
            tk.Label(self.selected_frame, image=original_image_tk).pack(side=tk.LEFT, padx=5, pady=5)
            self.original_image_tk = original_image_tk  # Keep a reference

            # Display the outline image
            outline_image_tk = ImageTk.PhotoImage(outline_image.resize((100, 100), Image.LANCZOS))
            tk.Label(self.selected_frame, image=outline_image_tk).pack(side=tk.LEFT, padx=5, pady=5)
            self.outline_image_tk = outline_image_tk  # Keep a reference

        except Exception as e:
            messagebox.showerror("Error", f"Failed to show selected images: {e}")

    def set_custom_timer(self):
    # Ask the user to input time (in minutes)
       custom_time = simpledialog.askinteger("Set Timer", "Enter time duration in minutes:", minvalue=1, maxvalue=1440)
       if custom_time:
        self.timer_duration = custom_time * 60  # Convert to seconds
        self.time_left = self.timer_duration
        self.timer = f"{custom_time:02}:00"
        self.timer_label.config(text=f"Timer: {self.timer}")

    def start_timer(self):
      if not self.timer_running:
        self.timer_running = True
        self.time_left = self.timer_duration
        self.update_timer()
    
    def update_timer(self):
      if self.timer_running:
        minutes, seconds = divmod(self.time_left, 60)
        time_format = f"{minutes:02}:{seconds:02}"
        self.timer_label.config(text=f"Timer: {time_format}")

        if self.time_left > 0:
            self.time_left -= 1
            self.root.after(1000, self.update_timer)  # Update timer every second
        else:
            self.timer_running = False
            self.save_progress()
            messagebox.showinfo("Time's Up", "The timer has ended!")
            self.root.destroy()

    def set_shape_mode(self, shape):
       """ Set the current shape mode for drawing """
       self.shape_mode = shape
       self.eraser_mode = False  # Disable eraser mode when in shape mode
       self.eraser_button.config(relief=tk.RAISED)  # Reset eraser button appearance

    def start_drawing(self, event):
       self.drawing = True
       self.start_x = event.x
       self.start_y = event.y
       self.save_state()  # Save state before drawing

    def stop_drawing(self, event):
       if self.shape_mode:  # Check if a shape is being drawn
        end_x = event.x
        end_y = event.y
        self.draw_shape(self.shape_mode, self.start_x, self.start_y, end_x, end_y)
        self.drawing = False
        self.canvas.delete("temp")  # Clear temporary shape

    def draw_on_canvas(self, event):
       """ Draw on the canvas, handling both brush, eraser, and shape modes """
       if self.shape_mode:
        # Remove only the shape that is currently being drawn (for smooth drawing effect)
        self.canvas.delete("current_temp")  # Clear the currently drawn temporary shape

        # Draw shapes based on the selected shape mode
        if self.shape_mode == 'circle':
            self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, 
                                    outline=self.color, width=self.brush_size, tags="current_temp")
        elif self.shape_mode == 'rectangle':
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, 
                                         outline=self.color, width=self.brush_size, tags="current_temp")
        elif self.shape_mode == 'line':
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, 
                                    fill=self.color, width=self.brush_size, tags="current_temp")
       else:
        # Brush and eraser functionality
        size = self.eraser_size if self.eraser_mode else self.brush_size
        color = "white" if self.eraser_mode else self.color

        # Calculate the coordinates for the brush or eraser
        x1, y1 = (event.x - size), (event.y - size)
        x2, y2 = (event.x + size), (event.y + size)

        # Draw on canvas for brush or eraser
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)

        # Also draw on the image for saving purposes
        self.draw.ellipse([x1, y1, x2, y2], fill=color)

    def finalize_shape(self, event):
       """ Make the drawn shape permanent when the mouse is released """
       if self.shape_mode:
        # Draw the shape permanently on canvas and image
        self.draw_shape(self.shape_mode, self.start_x, self.start_y, event.x, event.y)

        # Clear the temporary shape
        self.canvas.delete("current_temp")

    def draw_shape(self, shape, start_x, start_y, end_x, end_y):
       """ Draws the selected shape on both the canvas and the internal image """
       if shape == 'circle':
        # Draw the circle on the canvas
        self.canvas.create_oval(start_x, start_y, end_x, end_y, outline=self.color, width=self.brush_size)
        # Draw the circle on the image
        self.draw.ellipse([start_x, start_y, end_x, end_y], outline=self.color, width=self.brush_size)
    
       elif shape == 'rectangle':
        # Draw the rectangle on the canvas
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, outline=self.color, width=self.brush_size)
        # Draw the rectangle on the image
        self.draw.rectangle([start_x, start_y, end_x, end_y], outline=self.color, width=self.brush_size)
    
       elif shape == 'line':
        # Draw the line on the canvas
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=self.color, width=self.brush_size)
        # Draw the line on the image
        self.draw.line([start_x, start_y, end_x, end_y], fill=self.color, width=self.brush_size)
    
       # After drawing the shape, update the canvas to reflect the new changes
       self.update_canvas()


    # Update eraser size when slider is changed
    def update_eraser_size(self, value):
        self.eraser_size = int(value)

    # Bind the slider change event to the update function
        self.eraser_size_slider.config(command=self.update_eraser_size)
    
    def insert_text(self, event):
        # Function to insert text at mouse click position
        x, y = event.x, event.y
        text = simpledialog.askstring("Input", "Enter the text:")
        if text:
            self.canvas.create_text(x, y, text=text, fill=self.color, font=("Arial", 16))

    def change_brush_size(self, event):
        self.brush_size = event.widget.get()

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.color = color
            self.eraser_mode = False  # Disable eraser when choosing a color
            self.eraser_button.config(relief=tk.RAISED)  # Reset eraser button appearance

    def toggle_eraser(self):
        """ Toggle eraser mode on or off """
        self.eraser_mode = not self.eraser_mode
        if self.eraser_mode:
            self.eraser_button.config(text="Brush Mode")
        else:
            self.eraser_button.config(text="Eraser Mode")

    def clear_canvas(self):
        self.save_state()  # Save current state before clearing
        self.canvas.delete("all")
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

    def save_drawing(self):
        """ Save the current drawing to a file """
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.save_state()  # Save current state before saving the image
            self.image.save(file_path)
            messagebox.showinfo("Save Drawing", "Drawing saved successfully!")   

            level=self.get_current_level()
            if level:
                coins_earned= self.get_current_level()
                self.coins += coins_earned
                self.coins_label.config(text=f"Coins:{self.coins}")
                messagebox.showinfo("Congratulations !", f"You have earned {coins_earned} coins for saving your page in {level} !")

    def blank_page(self):
        """ Create a new blank page """
        self.save_state()  # Save current state before creating a blank page
        self.clear_canvas()  # Clear the current canvas

if __name__ == "__main__":
    root = tk.Tk()
    app = KidsDrawingApp(root)
    root.mainloop()