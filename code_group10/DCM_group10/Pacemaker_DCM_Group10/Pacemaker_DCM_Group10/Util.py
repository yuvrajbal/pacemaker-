#Utilities Menu
from MainUserGUI import *
from tkinter import *
from CommonFunctions import rgb_picker
#------------------------------Utilities Menu Functions--------------------------------------
#-----------------------------------Utility Button Windows-----------------------------------
def about(): #about window
    about = Tk() #make new window
    about.title("Pacemaker Device Controlled-Monitor - About the Device") #name window
    about.geometry("500x200") #dimensions of window
    about.config(bg = rgb_picker(196,231,255)) #set color of background

    #top banner label
    l_banner = Label(about,
                     text = "About DCM",
                     font = "Airal 16",
                     bg = rgb_picker(196,231,255)).pack()

    #insert space
    l_space = Label(about,
                    text = " ",
                    height = 1,
                    bg = rgb_picker(196,231,255)).pack()

    #institution label
    l_institution = Label(about,
                          text = "Pace10 Inc.",
                          font = "Airal 13",
                          bg = rgb_picker(196,231,255)).pack()

    #application model number label
    l_appNum = Label(about,
                     text = "Application Model Number: 2039845789",
                     font = "Airal 13",
                     bg = rgb_picker(196,231,255)).pack()

    #application version label
    l_appVersion = Label(about,
                         text = "Application Version: v1.00",
                         font = "Airal 13",
                         bg = rgb_picker(196,231,255)).pack()

    #DCM serial number label
    l_DCMserialNumber = Label(about,
                              text = "DCM Serial Number: 2110-A-001",
                              font = "Airal 13",
                              bg = rgb_picker(196,231,255)).pack()

    #return to util menu button
    b_return = Button(about,
                      text = 'Return to Utilities Menu',
                      height = 1,
                      width = 20,
                      command = about.destroy,
                      bg = rgb_picker(102,192,255)).place(x = 170, y = 160)

#---------------------------------Utilities Button-------------------------------------------
def Util_Button():      #when the button is pushed a new window
                        #is created and opened

    bWindow = Tk() #new window
    bWindow.title("Utilities Menu") #window title
    bWindow.geometry("500x150") #set window size

    bWindow.config(bg = rgb_picker(196,231,255)) #set color of background

    #welcome banner labels
    l_welcome = Label(bWindow,
                      text = "Welcome to the Utilities Menu",
                      font = "Airal 16",
                      height = 1, width = 35,
                      bg = rgb_picker(196,231,255)).pack() #label in window

    #create a blank space
    s1 = Label(bWindow,
               text = " ",
               height = 1,
               width = 1,
               bg = rgb_picker(196,231,255)).pack()

    #display the device information
    b_about = Button(bWindow,
                     text = 'About Device',
                     height = 1,
                     width = 20,
                     command = about,
                     bg = rgb_picker(102,192,255)).place(x=170, y = 50)

    #b_return will return the user to the main DCM UI
    b_return = Button(bWindow,
                      text = 'Return to DCM',
                      height = 1,
                      width = 20,
                      command = bWindow.destroy,
                      bg = rgb_picker(102,192,255)).place(x = 170, y = 110)
