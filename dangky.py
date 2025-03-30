from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import pymysql
import re

def login_page():
    signup_window.destroy()
    import dangnhap

def is_valid_email(email):
    # Biểu thức chính quy để kiểm tra địa chỉ email
    email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{3}$')

    # Kiểm tra địa chỉ email với biểu thức chính quy
    if re.match(email_pattern, email):
        return True
    else:
        return False

def clear():
    emailEntry.delete(0, END)
    usernameEntry.delete(0, END)
    passwordEntry.delete(0, END)
    confirmEntry.delete(0, END)
    check.set(0)

def connect_database():
    if emailEntry.get() == '' or usernameEntry.get() == '' or passwordEntry.get() == '' or confirmEntry.get() == '':
        messagebox.showerror('Error', 'All Fields Are Required')
    elif not is_valid_email(emailEntry.get()):
        messagebox.showerror('Error', 'Invalid Email Address')
    elif passwordEntry.get() != confirmEntry.get():
        messagebox.showerror('Error', 'Password Mismatch')
    elif check.get() == 0:
        messagebox.showerror('Error', 'Please Accept Terms & Conditions')
    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='123456789')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Database Connectivity Issue, Please Try Again')
            return
        try:
            query = 'create database userdata'
            mycursor.execute(query)
            query = 'use userdata'
            mycursor.execute(query)
            query = 'create table data(id int auto_increment primary key not null, email varchar(50), username varchar(100), password varchar(20))'
            mycursor.execute(query)
        except:
            mycursor.execute('use userdata')

        query = 'select * from data where username=%s'
        mycursor.execute(query, (usernameEntry.get()))

        query = 'ALTER TABLE data AUTO_INCREMENT = 1'
        mycursor.execute(query)

        row = mycursor.fetchone()
        if row != None:
            messagebox.showerror('Error', 'Username Already Exists')
        else:
            query = 'insert into data(email, username, password) values(%s, %s, %s)'
            mycursor.execute(query, (emailEntry.get(), usernameEntry.get(), passwordEntry.get()))
            con.commit()
            con.close()
            messagebox.showinfo('Success', 'Registration Is Successful')
            clear()
            signup_window.destroy()
            import dangnhap

signup_window = Tk()
signup_window.title('Trang Đăng Ký')
signup_window.resizable(False, False)
background = ImageTk.PhotoImage(file="bg.jpg")

bgLabel = Label(signup_window, image=background)
bgLabel.grid()

frame = Frame(signup_window, bg='white')
frame.place(x=554, y=100)

heading = Label(frame, text='CREATE AN ACCOUNT', font=('Microsoft Yahei UI Light', 18, 'bold'), bg='white',
                fg='firebrick1')
heading.grid(row=0, column=0, padx=10, pady=10)

emailLabel = Label(frame, text='Email', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='white',
                fg='firebrick1')
emailLabel.grid(row=1, column=0, padx=25, sticky='w', pady=(10, 0))

emailEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 10, 'bold'), bg='firebrick1',
                fg='white')
emailEntry.grid(row=2, column=0, padx=27, sticky='w')

usernameLabel = Label(frame, text='Username', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='white',
                fg='firebrick1')
usernameLabel.grid(row=3, column=0, padx=25, sticky='w', pady=(10, 0))

usernameEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 10, 'bold'), bg='firebrick1',
                fg='white')
usernameEntry.grid(row=4, column=0, padx=27, sticky='w')

passwordLabel = Label(frame, text='Password', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='white',
                fg='firebrick1')
passwordLabel.grid(row=5, column=0, padx=25, sticky='w', pady=(10, 0))

passwordEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 10, 'bold'), bg='firebrick1',
                fg='white')
passwordEntry.grid(row=6, column=0, padx=27, sticky='w')

confirmLabel = Label(frame, text='Confirm Password', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='white',
                fg='firebrick1')
confirmLabel.grid(row=7, column=0, padx=25, sticky='w', pady=(10, 0))

confirmEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 10, 'bold'), bg='firebrick1',
                fg='white')
confirmEntry.grid(row=8, column=0, padx=27, sticky='w')

check = IntVar()

termsandconditions = Checkbutton(frame, text='I agree to the Terms & Conditions', font=('Microsoft Yahei UI Light', 9, 'bold'),
                                 fg='firebrick1', bg='white', activebackground='white', activeforeground='firebrick1', cursor='hand2', variable=check)
termsandconditions.grid(row=9, column=0, padx=15, pady=10)

signupButton = Button(frame, text='Signup', font=('Open Sans', 16, 'bold'), bd=0, bg='firebrick1', cursor='hand2',
                fg='white', activebackground='firebrick1', activeforeground='white', width=17, command=connect_database)
signupButton.grid(row=10, column=0, pady=10)

alreadyaccount = Label(frame, text="Don't have an account?", font=('Open Sans', 9, 'bold'), fg='firebrick1', bg='white')
alreadyaccount.grid(row=11, column=0, padx=55, pady=10, sticky='w')

loginButton = Button(frame, text='Log in', bd=0, fg='blue', activebackground='white', cursor='hand2',
                    font=('Open Sans', 9, 'bold underline'), bg='white', activeforeground='blue', command=login_page)
loginButton.place(x=195, y=404)

signup_window.mainloop()
