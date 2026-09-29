# ******************************************************************
# * *
# * *
# * Example Python program that receives data from an Arduino *
# * *
# * *
# ******************************************************************
import serial
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import time

#
# Note 1: This python script was designed to run with Python 3.
#
# Note 2: The script uses "pyserial" which must be installed. If you have
# previously installed the "serial" package, it must be uninstalled
# first.
#
# Note 3: While this script is running you can not re-program the Arduino.
# Before downloading a new Arduino sketch, you must exit this
# script first.
#
#
# Set the name of the serial port. Determine the name as follows:
# 1) From Arduino's "Tools" menu, select "Port"
# 2) It will show you which Port is used to connect to the Arduino
#
# For Windows computers, the name is formatted like: "COM6"
# For Apple computers, the name is formatted like: "/dev/tty.usbmodemfa141"
#
arduinoComPort = "COM8"
#
# Set the baud rate
# NOTE1: The baudRate for the sending and receiving programs must be the same!
# NOTE2: For faster communication, set the baudRate to 115200 below
# and check that the arduino sketch you are using is updated as well.
#
baudRate = 115200
#
# open the serial port
#
serialPort = serial.Serial(arduinoComPort, baudRate, timeout=1)
time.sleep(2)
#
# main loop to read data from the Arduino, then display it
#


def rawToDistance(raw):
    return (
        1.360319998315560e-04 * raw * raw - 0.216927005444725 * raw + 96.761002374256321
    )

p = None

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(projection = "3d")

color_list = ['#00FF00', "#FFFF00", "#FF0000", "#0000FF"]

custom_cmap = LinearSegmentedColormap.from_list("map", color_list)

ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")
ax.set_title("Scanned Shape")
ax.legend()

while True:
    if serialPort.readline().decode("utf-8").strip() == "Ready":
        print("Arduino is connected and synced!")
        serialPort.flushInput()
        break


while True:
    lineOfData = serialPort.readline().decode()
    print(lineOfData)

    if "Done" in lineOfData:
        serialPort.flushInput()
        break

    if len(lineOfData) > 0:
        data = lineOfData.split(",")
        sensorValue = int(float(data[0]))
        distance = rawToDistance(sensorValue) # in cm
        theta = float(data[1]) * np.pi / 180 # read as deg then converted to rad
        phi = float(data[2]) * np.pi / 180 # read as deg then converted to rad

        print("distance = " + str(sensorValue), end="")
        print(", theta = " + str(theta), end="")
        print(", phi = " + str(phi))

        x = distance * np.sin(theta) * np.cos(phi)
        y = distance * np.sin(theta) * np.sin(phi)
        z = distance * np.cos(theta)
        print(x, y, z)
        if distance <= 60 and distance >= 13 and y <= 35:
            p = ax.scatter(x, y, z, c = y, s = 5, marker = "o", cmap = custom_cmap, vmin = 0, vmax = 35)
cbar = fig.colorbar(p, ax = ax, label = "Continuous Value Scale")
plt.axis('equal')
plt.show()
