# Main User Interface Data
import _tkinter
from tkinter import *
from functools import partial
from time import strftime
from datetime import datetime

import LoginGUI
from CommonFunctions import *
import MainUserGUI
from SerialCom import *

AtrAmp_counter = int(50)
VenAmp_counter = int(50)
AtrSens_counter = int(0)
VenSens_counter = int(0)

setFlag = -1

amp = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.7,0.8,0.9,1.0,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4.0,4.1,4.2,4.3,4.4,4.5,4.6,4.6,4.7,4.8,4.9,5.0]
sens = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.7,0.8,0.9,1.0,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4.0,4.1,4.2,4.3,4.4,4.5,4.6,4.6,4.7,4.8,4.9,5.0]

def submit_Parameters(w, mode, lr, ur, aa, apw, va, vpw, vrp, arp, AVD, react, recov, act, maxSen,rateS, vsen, asen,rf):  # submits the parameters

    global setFlag

    patient_file = open("" + LoginGUI.user[LoginGUI.name_Flag] + "" + LoginGUI.passw[LoginGUI.name_Flag] + " Parameters.txt", "w")

    # storing the inputted values
    pacingMode = mode.get()

    try:
        lower_rate = lr.get()
    except _tkinter.TclError:
        e = blankValueError(1)
        MainUserGUI.displayError(w, e, lr, ur, aa, apw, va, vpw, vrp, arp, AVD, react, recov, maxSen, vsen, asen,rf)
        return

    try:
        upper_rate = ur.get()
    except _tkinter.TclError:
        e = blankValueError(2)
        MainUserGUI.displayError(w, e, lr, ur, aa, apw, va, vpw, vrp, arp, AVD, react, recov, maxSen, vsen, asen,rf)
        return

    try:
        atr_amp = aa.get()
    except _tkinter.TclError:
        e = blankValueError(3)
        MainUserGUI.displayError(w, e, lr, ur, aa, apw, va, vpw, vrp, arp, AVD, react, recov, maxSen, vsen, asen,rf)
        return

    try:
        atr_pw = apw.get()
    except _tkinter.TclError:
        e = blankValueError(4)
        MainUserGUI.displayError(w, e, lr, ur, aa, apw, va, vpw, vrp, arp, AVD, react, recov, maxSen, vsen, asen,rf)
        return

    try:
        ven_amp = va.get()
    except _tkinter.TclError:
        e = blankValueError(5)
        MainUserGUI.displayError(w, e, lr, ur, aa, apw, va, vpw, vrp, arp, AVD, react, recov, maxSen, vsen, asen,rf)
        return

    try:
        ven_pw = vpw.get()
    except _tkinter.TclError:
        e = blankValueError(6)
        MainUserGUI.displayError(w, e, lr, ur, aa, apw, va, vpw, vrp, arp, AVD, react, recov, maxSen, vsen, asen,rf)
        return

    try:
        vrp_ = vrp.get()
    except _tkinter.TclError:
        e = blankValueError(7)
        MainUserGUI.displayError(w, e, lr, ur, aa, apw, va, vpw, vrp, arp, AVD, react, recov, maxSen, vsen, asen,rf)
        return

    try:
        arp_ = arp.get()
    except _tkinter.TclError:
        e = blankValueError(8)
        MainUserGUI.displayError(w, e, lr, ur, aa, apw, va, vpw, vrp, arp, AVD, react, recov, maxSen, vsen, asen,rf)
        return

    try:
        avd_ = AVD.get()
    except:
        e = blankValueError(9)
        MainUserGUI.displayError(w, e, lr, ur, aa, apw, va, vpw, vrp, arp, AVD, react, recov, maxSen, vsen, asen,rf)
        return

    try:
        react_ = react.get()
    except _tkinter.TclError:
        e = blankValueError(10)
        MainUserGUI.displayError(w, e, lr, ur, aa, apw, va, vpw, vrp, arp, AVD, react, recov, maxSen, vsen, asen,rf)
        return

    try:
        recov_ = recov.get()
    except _tkinter.TclError:
        e = blankValueError(11)
        MainUserGUI.displayError(w, e, lr, ur, aa, apw, va, vpw, vrp, arp, AVD, react, recov, maxSen, vsen, asen,rf)
        return

    act_ = act.get()

    try:
        max_sen = maxSen.get()
    except _tkinter.TclError:
        e = blankValueError(13)
        MainUserGUI.displayError(w, e, lr, ur, aa, apw, va, vpw, vrp, arp, AVD, react, recov, maxSen, vsen, asen,rf)
        return

    rate_s = rateS.get()

    try:
        a_sen = asen.get()
    except _tkinter.TclError:
        e = blankValueError(15)
        MainUserGUI.displayError(w, e, lr, ur, aa, apw, va, vpw, vrp, arp, AVD, react, recov, maxSen, vsen, asen,rf)
        return
    try:
        v_sen = vsen.get()
    except _tkinter.TclError:
        e = blankValueError(16)
        MainUserGUI.displayError(w, e, lr, ur, aa, apw, va, vpw, vrp, arp, AVD, react, recov, maxSen, vsen, asen,rf)
        return

    try:
        res_fact = rf.get()
    except _tkinter.TclError:
        e = blankValueError(17)
        MainUserGUI.displayError(w, e, lr, ur, aa, apw, va, vpw, vrp, arp, AVD, react, recov, maxSen, vsen, asen,rf)
        return

    p = [pacingMode, lower_rate, upper_rate, atr_amp, atr_pw, ven_amp, ven_pw, vrp_, arp_, avd_,react_, recov_, act_, max_sen, rate_s,v_sen, a_sen,res_fact]

    error = checkParameters(p)

    if (error[0] == 0):
        MainUserGUI.displayError(w,error, lr, ur, aa, apw, va, vpw, vrp, arp, AVD, react, recov,maxSen, vsen, asen,rf)
    elif(error[0] == 1):
        # prints all the values to show they have been stored
        error.append(0)
        error.append("")
        error.append(0)
        MainUserGUI.displayError(w,error, lr, ur, aa, apw, va, vpw, vrp, arp, AVD, react, recov,maxSen, vsen, asen,rf)

        MainUserGUI.set_message(w, pacingMode, lower_rate, upper_rate, atr_amp, atr_pw, ven_amp, ven_pw, vrp_, arp_, avd_,
                                react_, recov_, act_, max_sen, rate_s,v_sen, a_sen,res_fact)

        patient_file.write(pacingMode + "\n")       # 0
        patient_file.write(str(lower_rate) + "\n")  # 1
        patient_file.write(str(upper_rate) + "\n")  # 2
        patient_file.write(str(atr_amp) + "\n")     # 3
        patient_file.write(str(atr_pw) + "\n")      # 4
        patient_file.write(str(ven_amp) + "\n")     # 5
        patient_file.write(str(ven_pw) + "\n")      # 6
        patient_file.write(str(vrp_) + "\n")        # 7
        patient_file.write(str(arp_) + "\n")        # 8
        patient_file.write(str(avd_) + "\n")        # 9
        patient_file.write(str(react_) + "\n")      # 10
        patient_file.write(str(recov_) + "\n")      # 11
        patient_file.write(str(act_) + "\n")        # 12
        patient_file.write(str(max_sen) + "\n")     # 13
        patient_file.write(str(rate_s) + "\n")      # 14
        patient_file.write(str(v_sen) + "\n")       # 15
        patient_file.write(str(a_sen) + "\n")       # 16
        patient_file.write(str(res_fact) + "\n")    # 17

        setFlag = 1

        saveParameters(pacingMode, lower_rate, upper_rate, atr_amp, atr_pw, ven_amp, ven_pw, vrp_, arp_, avd_,react_, recov_, act_, max_sen, rate_s, v_sen, a_sen,res_fact)

        patient_file.close()

