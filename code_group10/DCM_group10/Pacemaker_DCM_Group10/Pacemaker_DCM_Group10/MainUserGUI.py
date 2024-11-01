# Main User Interface GUI
from tkinter import *
from functools import partial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import time

import LoginGUI
import MainUserData
from CommonFunctions import *
from MainUserData import *
from Util import *
from Reports import *
import SerialCom
import math
import matplotlib.pyplot as plt
isConnected = False
isNewDevice = False

time_ms = []
vData = []
aData = []
t = 0.0
cond = False
counter = 0
window = NONE

canvas = NONE
ax = NONE
fig = NONE

graphType = ""

#------------------------------Patient Information-------------------------
def patient_information(w):

    strName = "First Name: "+LoginGUI.user[LoginGUI.name_Flag]

    l_name = Label(w,
                   text = strName,
                   font="Arial 13",
                   anchor=N,
                   width = 22,
                   bg=rgb_picker(196, 231, 255)).place(x=760, y=105)

    strLast= "Last Name: " + LoginGUI.passw[LoginGUI.name_Flag]

    l_name = Label(w,
                   text=strLast,
                   font="Arial 13",
                   anchor=N,
                   width=22,
                   bg=rgb_picker(196, 231, 255)).place(x=760, y=125)
# ---------------------------------Report Menu-----------------------------
def reportMenu(w):
    # Drop Down Menu~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    report_Ops = ["Bradycardia Parameters Report", "Electrogram Report"]

    # drop-down menu options

    reportSel = StringVar()  # chosen option

    drop = OptionMenu(w,
                      reportSel,
                      *report_Ops)

    drop.config(width=25)

    drop.place(x=767, y=260)  # Drop-Down Menu Widget

    reportSel.set(report_Ops[0])

    open_Button = partial(report_Submit, w, reportSel)

    #open_Button = partial(receive)

    b_submit = Button(w,
                      text="Open",
                      command=open_Button).place(x=845, y=300)  # submit button
#-----------------------------------------Graphs----------------------------------------------
def graph(w):

    # Drop Down Menu~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    graphOps = ["~Select Graph~","Ventricular Signal", "Atrial Signal","Both Signals"]

    # drop-down menu options

    graphSel = StringVar()  # chosen option

    drop = OptionMenu(w,
                      graphSel,
                      *graphOps)

    drop.config(width=15)
    drop.config(height = 1)

    drop.place(x=620, y=370)  # Drop-Down Menu Widget

    #x=470, y=366

    graphSel.set(graphOps[0])

    view_Button = partial(viewGraph,graphSel)

    w.update()
    stop_button = Button(w,
                      text="Stop",
                        command = plot_stop).place(x=800, y=373)  # Stop Graph Button

    w.update()
    b_submit = Button(w,
                      text="View",
                      command = view_Button).place(x=760, y=373)  # Start Graph Button

def viewGraph(selection):
    #_clear()

    global graphType,window

    showCanvas()

    if(selection.get() == "Ventricular Signal" and SerialCom.SENT != -1):
        #print("V Signal")
        graphType = "V"
        plot_start()
    elif(selection.get() == "Atrial Signal" and SerialCom.SENT != -1):
        #print("A Signal")
        graphType = "A"
        plot_start()

    elif(selection.get() == "Both Signals" and SerialCom.SENT != -1):
        #print("Both Signals")
        graphType = "B"
        plot_start()

    if(SerialCom.SENT == -1):
        #print("Parameters have not been sent")
        clearConsole(window)

        l_err = Label(window,
                      text="Parameters have not been sent",
                      font="Arial 13",
                      anchor=N,
                      width=28,
                      height=12,
                      bg=rgb_picker(196, 231, 255),
                      fg="#F43405").place(x=475, y=103)
def plot_start():
    global cond,counter,t
    cond = True
    counter+=1
    t = 0.0
    _clear()

def plot_stop():
    global cond
    cond = False

def _clear():
    global canvas,counter,time_ms,aData,vData

    vData =[]
    time_ms = []
    aData = []

    if(counter >= 0):
        for item in canvas.get_tk_widget().find_all():
            canvas.get_tk_widget().delete(item)

