# Login GUI

from functools import partial
from tkinter import *
from CommonFunctions import *
from LoginData import *

#------------------------------------------------Global Variables-------------------------------------------------------
user = []  # holds usernames for all users
passw = []  # holds passwords for all users

name_Flag = -1

#------------------------------------------------Quit New User----------------------------------------------------------
def quitNewUser(w):
    w.destroy()
    login()

#--------------------------------------------------New User-------------------------------------------------------------
def newUser(login, username, password):
    login.destroy()  # close login screen
    newUser = Tk()
    newUser.geometry('400x150')
    newUser.title('Pacemaker Device Controller-Monitor - New User')

    newUser.config(bg=rgb_picker(196, 231, 255))  # set color of background

    # setting min and max size of window
    newUser.minsize(width=400, height=150)
    newUser.maxsize(width=400, height=150)

    l_new = Label(newUser,
                  text="New User Registration",
                  font="Airal 16",
                  height=11, width=20,
                  anchor=N,
                  bg=rgb_picker(196, 231, 255)).pack()

    if (len(user) < 10):  # if max number of users does has not been met

        # username label and text entry box
        l_user_entry = Label(newUser,
                             text="Username: ",
                             bg=rgb_picker(196, 231, 255)).place(x=20, y=40)

        newUsername = StringVar()

        usernameEntry = Entry(newUser,
                              textvariable=newUsername).place(x=80, y=40)
        # password label and password entry box
        l_pass_entry = Label(newUser,
                             text="Password: ",
                             bg=rgb_picker(196, 231, 255)).place(x=20, y=70)

        newPass = StringVar()

        passwordEntry = Entry(newUser,
                              textvariable=newPass,
                              show='*').place(x=80, y=70)

        # submitting username and password
        sub = partial(submitNew, newUser, newUsername, newPass)

        submit = Button(newUser,
                        text="Submit",
                        command=sub,
                        bg=rgb_picker(102, 192, 255)).place(x=20, y=100)

        # quitting window
        quitting = partial(quitNewUser, newUser)

        b_quit = Button(newUser,
                        text="Return to Login",
                        command=quitting,
                        bg=rgb_picker(102, 192, 255)).place(x=80, y=100)

    else:  # maximum users

        max_User = Label(newUser,
                         text="Device already has the maximum number of users",
                         font="Airal 13",
                         bg=rgb_picker(196, 231, 255)).place(x=20, y=50)  # tell user that max users has been reached

        quitting = partial(quitNewUser, newUser)  # quit

        returnb = Button(newUser,
                         text="Return to Login",
                         command=quitting,
                         bg=rgb_picker(102, 192, 255)).place(x=20, y=100)  # return to login

#-----------------------------------------------------Login-------------------------------------------------------------
def login():
    login = Tk()
    login.geometry('400x150')
    login.title('Pacemaker Device Controller-Monitor - Login')

    login.config(bg=rgb_picker(196, 231, 255))  # set color of background

    # setting min and max size of window
    login.minsize(width=400, height=150)
    login.maxsize(width=400, height=150)

    l_login = Label(login,
                    text="Login",
                    font="Airal 16",
                    height=11, width=20,
                    anchor=N,
                    bg=rgb_picker(196, 231, 255)).pack()

    # username label and text entry box
    l_user_entry = Label(login,
                         text="Username: ",
                         bg=rgb_picker(196, 231, 255)).place(x=20, y=40)

    username = StringVar()

    usernameEntry = Entry(login,
                          textvariable=username).place(x=80, y=40)
    # password label and password entry box
    l_pass_entry = Label(login,
                         text="Password: ",
                         bg=rgb_picker(196, 231, 255)).place(x=20, y=70)

    password = StringVar()

    passwordEntry = Entry(login,
                          textvariable=password,
                          show='*').place(x=80, y=70)

    log_in = partial(validateLogin, login, username, password)
    new = partial(newUser, login, username, password)

    # login button
    loginButton = Button(login,
                         text="Login",
                         command=log_in,
                         bg=rgb_picker(102, 192, 255)).place(x=20, y=100)

    b_NewUser = Button(login,
                       text="New User Registration",
                       command=new,
                       bg=rgb_picker(102, 192, 255)).place(x=70, y=100)

    b_quit = Button(login,
                    text='Quit',
                    command=login.destroy,
                    bg=rgb_picker(102, 192, 255)).place(x=205, y=100)

    login.mainloop()



