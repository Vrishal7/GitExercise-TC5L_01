import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk  # Importing for handling images (optional if using a background)
import os

# Function to open the Children's Drawing Menu
def open_drawing_menu():
    drawing_menu = tk.Toplevel(root)
    drawing_menu.title("Children's Drawing Menu")

    # Add widgets related to drawing features here
    tk.Label(drawing_menu, text="Children's Drawing Menu", font=("Arial", 18)).pack(pady=20)
    tk.Button(drawing_menu, text="Start Drawing", font=("Arial", 14), command=lambda: messagebox.showinfo("Drawing", "Starting Drawing")).pack(pady=10)



# Main window
root = tk.Tk()
root.title("Children's Drawing & Timer UI")
root.geometry("800x600")  # Set a suitable size for your window

# Load background image
bg_image_path = "C:/Users/Acer/Desktop/Drawin App/parent ui/background.jpg"  # Replace with the correct path to your background image
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((1800, 980), Image.Resampling.LANCZOS)  # Resize the image to fit the window
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label to hold the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Cover the entire window with the background image


# Children's Drawing Button
drawing_button = tk.Button(root, text="Children's Drawing", font=("Arial", 16), command=open_drawing_menu)
drawing_button.place(relx=0.5, rely=0.4, anchor="center")


# Start the main event loop
root.mainloop()