def plot_data():

    global window,lines,lines2,canvas,ax,inital_x1,inital_x2,graphType

    global cond, time_ms, vData, aData,t

    counter = 0

    if(cond == True):

        SerialCom.s.reset_input_buffer()
        signal = SerialCom.getAVSignal()

        if(SerialCom.MODE in [0,2,5,7]):
            signal[0] = 0
        elif(SerialCom.MODE in [1,3,6,8]):
            signal[1] = 0

        if(graphType == "V"):

            signal = signal[0]

            if (len(vData) < 100):
                vData.append(signal)
                time_ms.append(t)

            else:
                vData[0:99] = vData[1:100]
                vData[99] = float(signal)

            t = t + 0.01
            # lines.set_xdata(np.arange(0,len(vData)))
            lines.set_xdata(time_ms)
            lines.set_ydata(vData)
            canvas.draw()
            time.sleep(0.01)
        elif(graphType == "A"):
            signal =signal[1]

            if (len(aData) < 100):
                aData.append(signal)
                time_ms.append(t)

            else:
                aData[0:99] = aData[1:100]
                aData[99] = float(signal)

            t = t + 0.01
            # lines.set_xdata(np.arange(0,len(vData)))
            lines.set_xdata(time_ms)
            lines.set_ydata(aData)
            canvas.draw()
            time.sleep(0.01)

        elif(graphType == "B"):
            if (len(aData) < 100):
                vData.append(signal[0])
                aData.append(signal[1])
                time_ms.append(t)
            else:
                aData[0:99] = aData[1:100]
                aData[99] = float(signal[1])

                vData[0:99] = vData[1:100]
                vData[99] = float(signal[0])

            t = t + 0.01
            #lines.set_xdata(np.arange(0,len(vData)))
            lines.set_xdata(time_ms)
            lines.set_ydata(vData)
            lines2.set_xdata(time_ms)
            lines2.set_ydata(aData)
            canvas.draw()
            time.sleep(0.01)
    window.after(1,plot_data)

def showCanvas():

    global lines, lines2, canvas,fig,ax, inital_x1, inital_x2

    fig = Figure()
    ax = fig.add_subplot(111)
    lines = ax.plot([], [])[0]
    lines2 = ax.plot([], [])[0]

    ax.set_xlim(0,1)

    ax.set_ylim(0,1)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().place(x=480, y=405, width=490, height=245)

