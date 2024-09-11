import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk, ImageFilter
import io
import os

class KidsDrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kids Drawing App")

        # Canvas dimensions
        self.canvas_width = 900
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

        # Draw Variables
        self.color = 'black'
        self.brush_size = 5
        self.drawing = False
        self.eraser_mode = False  # Initialize eraser mode

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
        self.completed_pages = {"Level 1": [False] * 6}

        #initialize complete button
        self.complete_buttons={}

    def create_widgets(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Display coins
        self.coins_label = tk.Label(toolbar, text=f"Coins: {self.coins}", font=("Arial", 14))
        self.coins_label.pack(side=tk.LEFT, padx=1)

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

        # Redo Button
        redo_button = tk.Button(toolbar, text="Redo", command=self.redo)
        redo_button.pack(side=tk.LEFT, padx=1)

        # Timer Label
        self.timer_label = tk.Label(toolbar, text="Timer: 30:00", font=("Arial", 14))
        self.timer_label.pack(side=tk.RIGHT, padx=1)

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
            self.save_state()  # Save current state to undo stack
            self.image = Image.open(io.BytesIO(state))
            self.draw = ImageDraw.Draw(self.image)
            self.update_canvas()

    def update_canvas(self):
        """ Update the canvas with the current image """
        self.canvas_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas_image)
        self.canvas.image = self.canvas_image  # Keep reference to avoid garbage collection

    def load_mini_pictures(self):
        self.widget_dict={} #create a dictionary to store labels and lock labels

        levels = {
            "Level 1": [f"level1/outline{i}_level1.jpg" for i in range(1, 7)],
            "Level 2": [f"level2/outline{i}_level2.jpg" for i in range(1, 7)],
            "Level 3": [f"level3/outline{i}_level3.jpg" for i in range(1, 7)],
            "Level 4": [f"level4/outline{i}_level4.jpg" for i in range(1, 7)],
            "Level 5": [f"level5/outline{i}_level5.jpg" for i in range(1, 7)],  # Add more levels as needed
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

                    img = Image.open(pic_path).resize((90, 90), Image.LANCZOS)  # Resize to fit
                    img_tk = ImageTk.PhotoImage(img)
                    label = tk.Label(level_frame, image=img_tk)
                    label.image = img_tk  # Keep a reference to avoid garbage collection
                    label.grid(row=i // 6, column=i % 6, padx=5, pady=5)  # Use grid for layout

                     # Bind click event to load the outline on the canvas
                    label.bind("<Button-1>", lambda event, image_path=pic_path: self.load_outline(image_path))
                    print(f"Loaded image successfully: {pic_path}")  # Debug: Successful load

                    self.widget_dict[(level,i)]=label

                    #add lock icon to the locked outline pages
                    if level != "Level 1" and i % 2 != 0 :
                        lock_img=Image.open("lock.png")
                        lock_img=lock_img.resize((50,50),Image.LANCZOS)
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

                    elif level == "Level 1" and i % 2 != 0:
                        complete_button = tk.Button(level_frame, text="Complete Page", command=lambda level=level, i=i: self.complete_page(level, i))
                        complete_button.grid(row=i // 6 + 1, column=i % 6, padx=5, pady=3)
                        self.complete_buttons[(level, i)] = complete_button

                except Exception as e:
                    print(f"Failed to load mini picture: {e}")  # Debug: Print error details

                    print(self.widget_dict)
    
            # Update starting y position for the next level
            start_y += len(mini_pics) // 5 * row_height + row_height  # Move to the next row

    def unlock_page(self,level,i):
        coins_needed={
            "Level 2":10,
            "Level 3":20,
            "Level 4":30,
            "Level 5":40
        }       

        coins_required=coins_needed.get(level,0) 

        if self.coins >= coins_required:
            response=messagebox.askyesno("Confirm Purchase",f"Are you sure you want to unlock Page {i} in {level} for {coins_required} coins ?")
            if response:
              self.coins -= coins_required
              self.coins_label.config(text=f"Coins: {self.coins}")
                
              print(self.widget_dict)

        #get the label and lock label from dictionary
              label=self.widget_dict.get((level,i))
              lock_label=self.widget_dict.get((level,i,'lock'))    

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
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas_image)

            # Show the original and outline images on the right side
            self.show_selected_images(image_path, original_image_resized, outline_image_resized)

            # Update the image and draw object to the new outline
            self.image = outline_image_resized.copy()
            self.draw = ImageDraw.Draw(self.image)

            # Start the timer
            self.start_timer()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load outline: {e}")

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
        self.drawing = True
        self.save_state()  # Save state before drawing

    def stop_drawing(self, event):
        self.drawing = False

    def draw_on_canvas(self, event):
        if self.drawing:
            x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
            x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)
            if self.eraser_mode:
                # Draw an eraser
                self.canvas.create_oval(x1, y1, x2, y2, fill='white', outline='white')
                self.draw.ellipse([x1, y1, x2, y2], fill='white', outline='white')
            else:
                # Draw a brush stroke
                self.canvas.create_oval(x1, y1, x2, y2, fill=self.color, outline=self.color)
                self.draw.ellipse([x1, y1, x2, y2], fill=self.color, outline=self.color)

    def change_brush_size(self, event):
        self.brush_size = event.widget.get()

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.color = color
            self.eraser_mode = False  # Disable eraser when choosing a color
            self.eraser_button.config(relief=tk.RAISED)  # Reset eraser button appearance

    def toggle_eraser(self):
        self.eraser_mode = not self.eraser_mode
        if self.eraser_mode:
            self.eraser_button.config(relief=tk.SUNKEN)
        else:
            self.eraser_button.config(relief=tk.RAISED)

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

if __name__ == "__main__":
    root = tk.Tk()
    app = KidsDrawingApp(root)
    root.mainloop()