def checkParameters(list):

    message = ""

    global AtrAmp_counter
    global VenAmp_counter
    global AtrSens_counter
    global VenSens_counter

    #Check Lower Rate Limit Values--------------------------------------------------------------------------------------
    if(list[1] >= 30 and list[1] <= 175):

        if(list[1] >= 30 and list[1] <=50):
            if(list[1] % 5 != 0):
                message = "Invalid Lower Rate Limit\nIncrementation between 30-50\nmust be divisible by 5"
                return [0,1,message,60]

        elif(list[1] >= 90 and list[1] <=175):
            if(list[1] % 5 != 0):
                message = "Invalid Lower Rate Limit\nIncrementation between 90-175\nmust be divisible by 5"
                return [0,1,message,60]

    elif(list[1] < 30 or list[1] > 175):
        message = "Invalid Lower Rate Limit\nMust be between 30-175 ppm"
        return [0,1, message,60]

    #===================================================================================================================
    #Check Upper Rate Limit---------------------------------------------------------------------------------------------
    if(list[2] >=50 and list[2] <=175):

        if(list[2] % 5 != 0):
            message = "Invalid Upper Rate Limit\nIncrementation between 50-175\nmust be divisible by 5"
            return [0,2, message,120]
    elif (list[2] < 50 or list[2] > 175):
        message = "Invalid Upper Rate Limit\nMust be between 50-175 ppm"
        return [0,2, message,120]

    #===================================================================================================================
    #Check Atrial Amplitude Values--------------------------------------------------------------------------------------
    checkAA = 0
    for i in range(len(amp)):
        if(list[3] == amp[i]):
            checkAA+=1

    if(checkAA == 0):
        AtrAmp_counter = 0
        message = "Invalid Atrial Amplitude\nMust be between 0.1-5.0 V"
        return [0,3,message,5.0]

    #===================================================================================================================
    #Check Atrial Pulse Width Values------------------------------------------------------------------------------------
    if(list[4] < 1 or list[4] > 30):
        message = "Invalid Atrial Pulse Width\nMust be between 1-30 ms"
        return[0,4,message,1]
    #===================================================================================================================
    #Check Ventricular Amplitude Values---------------------------------------------------------------------------------
    checkVA = 0
    for i in range(len(amp)):
        if(list[5] == amp[i]):
            checkVA+=1

    if(checkVA == 0):
        VenAmp_counter = 0
        message = "Invalid Ventricular Amplitude\nMust be between 0.1-5.0 V"
        return [0,5,message,5.0]

    #===================================================================================================================
    #Check Ventricular Pulse Width--------------------------------------------------------------------------------------
    if(list[6] < 1 or list[6] > 30):
        message = "Invalid Ventricular Pulse Width\nMust be between 1-30 ms"
        return [0,6,message,1]

    #===================================================================================================================
    #Check VRP Values---------------------------------------------------------------------------------------------------
    if(list[7] >= 150 and list[7] <= 500):
        if(list[7] % 10 != 0):
            message = "Invalid VRP Values\nIncrementation must be divisible by 10"
            return [0,7,message,320]

    if(list[7] < 150 or list[7] > 500):
        message = "Invalid VRP Values\nMust be between 150-500 ms"
        return [0,7, message,320]

    #===================================================================================================================
    #Check ARP Values---------------------------------------------------------------------------------------------------
    if (list[8] >= 150 and list[8] <= 500):
        if (list[8] % 10 != 0):
            message = "Invalid ARP Values\nIncrementation must be divisible by 10"
            return [0,8, message,250]

    if (list[8] < 150 or list[8] > 500):
        message = "Invalid ARP Values\nMust be between 150-500 ms"
        return [0,8, message,250]

    #===================================================================================================================
    #Check AV Delay Values----------------------------------------------------------------------------------------------
    if (list[9] >= 70 and list[9] <= 300):
        if (list[9] % 10 != 0):
            message = "Invalid AV Delay Values\nIncrementation must be divisible by 10"
            return [0,9, message,150]

    if (list[9] < 70 or list[9] > 300):
        message = "Invalid AV Delay Values\nMust be between 70-300 ms"
        return [0, 9,message,150]

    #===================================================================================================================
    #Reaction Time------------------------------------------------------------------------------------------------------
    if(list[10] >= 10 and list[10] <=50):
        if(list[10] % 10 != 0):
            message = "Invalid Reaction Time Values\nIncrementation must be divisible by 10"
            return [0,10, message,30]

    if(list[10] < 10 or list[10] > 50):
        message = "Invalid Reaction Time Values\nMust be between 10-50 s"
        return [0,10, message,30]

    #===================================================================================================================
    #Recovery Time------------------------------------------------------------------------------------------------------
    if(list[11] < 2 or list[11] > 16):
        message = "Invalid Recovery Time Values\nMust be between 2-16 min"
        return [0,11, message,5]

    #===================================================================================================================
    #Max Sensor Rate----------------------------------------------------------------------------------------------------
    if(list[13] >= 50 and list[13] <= 175):
        if(list[13] % 5 != 0):
            message = "Invalid Max Sensor Rate Values\nIncrementation must be divisible by 5"
            return [0,13,message,120]

    if(list[13] < 50 or list[13] > 175):
        message = "Invalid Max Sensor Rate Values\nMust be between 50-175 ppm"
        return [0,13,message,120]

    #===================================================================================================================
    #Ventricular Sensitivty---------------------------------------------------------------------------------------------
    checkVS = 0
    for i in range(len(sens)):
        if(list[15] == sens[i]):
            checkVS+=1

    if(checkVS == 0):
        VenSens_counter = 0
        message = "Invalid Atrial Sensitivity\nMust be between 0.0-5.0 V"
        return [0,15,message,0]
    #===================================================================================================================
    #Atrial Sensitivity-------------------------------------------------------------------------------------------------
    checkAS = 0
    for i in range(len(sens)):
        if(list[16] == sens[i]):
            checkAS+=1

    if(checkAS == 0):
        AtrSens_counter = 0
        message = "Invalid Atrial Sensitivity\nMust be between 0.0-5.0 V"
        return [0,16,message,0]

    #===================================================================================================================
    #Response Factor----------------------------------------------------------------------------------------------------
    if(list[17] < 1 or list[17] > 16):
        message = "Invalid Response Factor Values\nMust be between 1-16"
        return [0,17,message,8]

    return [1]
