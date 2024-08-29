import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

class KidsDrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kids Drawing App")

        # Buttons and Options
        self.create_widgets()

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