# ---------------------------------Programmable Parameters------------------------------------
def prog_para(w):
    flag = 0

    f = open("" + LoginGUI.user[LoginGUI.name_Flag] + "" + LoginGUI.passw[LoginGUI.name_Flag] + " Parameters.txt", "r")

    default = f.read().splitlines()

    if (default == [] or default == ['']):
        flag = 1

    if(flag != 1):
        setIndex()

    # Pacing Mode~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Drop Down Menu~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    l_drop = Label(w,
                   text="Pacing Mode: ",
                   font="Arial 13",
                   anchor=W,
                   bg=rgb_picker(196, 231, 255)).place(x=35, y=115)  # label

    pacingModes = ["AOO", "VOO", "AAI", "VVI", "DOO", "DOOR", "AOOR", "VOOR", "AAIR", "VVIR"]  # drop-down menu options

    clicked = StringVar()  # chosen option

    if (flag == 1):
        clicked.set(pacingModes[0])  # default option
    else:
        clicked.set(default[0])

    drop = OptionMenu(w,
                      clicked,
                      *pacingModes).place(x=145, y=112)  # Drop-Down Menu Widget

    # Lower Rate Limit Components~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    l_LowerRate = Label(w,
                        text="Lower Rate Limit: ",
                        font="Arial 13",
                        anchor=W,
                        bg=rgb_picker(196, 231, 255)).place(x=35, y=148)  # label

    lr = IntVar()  # set variable to type IntVar

    e_lowerR = Entry(w,
                     textvariable=lr).place(x=170, y=150)  # Entry Widget

    # call incr and decr functions
    lr_incre = partial(incr, lr, 1)
    lr_decre = partial(decr, lr, 1)

    if (flag == 1):
        lr.set(60)  # set default value to 30
    else:
        lr.set(int(default[1]))

    lr_units = Label(w,
                     text="ppm",
                     font="Arial 13",
                     anchor=W,
                     bg=rgb_picker(196, 231, 255)).place(x=300, y=148)

    lr_ibutton = Button(w,
                        text="+",
                        command=lr_incre).place(x=390, y=148)  # plus button

    lr_dbutton = Button(w,
                        text="-",
                        command=lr_decre).place(x=415, y=148)  # minus button

    # Upper Rate Limit Components~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    l_UpperRate = Label(w,
                        text="Upper Rate Limit: ",
                        font="Arial 13",
                        anchor=W,
                        bg=rgb_picker(196, 231, 255)).place(x=35, y=180)  # label

    ur = IntVar()  # set to type IntVar

    e_upperR = Entry(w,
                     textvariable=ur).place(x=170, y=182)  # Entry Widget

    # call incr and decr function
    ur_incre = partial(incr, ur, 2)
    ur_decre = partial(decr, ur, 2)

    if (flag == 1):
        ur.set(120)  # set default value to 50
    else:
        ur.set(str(default[2]))

    ur_units = Label(w,
                     text="ppm",
                     font="Arial 13",
                     anchor=W,
                     bg=rgb_picker(196, 231, 255)).place(x=300, y=180)

    ur_ibutton = Button(w,
                        text="+",
                        command=ur_incre).place(x=390, y=180)  # plus button

    ur_dbutton = Button(w,
                        text="-",
                        command=ur_decre).place(x=415, y=180)  # minus button

    # Atrial Amplitude~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    l_Atrial_Amp = Label(w,
                         text="Atrial Amplitude: ",
                         font="Arial 13",
                         anchor=W,
                         bg=rgb_picker(196, 231, 255)).place(x=35, y=210)  # label

    aa = DoubleVar()  # set to type DoubleVar

    e_aAmp = Entry(w,
                   textvariable=aa).place(x=163, y=212)  # Entry Widget

    # call incr and decr function
    aa_incre = partial(incr, aa, 3)
    aa_decre = partial(decr, aa, 3)

    if (flag == 1):
        aa.set(5.0)  # set default value
    else:
        aa.set(str(default[3]))

    aa_units = Label(w,
                     text="V",
                     font="Arial 13",
                     anchor=W,
                     bg=rgb_picker(196, 231, 255)).place(x=293, y=210)

    aa_ibutton = Button(w,
                        text="+",
                        command=aa_incre).place(x=390, y=210)  # plus button

    aa_dbutton = Button(w,
                        text="-",
                        command=aa_decre).place(x=415, y=210)  # minus button

    # Atrial Pulse Width~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    l_Atrial_PW = Label(w,
                        text="Atrial Pulse Width:",
                        font="Arial 13",
                        anchor=W,
                        bg=rgb_picker(196, 231, 255)).place(x=35, y=240)  # label

    apw = IntVar()  # set to DoubleVar
    e_apw = Entry(w,
                  textvariable=apw).place(x=178, y=242)  # entry widget

    # call incr and decr function
    apw_incre = partial(incr, apw, 4)
    apw_decre = partial(decr, apw, 4)

    if (flag == 1):
        apw.set(1)  # set default
    else:
        apw.set(str(default[4]))

    apw_units = Label(w,
                      text="ms",
                      font="Arial 13",
                      anchor=W,
                      bg=rgb_picker(196, 231, 255)).place(x=308, y=240)

    apw_ibutton = Button(w,
                         text="+",
                         command=apw_incre).place(x=390, y=240)  # plus button

    apw_dbutton = Button(w,
                         text="-",
                         command=apw_decre).place(x=415, y=240)  # minus button

    # Ventricular Amplitude~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    l_Ven_Amp = Label(w,
                      text="Ventricular Amplitube: ",
                      font="Arial 13",
                      anchor=W,
                      bg=rgb_picker(196, 231, 255)).place(x=35, y=270)  # label

    va = DoubleVar()  # set to type DoubleVar
    e_va = Entry(w,
                 textvariable=va).place(x=205, y=272)  # Entry Widget

    # call incr and decr function
    va_incre = partial(incr, va, 5)
    va_decre = partial(decr, va, 5)

    if (flag == 1):
        va.set(5.0)  # set default
    else:
        va.set(str(default[5]))

    va_units = Label(w,
                     text="V",
                     font="Arial 13",
                     anchor=W,
                     bg=rgb_picker(196, 231, 255)).place(x=335, y=270)

    va_ibutton = Button(w,
                        text="+",
                        command=va_incre).place(x=390, y=270)  # plus

    va_dbutton = Button(w,
                        text="-",
                        command=va_decre).place(x=415, y=270)  # minus

    # Ventricular Pulse Width~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    l_Ven_PW = Label(w,
                     text="Ventricular Pulse Width: ",
                     font="Arial 13",
                     anchor=W,
                     bg=rgb_picker(196, 231, 255)).place(x=35, y=300)  # label

    vpw = IntVar()  # set to DoubleVar
    e_vpw = Entry(w,
                  textvariable=vpw).place(x=220, y=302)  # Entry Widget

    # call incr and decr function
    vpw_incre = partial(incr, vpw, 6)
    vpw_decre = partial(decr, vpw, 6)

    if (flag == 1):
        vpw.set(1)  # set default
    else:
        vpw.set(str(default[6]))

    vpw_units = Label(w,
                      text="ms",
                      font="Arial 13",
                      anchor=W,
                      bg=rgb_picker(196, 231, 255)).place(x=350, y=300)

    vpw_ibutton = Button(w,
                         text="+",
                         command=vpw_incre).place(x=390, y=300)  # plus

    vpw_dbutton = Button(w,
                         text="-",
                         command=vpw_decre).place(x=415, y=300)  # minus

    # VRP~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    l_VRP = Label(w,
                  text="VRP: ",
                  font="Arial 13",
                  anchor=W,
                  bg=rgb_picker(196, 231, 255)).place(x=35, y=330)  # label

    vrp = IntVar()  # set to IntVar
    e_vrp = Entry(w,
                  textvariable=vrp).place(x=80, y=332)  # Entry Widget

    # call incr and decr fucntions
    vrp_incre = partial(incr, vrp, 7)
    vrp_decre = partial(decr, vrp, 7)

    if (flag == 1):
        vrp.set(320)  # set default
    else:
        vrp.set(str(default[7]))

    vrp_units = Label(w,
                      text="ms",
                      font="Arial 13",
                      anchor=W,
                      bg=rgb_picker(196, 231, 255)).place(x=210, y=330)

    vrp_ibutton = Button(w,
                         text="+",
                         command=vrp_incre).place(x=390, y=330)  # plus

    vrp_dbutton = Button(w,
                         text="-",
                         command=vrp_decre).place(x=415, y=330)  # minus

    # ARP~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    l_ARP = Label(w,
                  text="ARP: ",
                  font="Arial 13",
                  anchor=W,
                  bg=rgb_picker(196, 231, 255)).place(x=35, y=360)  # label

    arp = IntVar()  # set to type IntVar
    e_arp = Entry(w,
                  textvariable=arp).place(x=80, y=362)  # Entry Widegt

    # call incr and decr functions
    arp_incre = partial(incr, arp, 8)
    arp_decre = partial(decr, arp, 8)

    if (flag == 1):
        arp.set(250)  # set default
    else:
        arp.set(str(default[8]))

    arp_units = Label(w,
                      text="ms",
                      font="Arial 13",
                      anchor=W,
                      bg=rgb_picker(196, 231, 255)).place(x=210, y=360)

    arp_ibutton = Button(w,
                         text="+",
                         command=arp_incre).place(x=390, y=360)  # plua

    arp_dbutton = Button(w,
                         text="-",
                         command=arp_decre).place(x=415, y=360)  # minus

    # AV Delay~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    l_avd = Label(w,
                  text="AV Delay: ",
                  font="Arial 13",
                  anchor=W,
                  bg=rgb_picker(196, 231, 255)).place(x=35, y=390)  # label

    AVD = IntVar()  # set to type IntVar
    e_avd = Entry(w,
                  textvariable=AVD).place(x=115, y=392)  # Entry Widegt

    AVD_incre = partial(incr, AVD, 10)
    AVD_decre = partial(decr, AVD, 10)
    if (flag == 1):
        AVD.set(150)
    else:
        AVD.set(str(default[9]))

    avd_units = Label(w,
                      text="ms",
                      font="Arial 13",
                      anchor=W,
                      bg=rgb_picker(196, 231, 255)).place(x=243, y=390)

    AVD_ibutton = Button(w,
                         text="+",
                         command=AVD_incre).place(x=390, y=390)  # plua

    AVD_dbutton = Button(w,
                         text="-",
                         command=AVD_decre).place(x=415, y=390)  # minus

    # Plus ans Minus Button

    # Reaction Time~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    l_react = Label(w,
                    text="Reaction Time: ",
                    font="Arial 13",
                    anchor=W,
                    bg=rgb_picker(196, 231, 255)).place(x=35, y=420)  # label

    react = IntVar()  # set to type IntVar
    e_react = Entry(w,
                    textvariable=react).place(x=155, y=422)  # Entry Widegt

    react_incre = partial(incr, react, 11)
    react_decre = partial(decr, react, 11)

    if (flag == 1):
        react.set(30)
    else:
        react.set(str(default[10]))

    react_units = Label(w,
                        text="s",
                        font="Arial 13",
                        anchor=W,
                        bg=rgb_picker(196, 231, 255)).place(x=283, y=420)

    react_ibutton = Button(w,
                           text="+",
                           command=react_incre).place(x=390, y=420)  # plus

    react_dbutton = Button(w,
                           text="-",
                           command=react_decre).place(x=415, y=420)  # minus

    # Recovery Time~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    l_recov = Label(w,
                    text="Recovery Time: ",
                    font="Arial 13",
                    anchor=W,
                    bg=rgb_picker(196, 231, 255)).place(x=35, y=450)  # label

    recov = IntVar()  # set to type IntVar
    e_recov = Entry(w,
                    textvariable=recov).place(x=155, y=452)  # Entry Widegt

    recov_incre = partial(incr, recov, 12)
    recov_decre = partial(decr, recov, 12)

    if (flag == 1):
        recov.set(5)
    else:
        recov.set(str(default[11]))

    recov_units = Label(w,
                        text="min",
                        font="Arial 13",
                        anchor=W,
                        bg=rgb_picker(196, 231, 255)).place(x=283, y=450)

    recov_ibutton = Button(w,
                           text="+",
                           command=recov_incre).place(x=390, y=450)  # plus

    recov_dbutton = Button(w,
                           text="-",
                           command=recov_decre).place(x=415, y=450)  # minus

    # Plus ans Minus Button

    # Activity Threshold~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    l_act = Label(w,
                  text="Activity Threshold: ",
                  font="Arial 13",
                  anchor=W,
                  bg=rgb_picker(196, 231, 255)).place(x=35, y=480)  # label

    activity_threshold = ["V-Low", "Low", "Med-Low", "Med", "Med-High", "High", "V-High"]

    act = StringVar()  # set to type IntVar

    m_act = OptionMenu(w,
                       act,
                       *activity_threshold).place(x = 175, y = 478)

    if (flag == 1):
        act.set(activity_threshold[3])
    else:
        act.set(str(default[12]))

    # Plus ans Minus Button

    # Max Sensor Rate~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    l_maxSen = Label(w,
                     text="Max Sensor Rate: ",
                     font="Arial 13",
                     anchor=W,
                     bg=rgb_picker(196, 231, 255)).place(x=35, y=510)  # label

    maxSen = IntVar()  # set to type IntVar
    e_maxSen = Entry(w,
                     textvariable=maxSen).place(x=175, y=512)  # Entry Widegt

    # Plus ans Minus Button
    maxSen_incre = partial(incr, maxSen, 14)
    maxSen_decre = partial(decr, maxSen, 14)

    if (flag == 1):
        maxSen.set(120)
    else:
        maxSen.set(str(default[13]))

    maxSen_units = Label(w,
                         text="ppm",
                         font="Arial 13",
                         anchor=W,
                         bg=rgb_picker(196, 231, 255)).place(x=298, y=510)

    maxSen_ibutton = Button(w,
                            text="+",
                            command=maxSen_incre).place(x=390, y=510)  # plus

    maxSen_dbutton = Button(w,
                            text="-",
                            command=maxSen_decre).place(x=415, y=510)  # minus

    # Rate Smoothing~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    l_rateS = Label(w,
                    text="Rate Smoothing: ",
                    font="Arial 13",
                    anchor=W,
                    bg=rgb_picker(196, 231, 255)).place(x=35, y=540)  # label

    rateSmoothing = [0,3,6,9,12,15,18,21,25]

    rateS = IntVar()  # set to type IntVar


    m_rateS = OptionMenu(w,
                         rateS,
                         *rateSmoothing).place(x=160, y=538)  # Entry Widegt

    # Plus ans Minus Button
    rateS_incre = partial(incr, rateS, 15)
    rateS_decre = partial(decr, rateS, 15)

    if (flag == 1):
        rateS.set(rateSmoothing[0])
    else:
        rateS.set(str(default[14]))

    rateS_units = Label(w,
                        text="%",
                        font="Arial 13",
                        anchor=W,
                        bg=rgb_picker(196, 231, 255)).place(x=220, y=540)

    #Ventricular Sensitiivty~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    l_vsen = Label(w,
                    text="Ventricular Sensitivity: ",
                    font="Arial 13",
                    anchor=W,
                    bg=rgb_picker(196, 231, 255)).place(x=35, y=570)  # label

    vsen = DoubleVar()  # set to type IntVar
    e_vsen = Entry(w,
                    textvariable=vsen).place(x=205, y=572)  # Entry Widget

    # Plus ans Minus Button
    vsen_incre = partial(incr, vsen, 15)
    vsen_decre = partial(decr, vsen, 15)

    if (flag == 1):
        vsen.set(0)
    else:
        vsen.set(str(default[15]))

    vsen_units = Label(w,
                       text="V",
                       font="Arial 13",
                       anchor=W,
                       bg=rgb_picker(196, 231, 255)).place(x=330, y=570)

    vsen_ibutton = Button(w,
                           text="+",
                           command=vsen_incre).place(x=390, y=570)  # plus

    vsen_dbutton = Button(w,
                           text="-",
                           command=vsen_decre).place(x=415, y=570)  # minus

    #Atrial Sensitivity~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    l_asen = Label(w,
                    text="Atrial Sensitivity: ",
                    font="Arial 13",
                    anchor=W,
                    bg=rgb_picker(196, 231, 255)).place(x=35, y=600)  # label

    asen = DoubleVar()  # set to type IntVar
    e_asen = Entry(w,
                    textvariable=asen).place(x=160, y=602)  # Entry Widget

    # Plus ans Minus Button
    asen_incre = partial(incr, asen, 16)
    asen_decre = partial(decr, asen, 16)

    if (flag == 1):
        asen.set(0)
    else:
       asen.set(str(default[16]))

    asen_units = Label(w,
                        text="V",
                        font="Arial 13",
                        anchor=W,
                        bg=rgb_picker(196, 231, 255)).place(x=283, y=600)

    asen_ibutton = Button(w,
                           text="+",
                           command=asen_incre).place(x=390, y=600)  # plus

    asen_dbutton = Button(w,
                           text="-",
                           command=asen_decre).place(x=415, y=600)  # minus

    #Response Factor----------------------------------------------------------------------------------------------------
    l_rf = Label(w,
                   text="Response Factor: ",
                   font="Arial 13",
                   anchor=W,
                   bg=rgb_picker(196, 231, 255)).place(x=35, y=630)  # label

    rf = IntVar()  # set to type IntVar
    e_rf = Entry(w,
                   textvariable=rf).place(x=170, y=632)  # Entry Widget

    # Plus ans Minus Button
    rf_incre = partial(incr, rf, 17)
    rf_decre = partial(decr, rf, 17)

    if (flag == 1):
        rf.set(8)
    else:
        rf.set(str(default[17]))

    rf_ibutton = Button(w,
                          text="+",
                          command=rf_incre).place(x=340, y=630)  # plus

    rf_dbutton = Button(w,
                          text="-",
                          command=rf_decre).place(x=365, y=630)  # minus

    # Submit~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    s = partial(submit_Parameters, w, clicked, lr, ur, aa, apw, va, vpw, vrp, arp, AVD, react, recov, act, maxSen,
                rateS,vsen,asen,rf)  # call submit function
    # to store parameters

    b_submit = Button(w,
                      text="Submit",
                      command=s).place(x=390, y=629)  # submit button