# -----------------------------------Increase Button------------------------------------------
def incr(value, typeP):
    # array of values for typeP 4, 6, 9
    global pulse_width
    global activity_threshold
    global sens
    global amp
    global AtrAmp_counter
    global VenAmp_counter
    global AtrSens_counter
    global VenSens_counter
    global Act_Thres_counter

    if (typeP == 1):  # Lower Rate Limit

        if (value.get() >= 90 and value.get() < 175):
            value.set(value.get() + 5)

        elif (value.get() >= 50 and value.get() < 90):
            value.set(value.get() + 1)

        elif (value.get() >= 30 and value.get() < 50):
            value.set(value.get() + 5)
        else:
            value.set(value.get())

    elif (typeP == 2):  # Upper Rate Limit

        if (value.get() >= 50 and value.get() < 175):
            value.set(value.get() + 5)
        else:
            value.set(value.get())

    elif (typeP == 3 or typeP == 5):  # Atrial Amplitude and Ventricular Amplitude

        if(typeP == 3):

            index3 = plus(AtrAmp_counter, len(amp))
            AtrAmp_counter = index3

            if (index3 >= 0 and index3 < len(amp)):
                value.set(amp[index3])

        elif(typeP == 5):

            index5 = plus(VenAmp_counter, len(amp))
            VenAmp_counter = index5

            if (index5 >= 0 and index5 < len(amp)):
                value.set(amp[index5])

    elif (typeP == 4 or typeP == 6):  # Atrial Pulse Width and Ventricular Pulse Width

        if(value.get() >= 1 and value.get() <30):
            value.set(value.get() + 1)

    elif (typeP == 7 or typeP == 8):  # VRP and ARP

        if (value.get() >= 150 and value.get() < 500):
            value.set(value.get() + 10)
        else:
            value.set(value.get())

    elif (typeP == 10):  # AV Delay

        if (value.get() >= 70 and value.get() < 300):
            value.set(value.get() + 10)
        else:
            value.set(value.get())

    elif (typeP == 11):  # Reaction Time

        if (value.get() >= 10 and value.get() < 50):
            value.set(value.get() + 10)
        else:
            value.set(value.get())

    elif (typeP == 12):  # Recovery Time

        if (value.get() >= 2 and value.get() < 16):
            value.set(value.get() + 1)
        else:
            value.set(value.get())

    elif (typeP == 14):

        if (value.get() >= 5 and value.get() < 175):
            value.set(value.get() + 5)
        else:
            value.set(value.get())

    elif (typeP == 15 or typeP == 16):

        if(typeP == 16):
            index16 = plus(AtrSens_counter, len(sens))
            AtrSens_counter = index16

            if (index16 >= 0 and index16 < len(sens)):
                value.set(sens[index16])
        elif(typeP == 15):
            index17 = plus(VenSens_counter, len(sens))
            VenSens_counter = index17

            if (index17 >= 0 and index17 < len(sens)):
                value.set(sens[index17])
    elif(typeP == 17):
        if (value.get() >= 1 and value.get() < 16):
            value.set(value.get() + 1)
        else:
            value.set(value.get())

