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

    def create_widgets(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Brush Size Slider
        size_slider = tk.Scale(toolbar, from_=1, to=10, orient=tk.HORIZONTAL, label="Brush Size")
        size_slider.set(self.brush_size)
        size_slider.pack(side=tk.LEFT, padx=5)
        size_slider.bind("<Motion>", self.change_brush_size)

        # Color Button
        color_button = tk.Button(toolbar, text="Choose Color", command=self.choose_color)
        color_button.pack(side=tk.LEFT, padx=5)

        # Eraser Button
        self.eraser_button = tk.Button(toolbar, text="Eraser", command=self.toggle_eraser)
        self.eraser_button.pack(side=tk.LEFT, padx=5)

        # Save Button
        save_button = tk.Button(toolbar, text="Save Drawing")
        save_button.pack(side=tk.LEFT, padx=5)

        # Clear Button
        clear_button = tk.Button(toolbar, text="Clear", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT, padx=5)

        # Undo Button
        undo_button = tk.Button(toolbar, text="Undo", command=self.undo)
        undo_button.pack(side=tk.LEFT, padx=5)

        # Redo Button
        redo_button = tk.Button(toolbar, text="Redo", command=self.redo)
        redo_button.pack(side=tk.LEFT, padx=5)

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
        mini_pics = [f"outline{i}.jpg" for i in range(1, 7)]  # Update file names as needed
        self.mini_pic_images = []

        for pic in mini_pics:
            pic_path = os.path.join(self.assets_directory, pic)
            try:
                print(f"Trying to load image: {pic_path}")  # Debug print statement
                img = Image.open(pic_path).resize((100, 100), Image.LANCZOS)  # Resize to fit
                img_tk = ImageTk.PhotoImage(img)
                label = tk.Label(self.mini_pics_frame, image=img_tk)
                label.image = img_tk  # Keep a reference to avoid garbage collection
                label.pack(side=tk.LEFT, padx=5, pady=5)

                # Bind click event to load the outline on the canvas
                label.bind("<Button-1>", lambda event, image_path=pic_path: self.load_outline(image_path))
                self.mini_pic_images.append(label)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load mini picture: {e}")

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
                self.canvas.create_oval(x1, y1, x2, y2, fill=self.color, outline=self.color)
                self.draw.ellipse([x1, y1, x2, y2], fill=self.color, outline=self.color)
            self.update_canvas()

    def change_brush_size(self, event):
        self.brush_size = event.widget.get()

    def choose_color(self):
        self.color = colorchooser.askcolor(color=self.color)[1]

    def toggle_eraser(self):
        """ Toggle between drawing and eraser mode """
        self.eraser_mode = not self.eraser_mode
        if self.eraser_mode:
            self.color = 'white'  # Set the color to white for erasing
            self.eraser_button.config(relief=tk.SUNKEN)
        else:
            self.color = 'black'  # Reset to default color
            self.eraser_button.config(relief=tk.RAISED)

    def clear_canvas(self):
        self.save_state()  # Save state before clearing
        self.canvas.delete("all")
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

if __name__ == "__main__":
    root = tk.Tk()
    app = KidsDrawingApp(root)
    root.mainloop()
