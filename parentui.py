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

# Function to open the Timer Menu and customize the timer
def open_timer_menu():
    timer_menu = tk.Toplevel(root)
    timer_menu.title("Timer Customization Menu")

    tk.Label(timer_menu, text="Set Timer (in seconds):", font=("Arial", 14)).pack(pady=10)
    timer_entry = tk.Entry(timer_menu, font=("Arial", 14))
    timer_entry.pack(pady=5)

    def set_timer():
        try:
            global time_left
            time_left = int(timer_entry.get())
            messagebox.showinfo("Timer Set", f"Timer set to {time_left} seconds")
            update_timer()  # Start the timer immediately after setting it
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")

    tk.Button(timer_menu, text="Set Timer", font=("Arial", 14), command=set_timer).pack(pady=10)

# Function to update the timer
def update_timer():
    global time_left
    if time_left > 0:
        time_left -= 1
        timer_label.config(text=f"Time Left: {time_left}s")
        root.after(1000, update_timer)
    elif time_left == 0:
        messagebox.showinfo("Time's up!", "The timer has finished.")
        time_left = None

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

# Initialize Timer
time_left = None  # Timer starts uninitialized

# Timer Label (display timer at the top right)
timer_label = tk.Label(root, text="Time Left: None", font=("Arial", 16), bg="#ffffff")
timer_label.place(x=700, y=10)

# Children's Drawing Button
drawing_button = tk.Button(root, text="Children's Drawing", font=("Arial", 16), command=open_drawing_menu)
drawing_button.place(relx=0.5, rely=0.4, anchor="center")

# Timer Button
timer_button = tk.Button(root, text="Timer", font=("Arial", 16), command=open_timer_menu)
timer_button.place(relx=0.5, rely=0.5, anchor="center")

# Start the main event loop
root.mainloop()
