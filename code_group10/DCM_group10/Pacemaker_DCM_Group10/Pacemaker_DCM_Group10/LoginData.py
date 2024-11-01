# Login Data
import LoginGUI
from tkinter import *
from CommonFunctions import *
from MainUserGUI import *


def readF():  # reads text file,
    logins = open("Login.txt", "r+")

    login_List = logins.read().splitlines()  # store each line of txt file (without \n) in separate
    # elements in an array

    for i in range(len(login_List)):
        comma = login_List[i].index(",")  # find index where comma is

        string = login_List[i]  # store in temp string

        LoginGUI.user.append(string[:comma])  # split string at comma
        LoginGUI.passw.append(string[comma + 1:])


def validateLogin(login, username, password):

    length = len(LoginGUI.user)

    l_invalid = Label(login,
                      text='Access Denied',
                      height=1,
                      width=20,
                      anchor=W,
                      bg=rgb_picker(196, 231, 255))  # label

    for i in range(length):
        if (LoginGUI.user[i] == username.get() and LoginGUI.passw[i] == password.get()):
            LoginGUI.name_Flag = i  # set flag
            login.destroy()  # close login
            main_window()  # call main_window()
            return
        else:
            l_invalid.place(x=20, y=125)  # tell user input is invalid


def submitNew(login, username, password):
    f = open("Login.txt", "a+")  # open file with append mode and reading mode

    flag = 0

    for i in range(len(LoginGUI.user)):
        if (username.get() == LoginGUI.user[i]):
            l_registered = Label(login,
                                 text='Registration Error: Username is already in use',
                                 height=1,
                                 width=100,
                                 anchor=W,
                                 bg=rgb_picker(196, 231, 255)).place(x=20, y=125)  # tell user input is invalid
            flag = 1

    if (username.get() == '' or password.get() == ''):
        l_registered = Label(login,
                             text='Registration Error: Username/Password Cannot be Blank Spaces',
                             height=1,
                             width=100,
                             anchor=W,
                             bg=rgb_picker(196, 231, 255)).place(x=20, y=125)  # tell user input is invalid
        flag = 1
    elif (len(LoginGUI.user) > 9):
        l_registered = Label(login,
                             text='Registration Error: Maximum Number of Users Reached',
                             height=1,
                             width=100,
                             anchor=W,
                             bg=rgb_picker(196, 231, 255)).place(x=20, y=125)  # tell user it has been registered
        flag = 1
    elif (flag == 0):
        f.write("\n" + username.get() + "," + password.get())  # store new username and password

        LoginGUI.user.append(username.get())  # append user and passw
        LoginGUI.passw.append(password.get())

        l_registered = Label(login,
                             text='Registration Successful',
                             height=1,
                             width=100,
                             anchor=W,
                             bg=rgb_picker(196, 231, 255)).place(x=20, y=125)  # tell user it has been registered
        info = open("" + LoginGUI.user[len(LoginGUI.user) - 1] + "" + LoginGUI.passw[
            len(LoginGUI.passw) - 1] + " Parameters.txt", "w+")