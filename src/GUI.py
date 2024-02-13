"""! @file GUI.py
This file creates a graphical interface to trigger a step response function flashed on our microcontroller
"""

import math
import tkinter
from serial import Serial
from matplotlib.figure import Figure
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


def plot_example(plot_axes, plot_canvas, xlabel, ylabel):
    """! This function defines both plots (Theoretical and Experimental).
    It reads data through the serial port, cleans it up, and plots the step response.

    @param plot_axes: The axes on which the plots will be drawn.
    @param plot_canvas: The canvas on which the plots will be displayed.
    @param xlabel: The label for the x-axis.
    @param ylabel: The label for the y-axis.
    """

    time_data = []
    height_data = []
    ser = Serial('/dev/tty.usbmodem204F377739472', timeout=10)
    # Seamus's serial /dev/tty.usbmodem204F377739472
    ser.write(b'\x02')
    ser.write(b'\x04')
    line = ser.readline().decode('utf-8').rstrip().split(",", 1)
    while line[0] != "END":
        try:
            float(line[0])
            float(line[1])
        except (ValueError, IndexError):
            print("exception")
        else:
            time_data.append(float(line[0]))
            height_data.append(float(line[1]))
        finally:
            line = ser.readline().decode('utf-8').rstrip().split(",", 1)
# Calculation of Voltage
    voltage_theory = [3.3*(1 - math.exp((-1)*t/330)) for t in time_data]

    # Draw the plot. Of course, the axes must be labeled. A grid is optional
    plot_axes.plot(time_data, height_data, linestyle='dotted')
    plot_axes.plot(time_data, voltage_theory)
    plot_axes.set_xlabel(xlabel)
    plot_axes.set_ylabel(ylabel)
    plot_axes.legend("ET")
    plot_axes.grid(True)
    plot_canvas.draw()


def tk_matplot(plot_function, xlabel, ylabel, title):
    """! This function is for the GUI program.

    @param plot_function: The function responsible for plotting the data.
    @param xlabel: The label for the x-axis.
    @param ylabel: The label for the y-axis.
    @param title: The title of the GUI window.
    """

    tk_root = tkinter.Tk()
    tk_root.wm_title(title)

    # Create a Matplotlib
    fig = Figure()
    axes = fig.add_subplot()

    # Create the drawing canvas and a handy plot navigation toolbar
    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()

    # Create the buttons that run tests, clear the screen, and exit the program
    button_quit = tkinter.Button(master=tk_root,
                                 text="Quit",
                                 command=tk_root.destroy)
    button_clear = tkinter.Button(master=tk_root,
                                  text="Clear",
                                  command=lambda: axes.clear() or canvas.draw())
    button_run = tkinter.Button(master=tk_root,
                                text="Run Test",
                                command=lambda: plot_function(axes, canvas,
                                                              xlabel, ylabel))

    # Arrange things in a grid because "pack" is weird
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
    toolbar.grid(row=1, column=0, columnspan=3)
    button_run.grid(row=2, column=0)
    button_clear.grid(row=2, column=1)
    button_quit.grid(row=2, column=2)

    # This function runs the program until the user decides to quit
    tkinter.mainloop()


if __name__ == "__main__":
    tk_matplot(plot_example,
               xlabel="Time (ms)",
               ylabel="Voltage (V)",
               title="Step Response")
