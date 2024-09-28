import tkinter as tk
from tkinter import simpledialog, messagebox, Scrollbar, Canvas
from PIL import Image, ImageTk
import os

# Function to open the Children's Drawing Menu and show .png images
def open_drawing_menu():
    drawing_menu = tk.Toplevel(root)
    drawing_menu.title("Children's Drawing Menu")
    
    # Add a canvas to allow scrolling if there are many images
    canvas = Canvas(drawing_menu)
    scrollbar = Scrollbar(drawing_menu, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Layout canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Path to the directory with images
    image_folder = "C:/Users/user/Pictures"  # Adjust this path to your pictures folder

    # Loop through all png files in the directory
    images = [f for f in os.listdir(image_folder) if f.endswith(".png")]
    
    if images:
        for img_file in images:
            img_path = os.path.join(image_folder, img_file)
            try:
                # Open the image and resize it to fit in the window
                img = Image.open(img_path)
                img = img.resize((200, 200), Image.Resampling.LANCZOS)
                img_photo = ImageTk.PhotoImage(img)
                
                # Create a label for each image and display it in the scrollable frame
                img_label = tk.Label(scrollable_frame, image=img_photo)
                img_label.image = img_photo  # Keep a reference to avoid garbage collection
                img_label.pack(pady=10)
                
                # Add a label with the file name
                tk.Label(scrollable_frame, text=img_file, font=("Arial", 12)).pack(pady=5)
                
            except Exception as e:
                messagebox.showerror("Error", f"Unable to open image {img_file}. Error: {str(e)}")
    else:
        tk.Label(scrollable_frame, text="No PNG images found.", font=("Arial", 14)).pack(pady=20)

# Main window
root = tk.Tk()
root.title("Children's Drawing & Timer UI")
root.geometry("800x600")  # Set a suitable size for your window

# Load background image
bg_image_path = "C:/Users/User/Desktop/Minni it/GitExercise-TC5L_01/GitExercise-TC5L_01/parent ui/background.jpg"  # Replace with the correct path to your background image
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