def displayError(w,error_list, lr, ur, aa, apw, va, vpw, vrp, arp, AVD, react, recov, maxSen, vsen, asen,rf):

    clearConsole(w)

    l_err = Label(w,
                  text = error_list[2],
                  font = "Arial 13",
                  anchor = N,
                  width = 28,
                  height = 12,
                  bg= rgb_picker(196, 231, 255),
                  fg = "#F43405").place(x=475, y=103)

    if(error_list[0] == 0):
        if(error_list[1] == 1):
            lr.set(error_list[3])
        elif(error_list[1] == 2):
            ur.set(error_list[3])
        elif (error_list[1] == 3):
            aa.set(error_list[3])
        elif (error_list[1] == 4):
            apw.set(error_list[3])
        elif(error_list[1] == 5):
            va.set(error_list[3])
        elif (error_list[1] == 6):
            vpw.set(error_list[3])
        elif(error_list[1] == 7):
            vrp.set(error_list[3])
        elif (error_list[1] == 8):
            arp.set(error_list[3])
        elif(error_list[1] == 9):
            AVD.set(error_list[3])
        elif (error_list[1] == 10):
            react.set(error_list[3])
        elif(error_list[1] == 11):
            recov.set(error_list[3])
        elif (error_list[1] == 13):
            maxSen.set(error_list[3])
        elif (error_list[1] ==15):
            vsen.set(error_list[3])
        elif(error_list[1] == 16):
            asen.set(error_list[3])
        elif(error_list[1] == 17):
            rf.set(error_list[3])

