import string
import random
from tkinter import *
from tkinter import messagebox
import sqlite3

class GUI():
    def __init__(self, master):
        self.master = master
        self.username = StringVar()
        self.passwordlen = IntVar()
        self.generatedpassword = StringVar()
        self.n_username = StringVar()
        self.n_generatedpassword = StringVar()
        self.n_passwordlen = IntVar()

        root.title('Password Generator')
        root.geometry('660x500')
        root.config(bg='#FF8000')
        root.resizable(False, False)

        self.label = Label(text=":PASSWORD GENERATOR:", anchor=N, fg='darkblue', bg='#FF8000', font='arial 20 bold underline')
        self.label.grid(row=0, column=1)

        # Labels and Entry fields for username, password length, and generated password
        Label(text="Enter User Name: ", font='times 15 bold', bg='#FF8000', fg='darkblue').grid(row=4, column=0)
        self.textfield = Entry(textvariable=self.n_username, font='times 15', bd=6, relief='ridge')
        self.textfield.grid(row=4, column=1)
        self.textfield.focus_set()

        Label(text="Enter Password Length: ", font='times 15 bold', bg='#FF8000', fg='darkblue').grid(row=6, column=0)
        self.length_textfield = Entry(textvariable=self.n_passwordlen, font='times 15', bd=6, relief='ridge')
        self.length_textfield.grid(row=6, column=1)

        Label(text="Generated Password: ", font='times 15 bold', bg='#FF8000', fg='darkblue').grid(row=8, column=0)
        self.generated_password_textfield = Entry(textvariable=self.n_generatedpassword, font='times 15', bd=6, relief='ridge', fg='#DC143C')
        self.generated_password_textfield.grid(row=8, column=1)

        # Buttons for generate password, accept fields, and reset fields
        Button(text="GENERATE PASSWORD", bd=3, relief='solid', padx=1, pady=1, font='Verdana 15 bold', fg='#68228B', bg='#BCEE68', command=self.generate_pass).grid(row=11, column=1)
        Button(text="ACCEPT", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='#458B00', bg='#FFFAF0', command=self.accept_fields).grid(row=13, column=1)
        Button(text="RESET", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='#458B00', bg='#FFFAF0', command=self.reset_fields).grid(row=15, column=1)

        # Initialize SQLite database
        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS users(Username TEXT NOT NULL, GeneratedPassword TEXT NOT NULL);")
            db.commit()

    def generate_pass(self):
        upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lower = "abcdefghijklmnopqrstuvwxyz"
        chars = "@#%&()\"?!"
        numbers = "1234567890"

        upper = list(upper)
        lower = list(lower)
        chars = list(chars)
        numbers = list(numbers)

        name = self.textfield.get()
        length = self.n_passwordlen.get()

        if name == "":
            messagebox.showerror("Error", "Name cannot be empty")
            return

        if not name.isalpha():
            messagebox.showerror("Error", "Name must be alphabetic")
            self.textfield.delete(0, END)
            return

        if length < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            self.length_textfield.delete(0, END)
            return

        u = random.randint(1, length - 3)
        l = random.randint(1, length - 2 - u)
        c = random.randint(1, length - 1 - u - l)
        n = length - u - l - c

        password = random.sample(upper, u) + random.sample(lower, l) + random.sample(chars, c) + random.sample(numbers, n)
        random.shuffle(password)
        gen_passwd = "".join(password)

        self.n_generatedpassword.set(gen_passwd)

    def accept_fields(self):
        username = self.n_username.get()
        generated_password = self.n_generatedpassword.get()

        if username == "":
            messagebox.showerror("Error", "Username cannot be empty")
            return

        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            find_user = "SELECT * FROM users WHERE Username = ?"
            cursor.execute(find_user, (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists! Please use another username.")
            else:
                insert_query = "INSERT INTO users (Username, GeneratedPassword) VALUES (?, ?)"
                cursor.execute(insert_query, (username, generated_password))
                db.commit()
                messagebox.showinfo("Success", "Password generated and stored successfully!")

    def reset_fields(self):
        self.textfield.delete(0, END)
        self.length_textfield.delete(0, END)
        self.generated_password_textfield.delete(0, END)


if __name__ == '__main__':
    root = Tk()
    pass_gen = GUI(root)
    root.mainloop()
