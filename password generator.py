import string
import secrets
import tkinter as tk
from tkinter import ttk, messagebox


# =========================
# PASSWORD GENERATOR
# =========================

def generate_password(length, use_numbers, use_symbols):
    characters = string.ascii_letters

    if use_numbers:
        characters += string.digits

    if use_symbols:
        characters += string.punctuation

    return ''.join(
        secrets.choice(characters)
        for _ in range(length)
    )


# =========================
# PASSWORD STRENGTH
# =========================

def check_strength(password):
    score = 0

    if len(password) >= 12:
        score += 1

    if any(char.isupper() for char in password):
        score += 1

    if any(char.islower() for char in password):
        score += 1

    if any(char.isdigit() for char in password):
        score += 1

    if any(char in string.punctuation for char in password):
        score += 1

    if score >= 4:
        return "STRONG", 100

    elif score >= 3:
        return "MEDIUM", 65

    else:
        return "WEAK", 35


# =========================
# COPY PASSWORD
# =========================

def copy_password(password):
    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()

    status_label.config(
        text="✓ Password copied to clipboard"
    )


# =========================
# SHOW / HIDE PASSWORD
# =========================

def toggle_passwords():
    global passwords_visible

    passwords_visible = not passwords_visible

    if passwords_visible:
        show_button.config(text="Hide Passwords")
    else:
        show_button.config(text="Show Passwords")

    display_passwords()


# =========================
# DISPLAY PASSWORDS
# =========================

def display_passwords():
    for widget in results_frame.winfo_children():
        widget.destroy()

    for index, password in enumerate(generated_passwords):

        if passwords_visible:
            displayed_password = password
        else:
            displayed_password = "•" * len(password)

        strength, value = check_strength(password)

        password_label = ttk.Label(
            results_frame,
            text=f"{index + 1}. {displayed_password}",
            font=("Segoe UI", 11)
        )

        password_label.grid(
            row=index,
            column=0,
            padx=10,
            pady=8,
            sticky="w"
        )

        strength_label = ttk.Label(
            results_frame,
            text=strength
        )

        strength_label.grid(
            row=index,
            column=1,
            padx=10
        )

        copy_button = ttk.Button(
            results_frame,
            text="Copy",
            command=lambda p=password: copy_password(p)
        )

        copy_button.grid(
            row=index,
            column=2,
            padx=10
        )


# =========================
# GENERATE PASSWORDS
# =========================

def generate_passwords():

    global generated_passwords

    try:
        length = int(length_entry.get())
        count = int(count_entry.get())

    except ValueError:

        messagebox.showerror(
            "Invalid Input",
            "Please numbers enter karo."
        )

        return

    if length < 8:

        messagebox.showerror(
            "Invalid Length",
            "Password minimum 8 characters ka hona chahiye."
        )

        return

    if count < 1 or count > 20:

        messagebox.showerror(
            "Invalid Number",
            "1 se 20 passwords generate kar sakte ho."
        )

        return

    use_numbers = numbers_var.get()
    use_symbols = symbols_var.get()

    generated_passwords = []

    for _ in range(count):

        password = generate_password(
            length,
            use_numbers,
            use_symbols
        )

        generated_passwords.append(password)

    display_passwords()

    status_label.config(
        text=f"✓ {count} password(s) generated successfully"
    )


# =========================
# CLEAR
# =========================

def clear_passwords():

    global generated_passwords

    generated_passwords = []

    for widget in results_frame.winfo_children():
        widget.destroy()

    status_label.config(
        text="Ready to generate passwords"
    )


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()

root.title("Password Generator")
root.geometry("720x620")

root.minsize(650, 550)


# =========================
# STYLE
# =========================

style = ttk.Style()

try:
    style.theme_use("clam")
except:
    pass


# =========================
# VARIABLES
# =========================

numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

passwords_visible = True

generated_passwords = []


# =========================
# TITLE
# =========================

title_label = ttk.Label(
    root,
    text="🔐 PASSWORD GENERATOR",
    font=("Segoe UI", 24, "bold")
)

title_label.pack(pady=(25, 5))


subtitle_label = ttk.Label(
    root,
    text="Generate secure passwords instantly",
    font=("Segoe UI", 11)
)

subtitle_label.pack(
    pady=(0, 20)
)


# =========================
# SETTINGS FRAME
# =========================

settings_frame = ttk.Frame(root)

settings_frame.pack(
    padx=30,
    fill="x"
)


# Password length

ttk.Label(
    settings_frame,
    text="Password Length"
).grid(
    row=0,
    column=0,
    padx=10,
    pady=10
)

length_entry = ttk.Entry(
    settings_frame,
    width=15
)

length_entry.grid(
    row=0,
    column=1,
    padx=10
)

length_entry.insert(
    0,
    "12"
)


# Number of passwords

ttk.Label(
    settings_frame,
    text="Number of Passwords"
).grid(
    row=1,
    column=0,
    padx=10,
    pady=10
)

count_entry = ttk.Entry(
    settings_frame,
    width=15
)

count_entry.grid(
    row=1,
    column=1,
    padx=10
)

count_entry.insert(
    0,
    "5"
)


# =========================
# OPTIONS
# =========================

options_frame = ttk.Frame(root)

options_frame.pack(
    pady=15
)


ttk.Checkbutton(
    options_frame,
    text="Include Numbers",
    variable=numbers_var
).grid(
    row=0,
    column=0,
    padx=15
)


ttk.Checkbutton(
    options_frame,
    text="Include Symbols",
    variable=symbols_var
).grid(
    row=0,
    column=1,
    padx=15
)


# =========================
# BUTTONS
# =========================

button_frame = ttk.Frame(root)

button_frame.pack(
    pady=10
)


ttk.Button(
    button_frame,
    text="🔄 Generate Passwords",
    command=generate_passwords
).grid(
    row=0,
    column=0,
    padx=5
)


show_button = ttk.Button(
    button_frame,
    text="Hide Passwords",
    command=toggle_passwords
)

show_button.grid(
    row=0,
    column=1,
    padx=5
)


ttk.Button(
    button_frame,
    text="🧹 Clear",
    command=clear_passwords
).grid(
    row=0,
    column=2,
    padx=5
)


# =========================
# RESULTS
# =========================

ttk.Label(
    root,
    text="Generated Passwords",
    font=("Segoe UI", 13, "bold")
).pack(
    pady=(20, 8)
)


results_frame = ttk.Frame(
    root,
    relief="solid",
    borderwidth=1
)

results_frame.pack(
    padx=30,
    fill="both",
    expand=True
)


# =========================
# STATUS
# =========================

status_label = ttk.Label(
    root,
    text="Ready to generate passwords"
)

status_label.pack(
    pady=15
)


# =========================
# START APP
# =========================

root.mainloop()