# ---------------------------------Patient Information----------------------------------------
def set_message(w, pacingMode, lower_rate, upper_rate, atr_amp, atr_pw, ven_amp, ven_pw, vrp_, arp_, avd_, react_,
                recov_, act_, max_sen, rate_s, v_sen, a_sen,res_fact):
    # Label Place Holders

    l_set = Label(w,
                  text="Parameters Set",
                  font="Arial 11",
                  anchor=N,
                  bg=rgb_picker(196, 231, 255)).place(x=545, y=103)

    strMode = "Pacing Mode: " + pacingMode

    l_mode = Label(w,
                   text=strMode,
                   font="Arial 10",
                   anchor=W,
                   bg=rgb_picker(196, 231, 255)).place(x=472, y=120)

    strLower = "Lower Rate: " + str(lower_rate) + " ppm"

    l_lr = Label(w,
                 text=strLower,
                 font="Arial 10",
                 anchor=W,
                 bg=rgb_picker(196, 231, 255)).place(x=472, y=140)

    strUpper = "Upper Rate: " + str(upper_rate) + " ppm"

    l_ur = Label(w,
                 text=strUpper,
                 font="Arial 10",
                 anchor=W,
                 bg=rgb_picker(196, 231, 255)).place(x=472, y=160)

    strAA = "Atrial Amp: " + str(atr_amp) + " V"

    l_aa = Label(w,
                 text=strAA,
                 font="Arial 10",
                 anchor=W,
                 bg=rgb_picker(196, 231, 255)).place(x=472, y=180)

    strApw = "Atrial PW: " + str(atr_pw) + " ms"

    l_apw = Label(w,
                  text=strApw,
                  font="Arial 10",
                  anchor=W,
                  bg=rgb_picker(196, 231, 255)).place(x=472, y=200)

    strVA = "Ven Amp: " + str(ven_amp) + " V"

    l_va = Label(w,
                 text=strVA,
                 font="Arial 10",
                 anchor=W,
                 bg=rgb_picker(196, 231, 255)).place(x=472, y=220)

    strVpw = "Ven PW: " + str(ven_pw) + " ms"

    l_vpw = Label(w,
                  text=strVpw,
                  font="Arial 10",
                  anchor=W,
                  bg=rgb_picker(196, 231, 255)).place(x=472, y=240)

    strVrp = "VRP: " + str(vrp_) + " ms"

    l_vrp = Label(w,
                  text=strVrp,
                  font="Arial 10",
                  anchor=W,
                  bg=rgb_picker(196, 231, 255)).place(x=472, y=260)

    strArp = "ARP: " + str(arp_) + " ms"

    l_arp = Label(w,
                  text=strArp,
                  font="Arial 10",
                  anchor=W,
                  bg=rgb_picker(196, 231, 255)).place(x=472, y=280)

    strAVD = "AV Delay: " + str(avd_) + " ms"

    l_avd = Label(w,
                  text=strAVD,
                  font="Arial 10",
                  anchor=W,
                  bg=rgb_picker(196, 231, 255)).place(x=472, y=300)

    strReact = "Reaction Time: " + str(react_) + " s"

    l_react = Label(w,
                    text=strReact,
                    font="Arial 10",
                    anchor=W,
                    bg=rgb_picker(196, 231, 255)).place(x=600, y=120)

    strRecov = "Recovery Time: \n" + str(recov_) + " min"

    l_recov = Label(w,
                    text=strRecov,
                    font="Arial 10",
                    anchor=W,
                    bg=rgb_picker(196, 231, 255)).place(x=600, y=140)

    strAct = "Act. Threshold: \n" + act_

    l_act = Label(w,
                    text=strAct,
                    font="Arial 10",
                    anchor=W,
                    bg=rgb_picker(196, 231, 255)).place(x=600, y=180)

    strMaxSen = "Max Sensor Rate: " + str(max_sen) + " ppm"

    l_maxSen = Label(w,
                     text=strMaxSen,
                     font="Arial 10",
                     anchor=W,
                     bg=rgb_picker(196, 231, 255)).place(x=472, y=320)

    strRS = "Rate Smoothing: " + str(rate_s) + " %"

    l_rs = Label(w,
                 text=strRS,
                 font="Airal 10",
                 anchor=W,
                 bg=rgb_picker(196, 231, 255)).place(x=600, y=220)

    strVSen = "Ven. Sensitivity: " +str(v_sen) + " V"

    l_VSen = Label(w,
                 text=strVSen,
                 font="Arial 10",
                 anchor=W,
                 bg=rgb_picker(196, 231, 255)).place(x=600, y=240)

    strASen = "Atr. Sensitivity: " +str(a_sen) + " V"

    l_ASen = Label(w,
                 text=strASen,
                 font="Arial 10",
                 anchor=W,
                 bg=rgb_picker(196, 231, 255)).place(x=600, y=260)

    strRF = "Response Factor: " +str(res_fact)

    l_RF = Label(w,
                 text=strRF,
                 font="Arial 10",
                 anchor=W,
                 bg=rgb_picker(196, 231, 255)).place(x=600, y=280)

