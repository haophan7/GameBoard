from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import pymysql

def username_enter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)

def password_enter(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, END)

def hide():
    openeye.config(file='closeye.png')
    passwordEntry.config(show='*')
    eyeButton.config(command=show)

def show():
    openeye.config(file='openeye.png')
    passwordEntry.config(show='')
    eyeButton.config(command=hide)

def signup_page():
    login_window.destroy()
    import dangky

def login_user():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'All Fields Are Required')
    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='123456789')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Connection is not established try again')
            return
        query = 'use userdata'
        mycursor.execute(query)
        query = 'select * from data where username=%s and password=%s'
        mycursor.execute(query, (usernameEntry.get(), passwordEntry.get()))
        row = mycursor.fetchone()
        if row == None:
            messagebox.showerror('Error', 'Invalid Username Or Password')
        else:
            messagebox.showinfo('Welcome', 'Login Is Successful')
            login_window.destroy()
            import trochoicoban

def forget_pass():
    def change_password():
        if usernameEntry.get() == '' or newpassEntry.get() == '' or confirmEntry.get() == '':
            messagebox.showerror('Error', 'All Fields Are Required', parent=window)
        elif newpassEntry.get() != confirmEntry.get():
            messagebox.showerror('Error', 'Password And Confirm Password Are Not Matching', parent=window)
        else:
            con = pymysql.connect(host='localhost', user='root', password='123456789', database='userdata')
            mycursor = con.cursor()
            query = 'select * from data where username=%s'
            mycursor.execute(query, (usernameEntry.get()))
            row = mycursor.fetchone()
            if row == None:
                messagebox.showerror('Error', 'Incorrect Username', parent=window)
            else:
                query = 'update data set password=%s where username=%s'
                mycursor.execute(query, (newpassEntry.get(), usernameEntry.get()))
                con.commit()
                con.close()
                messagebox.showinfo('Success', 'Password Is Reset, Please Login With New Password', parent=window)
                window.destroy()
    window = Toplevel()
    window.resizable(False, False)
    window.title('Trang Thay Đổi Mật Khẩu')

    bgPic = ImageTk.PhotoImage(file='background.jpg')
    bgLabel = Label(window, image=bgPic)
    bgLabel.grid()

    heading_label = Label(window, text='RESET PASSWORD', font=('arial', 18, 'bold'), bg='white', fg='magenta2')
    heading_label.place(x=480, y=60)

    usernameLabel = Label(window, text='Username', font=('arial', 12, 'bold'), bg='white', fg='orchid1')
    usernameLabel.place(x=470, y=130)
    usernameEntry = Entry(window, width=25, font=('arial', 11, 'bold'), bd=0, fg='magenta2')
    usernameEntry.place(x=470, y=160)

    Frame(window, width=250, height=2, bg='orchid1').place(x=470, y=180)

    passwordLabel = Label(window, text='New Password', font=('arial', 12, 'bold'), bg='white', fg='orchid1')
    passwordLabel.place(x=470, y=210)
    newpassEntry = Entry(window, width=25, font=('arial', 11, 'bold'), bd=0, fg='magenta2')
    newpassEntry.place(x=470, y=240)

    Frame(window, width=250, height=2, bg='orchid1').place(x=470, y=260)

    confirmLabel = Label(window, text='Confirm Password', font=('arial', 12, 'bold'), bg='white', fg='orchid1')
    confirmLabel.place(x=470, y=290)
    confirmEntry = Entry(window, width=25, font=('arial', 11, 'bold'), bd=0, fg='magenta2')
    confirmEntry.place(x=470, y=320)

    Frame(window, width=250, height=2, bg='orchid1').place(x=470, y=340)

    submitButton = Button(window, text='Submit', bd=0, width=19, fg='white', activebackground='magenta2', cursor='hand2',
                         font=('Open Sans', 16, 'bold'), bg='magenta2', activeforeground='white', command=change_password)
    submitButton.place(x=470, y=390)

    window.mainloop()

login_window = Tk()
login_window.resizable(False, False)
login_window.title('Trang Đăng Nhập')
bgImage = ImageTk.PhotoImage(file='bg.jpg')

bgLabel = Label(login_window, image=bgImage)
bgLabel.grid()

heading = Label(login_window, text='USER LOGIN', font=('Microsoft Yahei UI Light', 23, 'bold'), bg='white',
                fg='firebrick1')
heading.place(x=605, y=120)

usernameLabel = Label(login_window, text='Username', font=('Microsoft Yahei UI Light', 11, 'bold'), bg='white', fg='firebrick1')
usernameLabel.place(x=580, y=175)
usernameEntry = Entry(login_window, width=25, font=('Microsoft Yahei UI Light', 11, 'bold'), bd=0, fg='firebrick1')
usernameEntry.place(x=580, y=200)

frame1 = Frame(login_window, width=250, height=2, bg='firebrick1')
frame1.place(x=580, y=222)

passwordLabel = Label(login_window, text='Password', font=('Microsoft Yahei UI Light', 11, 'bold'), bg='white', fg='firebrick1')
passwordLabel.place(x=580, y=245)
passwordEntry = Entry(login_window, width=25, font=('Microsoft Yahei UI Light', 11, 'bold'), bd=0, fg='firebrick1')
passwordEntry.place(x=580, y=270)

frame2 = Frame(login_window, width=250, height=2, bg='firebrick1')
frame2.place(x=580, y=292)

openeye = PhotoImage(file='openeye.png')
eyeButton = Button(login_window, image=openeye, bd=0, bg='white', activebackground='white', cursor='hand2', command=hide)
eyeButton.place(x=800, y=265)

forgetButton = Button(login_window, text='Forgot Password?', bd=0, bg='white', activebackground='white', cursor='hand2',
                      font=('Microsoft Yahei UI Light', 9, 'bold'), fg='firebrick1', activeforeground='firebrick1', command=forget_pass)
forgetButton.place(x=715, y=305)

loginButton = Button(login_window, text='Login', bd=0, width=19, fg='white', activebackground='firebrick1', cursor='hand2',
                    font=('Open Sans', 16, 'bold'), bg='firebrick1', activeforeground='white', command=login_user)
loginButton.place(x=578, y=350)

orLabel = Label(login_window, text='-------------- OR --------------', font=('Open Sans', 16), fg='firebrick1', bg='white')
orLabel.place(x=582, y=400)

facebook_logo = PhotoImage(file='facebook.png')
facebookLabel = Label(login_window, image=facebook_logo, bg='white')
facebookLabel.place(x=640, y=440)

google_logo = PhotoImage(file='google.png')
googleLabel = Label(login_window, image=google_logo, bg='white')
googleLabel.place(x=690, y=440)

twitter_logo = PhotoImage(file='twitter.png')
twitterLabel = Label(login_window, image=twitter_logo, bg='white')
twitterLabel.place(x=740, y=440)

signupLabel = Label(login_window, text="Don't have an account?", font=('Open Sans', 9, 'bold'), fg='firebrick1', bg='white')
signupLabel.place(x=590, y=500)

newaccountButton = Button(login_window, text='Create new one', bd=0, fg='blue', activebackground='white', cursor='hand2',
                    font=('Open Sans', 9, 'bold underline'), bg='white', activeforeground='blue', command=signup_page)
newaccountButton.place(x=725, y=500)

login_window.mainloop()
