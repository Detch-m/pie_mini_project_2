# ******************************************************************
# * *
# * *
# * Example Python program that receives data from an Arduino *
# * *
# * *
# ******************************************************************
import serial

arduinoComPort = "COM5"
baudRate = 9600
serialPort = serial.Serial(arduinoComPort, baudRate, timeout=1)


def processReadings():
    pass


def plotReadings():
    pass


def main():
    pass


while True:
    #
    # ask for a line of data from the serial port, the ".decode()" converts the
    # data from an "array of bytes", to a string
    #
    lineOfData = serialPort.readline().decode()

    if len(lineOfData) > 0:

        print(lineOfData)
