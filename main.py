import json
from tkinter import *
from tkinter import messagebox
import random
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    entry_password.delete(0, END)
    letters = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
        'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
        'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for _ in range(nr_letters)] + \
                    [random.choice(symbols) for _ in range(nr_symbols)] + \
                    [random.choice(numbers) for _ in range(nr_numbers)]
    random.shuffle(password_list)
    password = "".join(password_list)
    pyperclip.copy(password)
    entry_password.insert(END, string=password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website_txt = entry_website.get()
    email_txt = entry_email.get()
    password_txt = entry_password.get()
    new_data = {
        website_txt: {
            'Email': email_txt,
            'Password': password_txt
        }
    }

    if len(entry_website.get()) == 0 or len(entry_password.get()) == 0:
        messagebox.showinfo(title='Empty fields.', message="Please fill in required details.")
    else:
        try:
            with open('data.json') as file:
                data = json.load(file)
        except FileNotFoundError:
            is_ok = messagebox.askyesno(title='Confirm Data Entry?', message=f'Check details:\nWebsite: {website_txt}'
                                                                             f'\nEmail: {email_txt}\nPassword:'
                                                                             f' {password_txt}')
            if is_ok:
                with open('data.json', 'w') as file:
                    json.dump(new_data, file, indent=4)
        else:
            is_ok = messagebox.askyesno(title='Confirm Data Entry?', message=f'Check details:\nWebsite: {website_txt}'
                                                                             f'\nEmail: {email_txt}\nPassword: '
                                                                             f'{password_txt}')
            if is_ok:
                data.update(new_data)
                with open('data.json', 'w') as file:
                    json.dump(data, file, indent=4)

        finally:
            entry_email.delete(0, END)
            entry_password.delete(0, END)


# ---------------------------- SEARCH DETAILS ------------------------- #


def find_password():
    website = entry_website.get()
    if len(website) == 0:
        messagebox.showinfo(title='Incomplete Details', message="Fill in the website name.")
    else:
        try:
            open('data.json', 'r')
        except FileNotFoundError:
            messagebox.showinfo(title='Error 404', message='Data File Not Found')
        else:
            with open('data.json', 'r') as file:
                data = json.load(file)
                try:
                    data[website]
                except KeyError:
                    messagebox.showinfo(title='Error 404', message='Data Not Found')
                else:
                    email = data[website]['Email']
                    password = data[website]['Password']
                    messagebox.showinfo(title='Search Results', message=f'Website: {website}\nEmail: {email}\nPassword:'
                                                                        f' {password}')


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.config(padx=20, pady=20, highlightthickness=0)
window.title(string='Password Manager')

canvas = Canvas()
canvas.config(height=200, width=190)
image_url = PhotoImage(file='logo.png')
canvas.create_image(100, 95, image=image_url)
canvas.grid(row=0, column=0, columnspan=3)

label_website = Label(text="Website: ")
label_website.grid(row=1, column=0, sticky=W)
label_email = Label(text="Email/Username: ")
label_email.grid(row=2, column=0, sticky=W)
label_password = Label(text="Password: ")
label_password.grid(row=3, column=0, sticky=W)

entry_website = Entry(width=21)
entry_website.grid(row=1, column=1, columnspan=1, sticky=W)
entry_website.focus()
entry_email = Entry(width=39)
entry_email.grid(row=2, column=1, columnspan=2, sticky=W)
entry_email.insert(END, string='someone@example.com')
entry_password = Entry(width=21)
entry_password.grid(row=3, column=1, sticky=W)

generate_btn = Button(text='Generate Password', width=14, command=generate_password)
generate_btn.grid(row=3, column=2, sticky=W)
add_btn = Button(text='Add', width=33, command=save)
add_btn.grid(row=4, column=1, columnspan=2, sticky=W)
search_btn = Button(text='Search', width=14, command=find_password)
search_btn.grid(row=1, column=2, sticky=W)

window.mainloop()
