import datetime
import time

import LoginGUI
import SerialCom

from tkinter import *
from CommonFunctions import *
from functools import partial
from time import strftime
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np


# ---------------------------------------Reports Menu-----------------------------------------
def report_Submit(w, selection):
    report_file = open("" + LoginGUI.user[LoginGUI.name_Flag] + "" + LoginGUI.passw[
        LoginGUI.name_Flag] + " " + selection.get() + ".txt", "w+")
    parameters_file = open(
        "" + LoginGUI.user[LoginGUI.name_Flag] + "" + LoginGUI.passw[LoginGUI.name_Flag] + " Parameters.txt", "r")

    now = datetime.now()

    dt_string = now.strftime("%m/%d/%Y %H:%M:%S %p")

    report_file.write(
        "Pace10 Inc.\n\nDate & Time:" + dt_string + "\n\nDevice Model: FRDM-K64F\nDevice Serial Number: \nDCM Serial Number: 2110-A-001\nApplication Version Number: v2.30\n\n" + selection.get())

    report_file.close()

    report_file = open("" + LoginGUI.user[LoginGUI.name_Flag] + "" + LoginGUI.passw[
        LoginGUI.name_Flag] + " " + selection.get() + ".txt", "r")
    r = Tk()
    r.title(selection.get())

    r.config(bg=rgb_picker(196, 231, 255))

    bpr_report = report_file.readlines()

    l1 = Label(r,
               text=bpr_report[0],
               font="Airal 14",
               anchor=W,
               bg=rgb_picker(196, 231, 255)).place(x=0, y=0)

    l2 = Label(r,
               text=bpr_report[1],
               font="Airal 14",
               anchor=W,
               bg=rgb_picker(196, 231, 255)).place(x=0, y=30)

    l3 = Label(r,
               text=bpr_report[2],
               font="Airal 14",
               anchor=W,
               bg=rgb_picker(196, 231, 255)).place(x=0, y=60)

    l4 = Label(r,
               text=bpr_report[3],
               font="Airal 14",
               anchor=W,
               bg=rgb_picker(196, 231, 255)).place(x=0, y=90)

    l5 = Label(r,
               text=bpr_report[4],
               font="Airal 14",
               anchor=W,
               bg=rgb_picker(196, 231, 255)).place(x=0, y=120)

    l6 = Label(r,
               text=bpr_report[5],
               font="Airal 14",
               anchor=W,
               bg=rgb_picker(196, 231, 255)).place(x=0, y=150)

    l7 = Label(r,
               text=bpr_report[6],
               font="Airal 14",
               anchor=W,
               bg=rgb_picker(196, 231, 255)).place(x=0, y=180)

    l8 = Label(r,
               text=bpr_report[7],
               font="Airal 14",
               anchor=W,
               bg=rgb_picker(196, 231, 255)).place(x=0, y=210)

    l9 = Label(r,
               text=bpr_report[8],
               font="Airal 14",
               anchor=W,
               bg=rgb_picker(196, 231, 255)).place(x=0, y=240)

    l10 = Label(r,
                text=bpr_report[9],
                font="Airal 14",
                anchor=W,
                bg=rgb_picker(196, 231, 255)).place(x=0, y=270)

    if(selection.get() == "Bradycardia Parameters Report"):
        parameterReport(r)
    elif(selection.get() == "Electrogram Report"):
        egramReport(r)


