import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Importing Image and ImageTk from PIL for handling JPG images

# Function to handle the "Drawings" button
def open_drawings():
    messagebox.showinfo("Drawings", "This will open the drawings section.")

# Function to handle the "Shop" button
def open_shop():
    messagebox.showinfo("Shop", "This will open the shop section.")

# Function to update the timer
def update_timer():
    global time_left
    if time_left > 0:
        time_left -= 1
        timer_label.config(text=f"Time Left: {time_left}s")
        root.after(1000, update_timer)
    else:
        messagebox.showinfo("Time's up!", "The timer has finished.")

# Main window
root = tk.Tk()
root.title("User Interface with Drawings, Shop, Coins, and Timer")

# Set the window size to match the background image
root.geometry("800x600")  # You can adjust this size based on your background image dimensions

# Load background image
bg_image_path = "C:/Users/User/Desktop/ui/background.jpg"  # Replace with the correct path to your background image
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((1720, 1080), Image.Resampling.LANCZOS)  # Resize the image to fit the window
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label to hold the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Cover the entire window with the background image

# Coins Display
coins = 100
coins_label = tk.Label(root, text=f"Coins: {coins}", font=("Arial", 16), bg="#ffffff")
coins_label.place(x=10, y=10)  # Place in the top left corner

# Timer Display
time_left = 60  # Set initial time (in seconds)
timer_label = tk.Label(root, text=f"Time Left: {time_left}s", font=("Arial", 16), bg="#ffffff")
timer_label.place(x=700, y=10)  # Place in the top right corner (adjust x value based on window size)

# Start the timer
root.after(10000, update_timer)

# Drawings Button
drawings_button = tk.Button(root, text="Drawings", font=("Arial", 16), command=open_drawings)
drawings_button.place(relx=0.5, rely=0.5, anchor="center")  # Place in the center

# Shop Button
shop_button = tk.Button(root, text="Shop", font=("Arial", 16), command=open_shop)
shop_button.place(relx=0.5, rely=0.6, anchor="center")  # Place slightly below the drawings button

# Start the main event loop
root.mainloop()