def clearConsole(w):

    l_set = Label(w,
                  text="                               ",
                  font="Arial 11",
                  anchor=N,
                  bg=rgb_picker(196, 231, 255)).place(x=545, y=103)


    l_mode = Label(w,
                   text="                               ",
                   font="Arial 10",
                   anchor=W,
                   bg=rgb_picker(196, 231, 255)).place(x=472, y=120)


    l_lr = Label(w,
                 text="                               ",
                 font="Arial 10",
                 anchor=W,
                 bg=rgb_picker(196, 231, 255)).place(x=472, y=140)


    l_ur = Label(w,
                 text="                               ",
                 font="Arial 10",
                 anchor=W,
                 bg=rgb_picker(196, 231, 255)).place(x=472, y=160)


    l_aa = Label(w,
                 text="                               ",
                 font="Arial 10",
                 anchor=W,
                 bg=rgb_picker(196, 231, 255)).place(x=472, y=180)


    l_apw = Label(w,
                  text="                               ",
                  font="Arial 10",
                  anchor=W,
                  bg=rgb_picker(196, 231, 255)).place(x=472, y=200)

    l_va = Label(w,
                 text="                               ",
                 font="Arial 10",
                 anchor=W,
                 bg=rgb_picker(196, 231, 255)).place(x=472, y=220)


    l_vpw = Label(w,
                  text="                               ",
                  font="Arial 10",
                  anchor=W,
                  bg=rgb_picker(196, 231, 255)).place(x=472, y=240)


    l_vrp = Label(w,
                  text="                               ",
                  font="Arial 10",
                  anchor=W,
                  bg=rgb_picker(196, 231, 255)).place(x=472, y=260)


    l_arp = Label(w,
                  text="                               ",
                  font="Arial 10",
                  anchor=W,
                  bg=rgb_picker(196, 231, 255)).place(x=472, y=280)


    l_avd = Label(w,
                  text="                               ",
                  font="Arial 10",
                  anchor=W,
                  bg=rgb_picker(196, 231, 255)).place(x=472, y=300)


    l_react = Label(w,
                    text="                               ",
                    font="Arial 10",
                    anchor=W,
                    bg=rgb_picker(196, 231, 255)).place(x=600, y=120)


    l_recov = Label(w,
                    text="                               \n                               ",
                    font="Arial 10",
                    anchor=W,
                    bg=rgb_picker(196, 231, 255)).place(x=600, y=140)

    l_act = Label(w,
                    text="                               \n                               ",
                    font="Arial 10",
                    anchor=W,
                    bg=rgb_picker(196, 231, 255)).place(x=600, y=180)


    l_maxSen = Label(w,
                     text="                                        ",
                     font="Arial 10",
                     anchor=W,
                     bg=rgb_picker(196, 231, 255)).place(x=472, y=320)


    l_rs = Label(w,
                 text="                               \n                               ",
                 font="Airal 10",
                 anchor=W,
                 bg=rgb_picker(196, 231, 255)).place(x=600, y=220)


    l_VSen = Label(w,
                 text="                                ",
                 font="Arial 10",
                 anchor=W,
                 bg=rgb_picker(196, 231, 255)).place(x=600, y=240)


    l_ASen = Label(w,
                 text="                                ",
                 font="Arial 10",
                 anchor=W,
                 bg=rgb_picker(196, 231, 255)).place(x=600, y=260)

    l_RF = Label(w,
                 text="                                ",
                 font="Arial 10",
                 anchor=W,
                 bg=rgb_picker(196, 231, 255)).place(x=600, y=280)

