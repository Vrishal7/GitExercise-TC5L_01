import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk, ImageFilter
import io
from io import BytesIO
import os
from tkinter import simpledialog

class KidsDrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kids Drawing App")

        # Canvas dimensions
        self.canvas_width = 800
        self.canvas_height = 900

        # Coin system
        self.coins = 0

        # Timer variables
        self.timer_duration = 30 * 60  # 30 minutes in seconds
        self.time_left = self.timer_duration
        self.timer_running = False

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

        # Bind mouse events to canvas
        self.canvas.bind("<ButtonPress-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw_on_canvas)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        # Track completed pages
        self.completed_pages = {"Level 1 - Easy": [False] * 6}

        #initialize complete button
        self.complete_buttons={}

    def create_widgets(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Display coins
        self.coins_label = tk.Label(toolbar, text=f"Coins: {self.coins}", font=("Arial", 14))
        self.coins_label.pack(side=tk.TOP, padx=1)

        # Open Folder Button
        gallery_button = tk.Button(toolbar, text="Open Folder", command=self.open_gallery)
        gallery_button.pack(side=tk.LEFT, padx=1)

        # Timer Label
        self.timer_label = tk.Label(toolbar, text="Timer: 30:00", font=("Arial", 14))
        self.timer_label.pack(side=tk.TOP, padx=1)

        # Brush Size Slider
        size_slider = tk.Scale(toolbar, from_=1, to=10, orient=tk.HORIZONTAL, label="Brush Size")
        size_slider.set(self.brush_size)
        size_slider.pack(side=tk.LEFT, padx=1)
        size_slider.bind("<Motion>", self.change_brush_size)

        # Color Button
        color_button = tk.Button(toolbar, text="Choose Color", command=self.choose_color)
        color_button.pack(side=tk.LEFT, padx=1)

        # Eraser Button
        self.eraser_button = tk.Button(toolbar, text="Eraser", command=self.toggle_eraser)
        self.eraser_button.pack(side=tk.LEFT, padx=1)

        # Save Button
        save_button = tk.Button(toolbar, text="Save Drawing", command=self.save_drawing)
        save_button.pack(side=tk.LEFT, padx=1)

        # Clear Button
        clear_button = tk.Button(toolbar, text="Clear", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT, padx=1)

        # Undo Button
        undo_button = tk.Button(toolbar, text="Undo", command=self.undo)
        undo_button.pack(side=tk.LEFT, padx=1)

        # Brush Mode
        self.brush_button = tk.Button(root, text="Brush Mode", command=self.activate_brush_mode)
        self.brush_button.pack(side=tk.LEFT)

        # Text Mode
        self.text_button = tk.Button(root, text="Text Mode", command=self.activate_text_mode)
        self.text_button.pack(side=tk.LEFT)

        # Blank Page Button
        blank_page_button = tk.Button(toolbar, text="Blank Page", command=self.blank_page)
        blank_page_button.pack(side=tk.LEFT, padx=1)
        
        # Background Button
        bg_button = tk.Button(toolbar, text="Change Background", command=self.change_background)
        bg_button.pack(side=tk.LEFT, padx=1)

        # Mini Picture Section
        right_frame = tk.Frame(self.root, bd=2, relief=tk.RAISED)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.mini_pics_frame = tk.Frame(right_frame)
        self.mini_pics_frame.pack(side=tk.TOP, fill=tk.X)

        self.selected_frame = tk.Frame(right_frame)
        self.selected_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.load_mini_pictures()

    def save_state(self):
        """ Save the current state of the image to the undo stack """
        state = io.BytesIO()
        self.image.save(state, format="PNG")
        self.undo_stack.append(state.getvalue())
        self.redo_stack.clear()  # Clear redo stack on new action

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

                    img = Image.open(pic_path).resize((80, 80), Image.LANCZOS)  # Resize to fit
                    img_tk = ImageTk.PhotoImage(img)
                    label = tk.Label(level_frame, image=img_tk)
                    label.image = img_tk  # Keep a reference to avoid garbage collection
                    label.grid(row=i // 6, column=i % 6, padx=5, pady=5)  # Use grid for layout

                     # Bind click event to load the outline on the canvas
                    label.bind("<Button-1>", lambda event, image_path=pic_path: self.load_outline(image_path))
                    print(f"Loaded image successfully: {pic_path}")  # Debug: Successful load

                    self.widget_dict[(level,i)]=label

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
                        unlock_button=tk.Button(level_frame,text="Unlock Page", command=lambda level=level, i=i:self.unlock_page(level,i))   
                        unlock_button.grid(row=i // 6 + 1, column=i % 6, padx=5, pady=3)
                        self.widget_dict[(level,i,'unlock')]= unlock_button #store the unlock button

                    if level == "Level 1 - Easy" and i % 2 != 0:
                        complete_button = tk.Button(level_frame, text="Complete Page", command=lambda level=level, i=i: self.complete_page(level, i))
                        complete_button.grid(row=i // 6 + 1, column=i % 6, padx=5, pady=3)
                        self.complete_buttons[(level, i)] = complete_button

                except Exception as e:
                    print(f"Failed to load mini picture: {e}")  # Debug: Print error details

                    print(self.widget_dict)
    
            # Update starting y position for the next level
            start_y += len(mini_pics) // 5 * row_height + row_height  # Move to the next row

    def unlock_page(self,level,i):
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
                  unlock_button.config(state="disabled")

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
            messagebox.showerror("Not enough coins",f"You need {coins_required} coins to unlock this page.")    
                    

    def complete_page(self, level, i):
        if not self.completed_pages[level][i]:
            self.completed_pages[level][i] = True
            self.coins += 50  # Earn 50 coins for Level 1
            self.coins_label.config(text=f"Coins: {self.coins}")
            messagebox.showinfo("Congratulations!", "You have earned 50 coins")

            # Disable button after clicking once
            complete_button = self.complete_buttons.get((level, i))
            if complete_button:
                complete_button.config(state="disabled")
        else:
            messagebox.showinfo("Looks like you have already completed this page!")

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
                messagebox.showinfo("Time's Up", "The 30-minute timer has ended!")

    def start_drawing(self, event):
        if self.mode == 'brush' and not self.eraser_mode:
            self.drawing = True
            self.previous_x, self.previous_y = event.x, event.y
            self.save_state()  # Save state before drawing starts
        elif self.mode == 'brush' and self.eraser_mode:
            self.drawing = True
            self.previous_x, self.previous_y = event.x, event.y
            self.save_state()  # Save state before erasing starts

    def stop_drawing(self, event):
        if self.mode == 'brush':
            self.drawing = False
        self.previous_x, self.previous_y = None, None  # Reset previous points

    def draw_on_canvas(self, event):
        """ Draw on the canvas, handling both brush and eraser modes """
        x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
        x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)

        # Check if the mode is eraser
        if self.eraser_mode:
            size = self.eraser_size  # Use eraser size when eraser is active
            color = "white"  # Eraser color (background color)
        else:
            size = self.brush_size  # Use brush size otherwise
            color = self.color

        x1, y1 = (event.x - size), (event.y - size)
        x2, y2 = (event.x + size), (event.y + size)

    # Draw on canvas
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)

    # Also draw on the image for saving purposes
        self.draw.ellipse([x1, y1, x2, y2], fill=color)

    # Eraser size slider
        self.eraser_size_slider = tk.Scale(self, from_=1, to=50, orient="horizontal", label="Eraser Size")
        self.eraser_size_slider.set(self.eraser_size)  # Set default value
        self.eraser_size_slider.pack()

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

    def blank_page(self):
        """ Create a new blank page """
        self.save_state()  # Save current state before creating a blank page
        self.clear_canvas()  # Clear the current canvas

if __name__ == "__main__":
    root = tk.Tk()
    app = KidsDrawingApp(root)
    root.mainloop()