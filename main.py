import tkinter as tk
from canvas_area import CanvasArea
from toolbar import Toolbar
from mini_pictures import MiniPictures
import config

class KidsDrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kids Drawing App")

        # Create canvas area
        self.canvas_area = CanvasArea(root)

        # Create toolbar
        self.toolbar = Toolbar(root, self.canvas_area)

        # Create mini pictures section
        self.mini_pictures = MiniPictures(root)

if __name__ == "__main__":
    root = tk.Tk()
    app = KidsDrawingApp(root)
    root.mainloop()