# -----------------------------------Decrease Button------------------------------------------
def decr(value, typeP):
    # array of values for typeP 4, 6, 9
    global pulse_width
    global activity_threshold
    global sens
    global amp
    global AtrAmp_counter
    global VenAmp_counter
    global AtrSens_counter
    global VenSens_counter
    global Act_Thres_counter

    if (typeP == 1):  # Lower Rate Limit

        if (value.get() > 90 and value.get() <= 175):
            value.set(value.get() - 5)

        elif (value.get() > 50 and value.get() <= 90):
            value.set(value.get() - 1)

        elif (value.get() > 30 and value.get() <= 50):
            value.set(value.get() - 5)
        else:
            value.set(value.get())

    elif (typeP == 2):  # Upper Rate Limit

        if (value.get() > 50 and value.get() <= 175):
            value.set(value.get() - 5)
        else:
            value.set(value.get())


    elif (typeP == 3 or typeP == 5):  # Atrial Amplitude and Ventricular Amplitude

        if (typeP == 3):

            index3 = minus(AtrAmp_counter)
            AtrAmp_counter = index3

            if (index3 >= 0 and index3 < len(amp)):
                value.set(amp[index3])

        elif (typeP == 5):

            index5 = minus(VenAmp_counter)
            VenAmp_counter = index5

            if (index5 >= 0 and index5 < len(amp)):
                value.set(amp[index5])

    elif (typeP == 4 or typeP == 6):  # Atrial Pulse Width and Ventricular Pulse Width

        if(value.get() > 1 and value.get() <=30):
            value.set(value.get() - 1)

    elif (typeP == 7 or typeP == 8):  # VRP and ARP

        if (value.get() > 150 and value.get() <= 500):
            value.set(value.get() - 10)
        else:
            value.set(value.get())

    elif (typeP == 10):  # AV Delay

        if (value.get() > 70 and value.get() <= 300):
            value.set(value.get() - 10)
        else:
            value.set(value.get())

    elif (typeP == 11):  # Reaction Time

        if (value.get() > 10 and value.get() <= 50):
            value.set(value.get() - 10)
        else:
            value.set(value.get())

    elif (typeP == 12):  # Recovery Time

        if (value.get() > 2 and value.get() <= 16):
            value.set(value.get() - 1)
        else:
            value.set(value.get())

    elif (typeP == 14):

        if (value.get() > 50 and value.get() <= 175):
            value.set(value.get() - 5)
        else:
            value.set(value.get())

    elif(typeP == 16 or typeP == 15):

        if(typeP == 16):
            index16 = minus(AtrSens_counter)
            AtrSens_counter = index16

            if (index16 >= 0 and index16 < len(sens)):
                value.set(sens[index16])
        elif(typeP == 15):
            index17 = minus(VenSens_counter)
            VenSens_counter = index17

            if (index17 >= 0 and index17 < len(sens)):
                value.set(sens[index17])

    elif(typeP == 17):
        if (value.get() > 1 and value.get() <= 16):
            value.set(value.get() - 1)
        else:
            value.set(value.get())


