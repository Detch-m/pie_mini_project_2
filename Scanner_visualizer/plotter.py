import serial
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import time
import csv

arduinoComPort = "COM5"
baudRate = 115200
serialPort = serial.Serial(arduinoComPort, baudRate, timeout=1)
time.sleep(2)


def raw_to_distance(raw: float):
    """convert the sensor reading (raw) into distances"""
    return (
        1.360319998315560e-04 * raw * raw - 0.216927005444725 * raw + 96.761002374256321
    )


p = None
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(projection="3d")
color_list = ["#00FF00", "#FFFF00", "#FF0000", "#0000FF"]
custom_cmap = LinearSegmentedColormap.from_list("map", color_list)
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")
ax.set_title("Scanned Shape")
ax.legend()
points = []


def start_scan():
    """Start the scanning behavior

    This function first waits for the handshake agreement from the sensor
    to arrive, then begins reading the data. It converts the data into distances,
    and plots it according to algebraic properties. It also appends data to list
    of points in order to be used for other operations.
    """
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
            distance = raw_to_distance(sensorValue)  # in cm
            theta = float(data[1]) * np.pi / 180  # read as deg then converted to rad
            phi = float(data[2]) * np.pi / 180  # read as deg then converted to rad

            print("distance = " + str(sensorValue), end="")
            print(", theta = " + str(theta), end="")
            print(", phi = " + str(phi))

            x = distance * np.sin(theta) * np.cos(phi)
            y = distance * np.sin(theta) * np.sin(phi)
            z = distance * np.cos(theta)

            point_at = [x, y, z]
            points.append(point_at)

            print(x, y, z)
            if distance <= 60 and distance >= 13 and y <= 35:
                p = ax.scatter(
                    x, y, z, c=y, s=5, marker="o", cmap=custom_cmap, vmin=0, vmax=35
                )
    cbar = fig.colorbar(p, ax=ax, label="Continuous Value Scale")
    plt.axis("equal")
    plt.show()


def save_data(data):
    """Saves the points into a csv

    This function saves the points into a csv and must be used after startScan is ran.
    It will save it to 'output.csv' in the same folder and running it again will overwrite
    the previous data.

    Parameters:
        data, representing a list of points (where points represent a list of x,y,z coordinates)
    """
    headers = ["x", "y", "z"]
    with open("output.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(headers)

        # Write all data rows at once
        writer.writerows(data)

    print("successful data saved!")


def plot_from_csv(data=None):
    """Plots the data from a csv

    This function read the points from a csv and must be used after saveData is ran.
    It will read from to 'output.csv' in the same folder. It is possible to run it without
    save_data if data has been stored before from a start_scan run and passed into the function

    Parameters:
        data, representing a list of points (where points represent a list of x,y,z coordinates)
    """
    local_data = []
    if data is None:
        with open("output.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # skip the header row
            for row in reader:
                local_data.append([float(v) for v in row])
    else:
        local_data = data

    points_array = np.array(local_data, float)
    x, y, z = points_array[:, 0], points_array[:, 1], points_array[:, 2]

    figure3d = plt.figure()
    ax2 = figure3d.add_subplot(projection="3d")
    scattered = ax2.scatter(x, y, z, c=y, s=5, marker="o", cmap=custom_cmap)
    figure3d.colorbar(scattered, ax, label="Y value")
    ax2.set_xlabel("X Axis")
    ax2.set_ylabel("Y Axis")
    ax2.set_zlabel("Z Axis")
    ax2.set_title("Scanned Shape (from CSV)")
    ax2.set_box_aspect([1, 1, 1])
    plt.show()


def main():
    """Runs the scan and saves it to a csv; option to plot from csv"""
    # start_scan()
    # save_data(points)
    # plot_from_csv()


if __name__ == "__main__":
    main()