# ----------------------------Windows Quit-----------------------------
def window_Quit(w):  # quit the main menu
    # this will close the main window and call the
    # login function, prompting the user to login again
    w.destroy()
    LoginGUI.login()


# ---------------------------Main Window-------------------------------
def main_window():
    global isConnected
    global isNewDevice

    global window
    global lines, canvas
    window = Tk()  # creating new  blank window
    window.title("Pacemaker Device Controller-Monitor (authorized access)")
    window.geometry("1000x700")  # setting window size
    window.config(bg=rgb_picker(102, 192, 255))  # set color of background

    # setting min and max size of window
    window.minsize(width=1000, height=700)
    window.maxsize(width=1000, height=700)

    s_1 = Label(window, text=" ", bg=rgb_picker(102, 192, 255)).pack()  # new space

    # Welcome Banner~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    SerialCom.connection(window)

    if (LoginGUI.user[LoginGUI.name_Flag] == ''):
        s = "Welcome, Patient"
    else:
        s = "Welcome, " + LoginGUI.user[LoginGUI.name_Flag] + " " + LoginGUI.passw[LoginGUI.name_Flag]

    #print(LoginGUI.user)
    #print(LoginGUI.passw)
    #print(LoginGUI.name_Flag)

    l_welcome = Label(window,
                      text=s,
                      font="Arial 32",
                      bd=1,
                      relief='solid',
                      height=1, width=35,
                      bg=rgb_picker(196, 231, 255)).pack()  # label in window

    # Programmable Parameters Section~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    l_prg_par = Label(window,
                      text="Programmable Parameters",
                      font="Arial 16",
                      bd=1,
                      relief='solid',
                      height=24, width=35,
                      anchor=N,
                      bg=rgb_picker(196, 231, 255)).place(x=30, y=80)  # label in window

    prog_para(window)  # Call Programmable Parameters Function

    # Reports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    l_reports = Label(window,
                      text="Reports",
                      font="Arial 16",
                      bd=1,
                      relief='solid',
                      height=5, width=18,
                      anchor=N,
                      bg=rgb_picker(196, 231, 255)).place(x=755, y=220)
    reportMenu(window)

    # Console~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    l_console = Label(window,
                      text="Console",
                      font="Arial 16",
                      bd=1,
                      relief='solid',
                      height=11, width=22,
                      anchor=N,
                      bg=rgb_picker(196, 231, 255)).place(x=470, y=80)

    l_patient = Label(window,
                      text="Patient Information",
                      font="Arial 16",
                      bd=1,
                      relief='solid',
                      height=5, width=18,
                      anchor=N,
                      bg=rgb_picker(196, 231, 255)).place(x=755, y=80)

    patient_information(window)

    # Graphs Section~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    l_graphs = Label(window,
                     text="             Graphs",
                     font="Arial 16",
                     bd=1,
                     relief='solid',
                     height=12, width=42,
                     anchor=NW,
                     bg=rgb_picker(196, 231, 255)).place(x=470, y=366)
    graph(window)

    # creating a button
    b_utli = Button(window,
                    text='Utilities',
                    command=Util_Button,
                    height=1,
                    width=20).place(x=30, y=665)

    # should go to the login in menu

    quitting = partial(window_Quit, window)

    b_quit = Button(window,
                    text='Quit',
                    command=quitting,
                    height=1,
                    width=20).place(x=190, y=665)

    con = partial(SerialCom.connection, window)

    b_connect = Button(window,
                       text='Test Connection',
                       height=1,
                       command=con).place(x=350, y=665)

    window.after(1,plot_data)
    window.mainloop()