def setIndex():

    f = open("" + LoginGUI.user[LoginGUI.name_Flag] + "" + LoginGUI.passw[LoginGUI.name_Flag] + " Parameters.txt", "r")

    global pulse_width
    global activity_threshold
    global sens
    global amp
    global AtrAmp_counter
    global VenAmp_counter
    global AtrSens_counter
    global VenSens_counter

    preSet_values = f.read().splitlines()

    AtrAmp_counter = find(float(preSet_values[3]), amp)
    VenAmp_counter = find(float(preSet_values[5]), amp)
    AtrSens_counter = find(float(preSet_values[16]), sens)
    VenSens_counter = find(float(preSet_values[15]), sens)

def blankValueError(index):

    error_list = [] # [0/1, index, message, default value]

    if(index == 1):
        error_list = [0, index, "Invalid Lower Rate Limit\nCannot Be Blank", 60]

    elif(index == 2):
        error_list = [0, index, "Invalid Upper Rate Limit\nCannot Be Blank", 120]

    elif(index == 3):
        error_list = [0, index, "Invalid Atrial Amplitude\nCannot Be Blank", 5.0]

    elif(index == 4):
        error_list = [0, index, "Invalid Ventricular Amplitude\nCannot Be Blank", 5.0]

    elif (index == 5):
        error_list = [0, index, "Invalid Atrial Pulse Width\nCannot Be Blank", 1]

    elif (index == 6):
        error_list = [0, index, "Invalid Ventricular Pulse Width\nCannot Be Blank", 1]

    elif (index == 7):
        error_list = [0, index, "Invalid VRP\nCannot Be Blank", 320]

    elif (index == 8):
        error_list = [0, index, "Invalid ARP\nCannot Be Blank", 250]

    elif (index == 9):
        error_list = [0, index, "Invalid AV Delay\nCannot Be Blank", 150]

    elif (index == 10):
        error_list = [0, index, "Invalid Reaction Time\nCannot Be Blank", 30]

    elif (index == 11):
        error_list = [0, index, "Invalid Recovery Time\nCannot Be Blank", 5]

    elif (index == 13):
        error_list = [0, index, "Invalid Max Sensor Rate\nCannot Be Blank", 120]

    elif (index == 15):
        error_list = [0, index, "Invalid Atrial Sensitivity\nCannot Be Blank", 0]

    elif (index == 16):
        error_list = [0, index, "Invalid Ventricular Sensitivity\nCannot Be Blank", 0]

    elif (index == 17):
        error_list = [0,index, "Invalid Response Factor\nCannot Be Blank", 8]

    return error_list

