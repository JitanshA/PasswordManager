
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
symbols = ['!', '@', '#', '$', '%', '^', '&', '*']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7']


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 5))]
    password_numbers = [choice(numbers) for _ in range(randint(5, 8))]
    password_list = password_numbers + password_symbols + password_letters
    shuffle(password_list)
    random_password = "".join(password_list)

    password_input.insert(END, random_password)
    pyperclip.copy(random_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_password():
    password_to_save = password_input.get()
    website_to_save = website_input.get()
    email_to_save = email_input.get()
    new_data = {
        website_to_save: {
            "email": email_to_save,
            "password": password_to_save
        }
    }

    if password_to_save == "" or website_to_save == "" or email_to_save == "":
        messagebox.showinfo(message="Please don't leave any fields empty!")
    else:
        try:
            with open("passwords.json", "r") as password_file:
                data = json.load(password_file)
        except FileNotFoundError:
            with open("passwords.json", "w") as password_file:
                json.dump(new_data, password_file, indent=4)
        else:
            data.update(new_data)
            with open("passwords.json", "w") as password_file:
                json.dump(data, password_file, indent=4)
        finally:
            password_input.delete(0, END)
            website_input.delete(0, END)


# ------------------------- SEARCH PASSWORD ---------------------------#

def search_data():
    website_entered = website_input.get()
    try:
        with open("passwords.json", "r") as password_file:
            data = json.load(password_file)
    except FileNotFoundError:
        messagebox.showinfo(message="There are no saved passwords")
    else:
        if website_entered in data:
            email = data[website_entered]["email"]
            password = data[website_entered]["password"]
            messagebox.showinfo(title=website_entered, message=f"E-mail: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="No such Password", message="Password not in the saved list")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(pady=40, padx=40)

canvas = Canvas(height=200, width=200)
lock_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_image)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

website_input = Entry(width=21)
website_input.focus()
website_input.grid(row=1, column=1)

email_input = Entry(width=39)
email_input.insert(END, "pythontest764@gmail.com")
email_input.grid(row=2, column=1, columnspan=2)

password_input = Entry(width=21)
password_input.grid(row=3, column=1)

generate_button = Button(text="Generate Password", command=generate_password, width=16)
generate_button.grid(row=3, column=2)

add_button = Button(text="Add", width=37, command=save_password)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", width=16, command=search_data)
search_button.grid(row=1, column=2)

window.mainloop()
