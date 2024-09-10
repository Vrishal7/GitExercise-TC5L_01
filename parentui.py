import tkinter as tk
from tkinter import simpledialog, messagebox
import json
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

# Function to register a child and save credentials
def open_register_menu():
    register_menu = tk.Toplevel(root)
    register_menu.title("Parent Registration")

    tk.Label(register_menu, text="Parent Registration", font=("Arial", 18)).pack(pady=20)

    tk.Label(register_menu, text="Child's Name:", font=("Arial", 14)).pack(pady=5)
    child_name_entry = tk.Entry(register_menu, font=("Arial", 14))
    child_name_entry.pack(pady=5)

    tk.Label(register_menu, text="Username:", font=("Arial", 14)).pack(pady=5)
    username_entry = tk.Entry(register_menu, font=("Arial", 14))
    username_entry.pack(pady=5)

    tk.Label(register_menu, text="Password:", font=("Arial", 14)).pack(pady=5)
    password_entry = tk.Entry(register_menu, font=("Arial", 14), show="*")
    password_entry.pack(pady=5)

    def save_credentials():
        child_name = child_name_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        if not child_name or not username or not password:
            messagebox.showerror("Invalid Input", "All fields are required!")
            return

        credentials = {"child_name": child_name, "username": username, "password": password}

        # Save credentials to a JSON file
        file_path = "credentials.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                data = json.load(file)
        else:
            data = []

        data.append(credentials)

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

        messagebox.showinfo("Registration Successful", "Child registered successfully!")

    tk.Button(register_menu, text="Register", font=("Arial", 14), command=save_credentials).pack(pady=10)

# Main window
root = tk.Tk()
root.title("Children's Drawing & Timer UI")
root.geometry("800x600")  # Set a suitable size for your window

# Load background image
bg_image_path = "C:/Users/User/Desktop/parent ui/background.jpg"  # Replace with the correct path to your background image
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

# Register Button for Parent Registration
register_button = tk.Button(root, text="Register Child", font=("Arial", 16), command=open_register_menu)
register_button.place(relx=0.5, rely=0.6, anchor="center")

# Start the main event loop
root.mainloop()
