import PySimpleGUI as sg
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

def run_sql_command(command):

    connection = sqlite3.connect("../data/delivery-database.db")
    cursor = connection.cursor()
    cursor.execute(command)
    result = cursor.fetchall()

    connection.commit()
    connection.close()

    return result

sql_command = """
                SELECT delivery_distance 
                FROM orders;
            """
distance_list = run_sql_command(sql_command)
del sql_command

delivery_distance = []

for i in distance_list:
    delivery_distance.append(i[0])

del distance_list

# plt.figure()

plt.hist(delivery_distance)
plt.xlabel("Distance")
plt.title("Delivery Distance Histogram")
plt.xticks(rotation='vertical')

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


# ------------------------------- Beginning of GUI CODE -------------------------------

fig = plt.gcf()  # if using Pyplot then get the figure from the plot
figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds

# define the window layout
layout = [[sg.Text('Plot test', font='Any 18')],
          [sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')]]

# create the form and show it without the plot
window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI',
    layout, force_toplevel=True, finalize=True)

# add the plot to the window
fig_photo = draw_figure(window['-CANVAS-'].TKCanvas, fig)

# show it all again and get buttons
event, values = window.read()

window.close()
