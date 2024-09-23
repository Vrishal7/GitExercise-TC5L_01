import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import json
import os

# Function to handle login
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    # Load credentials from JSON file
    file_path = "credentials.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            users = json.load(file)
    else:
        users = []

    # Check if the entered credentials match any saved users
    for user in users:
        if user["username"] == username and user["password"] == password:
            login_frame.pack_forget()
            drawing_frame.pack(fill="both", expand=True)
            return

    messagebox.showerror("Login Failed", "Invalid Username or Password")

# Function to exit the app
def exit_app():
    root.quit()

# Function to draw on canvas
def paint(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    canvas.create_oval(x1, y1, x2, y2, fill="black", width=5)

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
    logo_image = PhotoImage(file="C:/Users/User/Desktop/login UI/drawinglogo.png")  # Update the path to your image
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

# Drawing Frame
drawing_frame = tk.Frame(root)

canvas = tk.Canvas(drawing_frame, bg="white", width=500, height=400)
canvas.pack(expand=True)

canvas.bind("<B1-Motion>", paint)

tk.Button(drawing_frame, text="Exit", command=exit_app, font=font_settings).pack(pady=10)

root.mainloop()