def parameterReport(r):

    r.geometry('500x900')

    patient_file = open("" + LoginGUI.user[LoginGUI.name_Flag] + "" + LoginGUI.passw[LoginGUI.name_Flag] + " Parameters.txt", "r")

    parameters = patient_file.read().splitlines()

    strP = ['Pacing Mode', 'Lower Rate Limit', 'Upper Rate Limit','Atrial Amplitude','Atrial Pulse Width',
           'Ventricular Amplitude', 'Ventricular Pulse Width', 'VRP', 'ARP','AV Delay','Reaction Time',
           'Recovery Time', 'Activity Threshold', 'Maximum Sensor Rate', 'Rate Smoothing','Ventricular Sensitivity',
           'Atrial Sensitivity', 'Response Factor']

    units = ['','ppm','ppm','V','ms','V','ms','ms','ms','ms','s','min','','ppm','%','V','V','']

    label_y = 270

    for i in range(len(parameters)):

        string = strP[i] +": " + parameters[i] + " " + units[i]
        label_y = label_y + 30

        l = Label(r,
                  text = string,
                  font = "Airal 12",
                  anchor = W,
                  bg = rgb_picker(196, 231, 255)).place(x = 0, y = label_y)

def egramReport(r):

    r.geometry('1100x950')

    patient_file = open("" + LoginGUI.user[LoginGUI.name_Flag] + "" + LoginGUI.passw[LoginGUI.name_Flag] + " Parameters.txt", "r")

    parameters = patient_file.read().splitlines()

    strP = ['Pacing Mode', 'Lower Rate Limit', 'Upper Rate Limit','Atrial Amplitude','Atrial Pulse Width',
           'Ventricular Amplitude', 'Ventricular Pulse Width', 'VRP', 'ARP','AV Delay','Reaction Time',
           'Recovery Time', 'Activity Threshold', 'Maximum Sensor Rate', 'Rate Smoothing','Ventricular Sensitivity',
           'Atrial Sensitivity', 'Response Factor']

    units = ['','ppm','ppm','V','ms','V','ms','ms','ms','ms','s','min','','ppm','%','V','V','']

    label_y = 280

    for i in range(len(parameters)):

        string = strP[i] +": " + parameters[i] + " " + units[i]
        label_y = label_y + 20

        l = Label(r,
                  text = string,
                  font = "Arial 10",
                  anchor = W,
                  bg = rgb_picker(196, 231, 255)).place(x = 0, y = label_y)

        #y = 640

    fig = Figure()
    ax = fig.add_subplot(111)

    ax.set_title('Ventricle Signal')
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Voltage')

    ax.set_xlim(0,1)
    ax.set_ylim(0,1)

    lines = ax.plot([],[])[0]

    canvas1 = FigureCanvasTkAgg(fig,master = r)
    canvas1.get_tk_widget().place(x = 0, y = 660, width=490, height=245)
    canvas1.draw()

    vData = []
    time_ms = []
    t = 0.0

    for i in range(100):
        signal = SerialCom.getAVSignal()

        if(SerialCom.MODE in [0,2,5,7]):
            signal = 0
        else:
            signal = signal[0]

        if(len(vData) < 100):
            vData.append(signal)
            time_ms.append(t)

        t = t + 0.01
        lines.set_xdata(time_ms)
        lines.set_ydata(vData)
        canvas1.draw()
        time.sleep(0.01)


    fig2 = Figure()
    ax2 = fig2.add_subplot(111)

    ax2.set_title('Atrial Signal')
    ax2.set_xlabel('Time (ms)')
    ax2.set_ylabel('Voltage')

    ax2.set_xlim(0,1)
    ax2.set_ylim(0,1)

    lines2 = ax2.plot([],[])[0]

    canvas2 = FigureCanvasTkAgg(fig2,master = r)
    canvas2.get_tk_widget().place(x = 500, y = 660, width=490, height=245)
    canvas2.draw()

    time_ms = []
    aData = []
    t = 0.0
    for i in range(100):
        signal = SerialCom.getAVSignal()

        if (SerialCom.MODE in [1, 3, 6, 8]):
            signal = 0
        else:
            signal = signal[1]

        if(len(aData) < 100):
            aData.append(signal)
            time_ms.append(t)

        t = t + 0.01
        lines2.set_xdata(time_ms)
        lines2.set_ydata(aData)
        canvas2.draw()
        time.sleep(0.01)