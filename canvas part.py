
import tkinter as tk

class KidsDrawingApp:
    def __init__(self,root):
        self.root=root
        self.root.title("Kids Drawing App")

        #Create dimensions
        self.canvas_width=900
        self.canvas_height=900

        #Create canvas
        self.canvas=tk.Canvas(root,width=self.canvas_width,height=self.canvas_height,bg='white')
        self.canvas.pack(side=tk.LEFT)

        if __name__ == "__main__":
            root=tk.Tk()
            app= KidsDrawingApp(root)
            root.mainloop()
