import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

class KidsDrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kids Drawing App")

        # Canvas dimensions
        self.canvas_width = 800
        self.canvas_height = 600

        # Create canvas
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack(side=tk.LEFT)

        # Draw Variables
        self.color = 'black'
        self.brush_size = 5
        self.drawing = False

        # Create image and draw objects
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

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

        # Color Button
        color_button = tk.Button(toolbar, text="Choose Color")
        color_button.pack(side=tk.LEFT, padx=5)

        # Eraser Button
        eraser_button = tk.Button(toolbar, text="Eraser")
        eraser_button.pack(side=tk.LEFT, padx=5)

        # Save Button
        save_button = tk.Button(toolbar, text="Save Drawing")
        save_button.pack(side=tk.LEFT, padx=5)

        # Clear Button
        clear_button = tk.Button(toolbar, text="Clear")
        clear_button.pack(side=tk.LEFT, padx=5)

        # Mini Picture Section
        right_frame = tk.Frame(self.root, bd=2, relief=tk.RAISED)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        mini_pics_frame = tk.Frame(right_frame)
        mini_pics_frame.pack(side=tk.TOP, fill=tk.X)

        selected_frame = tk.Frame(right_frame)
        selected_frame.pack(side=tk.BOTTOM, fill=tk.X)

    def start_drawing(self, event):
        self.drawing = True

    def stop_drawing(self, event):
        self.drawing = False

    def draw_on_canvas(self, event):
        if self.drawing:
            x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
            x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)
            self.canvas.create_oval(x1, y1, x2, y2, fill=self.color, outline=self.color)

if __name__ == "__main__":
    root = tk.Tk()
    app = KidsDrawingApp(root)
    root.mainloop()