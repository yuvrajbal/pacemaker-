# Common Functions
from struct import *
# ----------------------------------------RGB Picker------------------------------------------
def rgb_picker(r, g, b):  # takes in 3 integers for red, green, and blue and returns hexadecimal
    # of the colour

    # converting decimal to hexdecimal
    tempR = hex(r)
    r_16 = tempR[2:]  # take substring

    tempG = hex(g)
    g_16 = tempG[2:]  # take substring

    tempB = hex(b)
    b_16 = tempB[2:]  # take substring

    rgb = "#" + r_16 + g_16 + b_16;  # concatenate

    rgb = rgb.upper()  # convert to uppercase letters

    return rgb  # return value


# --------------------------------Increment/Decrement-----------------------------------------
# incrementer function to move through the array when button is pushed
# these functions were designed to increment through an array
# the values of the pulse width for A and V are stored in an array since they
# are doubles, they were being incremented incorrectly so they were stored in an array
# and being sent back to the function
# ----------------------------Plus/Minus Functions--------------------------------------------
def plus(x, length):
    if (x < length):
        x = x + 1

    return x

def minus(x):
    if (x > 0):
        x = x - 1

    return x

#---------------------------------Find Index------------------------------------------
def find(var,list):

    length = len(list)
    x = 0
    for i in range(length):
        if(list[i] == var):
            x = i
            break

    return x

