# ******************************************************************
# * *
# * *
# * Example Python program that receives data from an Arduino *
# * *
# * *
# ******************************************************************
import serial
import matplotlib.pyplot as plt
import numpy as np
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
arduinoComPort = "COM7"
#
# Set the baud rate
# NOTE1: The baudRate for the sending and receiving programs must be the same!
# NOTE2: For faster communication, set the baudRate to 115200 below
# and check that the arduino sketch you are using is updated as well.
#
baudRate = 9600
#
# open the serial port
#
serialPort = serial.Serial(arduinoComPort, baudRate, timeout=1)
#
# main loop to read data from the Arduino, then display it
#

# 1. Setup the figure and 3D axes
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(projection='3d')

# # 2. Generate sample data (a 3D spiral helix)
# z = np.linspace(0, 15, 100)
# x = np.sin(z)
# y = np.cos(z)

# # 3. Plot a continuous 3D line
# ax.plot(x, y, z, label='3D Parametric Spiral', color='blue', linewidth=2)

# # 4. Add some random 3D scatter points
# xs = np.random.uniform(-1, 1, 30)
# ys = np.random.uniform(-1, 1, 30)
# zs = np.random.uniform(0, 15, 30)
# ax.scatter(xs, ys, zs, color='red', marker='o', s=40, label='Random Points')

# 5. Label your dimensions
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')
ax.set_title('3D Line & Scatter Plot')
ax.legend()

iterations = 0

while True and iterations < 50:
    #
    # ask for a line of data from the serial port, the ".decode()" converts the
    # data from an "array of bytes", to a string
    #
    lineOfData = serialPort.readline().decode()
    #
    # check if data was received
    #
    if len(lineOfData) > 0:
    #
    # data was received, convert it into 3 integers
    #
        data = (x for x in lineOfData.split(','))
        # data = np.fromstring(lineOfData, dtype = float, sep = ",")
        sensorValue = int(data[0])
        theta = data[1] * np.pi / 180
        phi = data[2] * np.pi / 180
        #
        # print the results
        #
        print("sensorValue = " + str(sensorValue), end = "")
        print(", theta = " + str(theta), end = "")
        print(", phi = " + str(phi))
        iterations += 1
        x = sensorValue * np.cos(theta) * np.cos(phi)
        y = sensorValue * np.cos(theta) * np.sin(phi)
        z = sensorValue * np.sin(theta)
        ax.scatter(x, y, z, color='red', s=100, marker='o')
plt.show()