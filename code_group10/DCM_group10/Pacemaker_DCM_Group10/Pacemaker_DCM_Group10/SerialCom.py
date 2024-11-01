from MainUserData import *
import serial
import struct
from CommonFunctions import *
import serial.tools.list_ports
import MainUserGUI
import time
import threading
from tkinter import *
s = serial.Serial()

MODE = -1
SENT = -1
flag = -1

def saveParameters(pacingMode, lower_rate, upper_rate, atr_amp, atr_pw, ven_amp, ven_pw, vrp_, arp_, avd_,
                react_, recov_, act_, max_sen, rate_s,v_sen, a_sen,res_fact):
    flag = 0
    global s, MODE,SENT
    SENT = 0
    checkConnection()
    mode = 0
    act_thres = 0

    #Converting pacingMode -> mode to an integer
    if(pacingMode == "AOO"):
        mode = 0
    elif(pacingMode == "VOO"):
        mode = 1
    elif (pacingMode == "AAI"):
        mode = 2
    elif (pacingMode == "VVI"):
        mode = 3
    elif (pacingMode == "DOO"):
        mode = 4
    elif (pacingMode == "AOOR"):
        mode = 5
    elif (pacingMode == "VOOR"):
        mode = 6
    elif (pacingMode == "AAIR"):
        mode = 7
    elif (pacingMode == "VVIR"):
        mode = 8
    elif (pacingMode == "DOOR"):
        mode = 9

    MODE = mode
    #Converting act_ -> act_thres to an integer
    if (act_ == "V-Low"):
        act_thres = 0.003
    elif (act_ == "Low"):
        act_thres = 0.008
    elif (act_ == "Med-Low"):
        act_thres = 0.01
    elif (act_ == "Med"):
        act_thres = 0.08
    elif (act_ == "Med-High"):
        act_thres = 0.5
    elif (act_ == "High"):
        act_thres = 0.9
    elif (act_ == "V-High"):
        act_thres = 1.2

    toSend = [22,18,mode, lower_rate, upper_rate, atr_amp, atr_pw, ven_amp, ven_pw, vrp_, arp_, avd_,
                react_, recov_, act_thres, max_sen, rate_s,v_sen, a_sen,res_fact]

    sequence = "<BBHHHfHfHHHHHHdHHffH"

    #print("------------------------------------------Sending Data-------------------------------------------------")
    #print("To Send: ")
    #print(toSend)
    send(toSend, sequence)

    echo = echoParameters()

    SENT = 1

def send(toSend, sequence):

    packet = []

    assert(len(sequence[1:]) == len(toSend)), "patterns and arrays are not always equal"
    endian = sequence[0]
    sequence = sequence[1:]


    for i in range(0, len(toSend)):
        data = struct.pack(endian+sequence[i],toSend[i])
        packet.append(data)

    #print("Send in Bytes")
    #print(packet)
    for pac in packet:
        s.write(pac)


def echoParameters():

    global s

    #print("------------------------------------------Receive Data-------------------------------------------------")

    bits_toStartEcho = [22,22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    sequence = "<HHHfHfHHHHHHdHHffHdd"
    start_Sequence = "<BBHHHfHfHHHHHHdHHffH"

    send(bits_toStartEcho,start_Sequence)

    echo = s.read(66)
    echo = list(unpack(sequence,echo))

    #print("ECHO: ")
    #print(echo)

    return echo
#Get AV Signal
def getAVSignal():
    signal = echoParameters()

    signal = signal[-2:]

    return signal
#Connection Checker-----------------------------------------------------------------------------------------------------
def checkConnection():
    global s
    connection = ""
    myPorts = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    try:
        try:
            s = serial.Serial('COM8', 115200)
        except:
            connection_Error = True
        pacemaker = [port for port in myPorts if s.port in port][0]
        connection = "Connected"
        MainUserGUI.isConnected = True
    except serial.serialutil.SerialException:
        connection = "Disconnected 1"
        MainUserGUI.isConnected = False
    except IndexError:
        connection = "Disconnected 2"
        MainUserGUI.isConnected = False



def connection(window):

    global s

    connection = ""
    myPorts = [tuple(p) for p in list(serial.tools.list_ports.comports())]

    try:
        try:
            s = serial.Serial('COM8', 115200)
        except:
            connection_Error = True
        pacemaker = [port for port in myPorts if s.port in port][0]
        connection = "Connected"
        MainUserGUI.isConnected = True
    except serial.serialutil.SerialException:
        connection = "Disconnected 1"
        MainUserGUI.isConnected = False
    except IndexError:
        connection = "Disconnected 2"
        MainUserGUI.isConnected = False

    # Device Connection
    if (MainUserGUI.isConnected == True):
        colour = "green"
        connect = "Pacemaker Connected"
    elif (MainUserGUI.isConnected == False):
        colour = "red"
        connect = "Pacemaker Disconnected"

    canvas = Canvas(window, height=20, width=20, bg=colour)

    canvas.place(x=470, y=665)

    canvas.create_rectangle(0, 0, 200, 200, outline="black", fill=colour)

    connection = Label(window,
                       text=connect,
                       font="Arial 13",
                       anchor = W,
                       width = 25,
                       bg=rgb_picker(102, 192, 255)).place(x=495, y=665)

    # New Device
    if (MainUserGUI.isNewDevice == False and MainUserGUI.isConnected == True):
        colour = "green"
        connect = "Previously Integrated Device"
    elif (MainUserGUI.isNewDevice == True and MainUserGUI.isConnected == True):
        colour = "red"
        connect = "Newly Integrated Device"
    elif (MainUserGUI.isConnected == False):
        colour = "orange"
        connect = "No Device Detected"

    canvas = Canvas(window, height=20, width=20, bg=colour)

    canvas.place(x=700, y=662)

    canvas.create_rectangle(0, 0, 200, 200, outline="black", fill=colour)

    connection = Label(window,
                       text=connect,
                       font="Arial 13",
                       anchor = W,
                       width = 25,
                       bg=rgb_picker(102, 192, 255)).place(x=725, y=662)


