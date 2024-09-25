import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import json
import os
import subprocess

# Function to handle login
def login():
    username = entry_username.get()
    password = entry_password.get()

    # Check if username is "Parents" and password is "Parent12345"
    if username == "Parents" and password == "Parent12345":
        root.destroy()  # Close the current window
        # Open the parentui.py script
        subprocess.run(["python", "parentui.py"])  # Runs the parentui.py file
        return

    # Load credentials from JSON file for other users
    file_path = "credentials.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            users = json.load(file)
    else:
        users = []

    # Check if the entered credentials match any saved users
    for user in users:
        if user["username"] == username and user["password"] == password:
            root.destroy()  # Close the current window
            # Open the main.py script after successful login
            subprocess.run(["python", "main.py"])  # Runs the main.py file
            return

    messagebox.showerror("Login Failed", "Invalid Username or Password")

# Function to exit the app
def exit_app():
    root.quit()

# Function to register a new parent
def open_register():
    login_frame.pack_forget()
    register_frame.pack(pady=20)

def register_user():
    username = entry_reg_username.get()
    password = entry_reg_password.get()

    if not username or not password:
        messagebox.showerror("Registration Failed", "All fields are required!")
        return

    new_user = {"username": username, "password": password}

    # Save the credentials to a JSON file
    file_path = "credentials.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            users = json.load(file)
    else:
        users = []

    # Check if the username already exists
    for user in users:
        if user["username"] == username:
            messagebox.showerror("Registration Failed", "Username already exists!")
            return

    users.append(new_user)

    with open(file_path, "w") as file:
        json.dump(users, file, indent=4)

    messagebox.showinfo("Registration Success", "Parent registered successfully!")
    register_frame.pack_forget()
    login_frame.pack(pady=20)

# Main window
root = tk.Tk()
root.title("Kids Drawing App")
root.geometry("500x400")  # Set a suitable size for the window

# Login Frame
login_frame = tk.Frame(root)
login_frame.pack(pady=20)

# Add Logo Image with Error Handling and Centering
try:
    logo_image = PhotoImage(file="C:/Users/User/Desktop/Minni it/GitExercise-TC5L_01/GitExercise-TC5L_01/login ui/drawinglogo.png")  # Update the path to your image
except Exception as e:
    print("Error loading logo image:", e)
    logo_image = None  # Set to None if the image can't be loaded

if logo_image:
    logo_label = tk.Label(login_frame, image=logo_image)
    logo_label.grid(row=0, column=0, columnspan=2, pady=10)

# Username and Password Labels and Entries
font_settings = ("Arial", 14)

tk.Label(login_frame, text="Username:", font=font_settings).grid(row=1, column=0, pady=5)
entry_username = tk.Entry(login_frame, font=font_settings)
entry_username.grid(row=1, column=1, pady=5)

tk.Label(login_frame, text="Password:", font=font_settings).grid(row=2, column=0, pady=5)
entry_password = tk.Entry(login_frame, show="*", font=font_settings)
entry_password.grid(row=2, column=1, pady=5)

# Login and Register Buttons
tk.Button(login_frame, text="Login", command=login, font=font_settings).grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(login_frame, text="Register", command=open_register, font=font_settings).grid(row=4, column=0, columnspan=2, pady=5)

# Exit Button
tk.Button(login_frame, text="Exit", command=exit_app, font=font_settings).grid(row=5, column=0, columnspan=2, pady=5)

# Registration Frame
register_frame = tk.Frame(root)

tk.Label(register_frame, text="Register", font=("Arial", 18)).pack(pady=10)

tk.Label(register_frame, text="Username:", font=font_settings).pack(pady=5)
entry_reg_username = tk.Entry(register_frame, font=font_settings)
entry_reg_username.pack(pady=5)

tk.Label(register_frame, text="Password:", font=font_settings).pack(pady=5)
entry_reg_password = tk.Entry(register_frame, show="*", font=font_settings)
entry_reg_password.pack(pady=5)

tk.Button(register_frame, text="Register", command=register_user, font=font_settings).pack(pady=10)

tk.Button(register_frame, text="Back to Login", command=lambda: [register_frame.pack_forget(), login_frame.pack(pady=20)], font=font_settings).pack(pady=5)

root.mainloop()