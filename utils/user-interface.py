import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import re


def run_sql_command(command):
    """This function runs the provided SQL command with the help of sqlite3

    :param command : <class 'str'>
        the string with the sql command which is to be executed

    :return result: <class 'list'>
        the resulting list of values after running the sql operation on the database
        (or empty value if the sql command isn't supposed to return any value
        and/or simply does some operations on a database)
    """

    global dbFile
    # the dbFile variable is defined in the main body of the program only once,
    # beyond the scope of other functions

    connection = sqlite3.connect(dbFile)
    cursor = connection.cursor()
    cursor.execute(command)
    result = cursor.fetchall()

    connection.commit()
    connection.close()

    return result


def draw_plot(figure, canvas):
    """
    This function fills the provided canvas object with the provided plot figure.

    :param figure: <class 'matplotlib.figure.Figure'>
        the figure that holds the plot to be displayed in the canvas
    :param canvas: <class 'type'>
        canvas object in PySimpleGUI which will hold the provided figure (plot)
    """

    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()

    figure_canvas_agg = FigureCanvasTkAgg(figure, master=canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='bottom', fill='both', expand=1, pady=1, padx=1)


def email_validation_window():
    """
    This function runs a window that occurs if the user email is entered incorrectly.

    Once the user presses 'OK' button,
    the current window closes and they get back to the 'New Customer' window.

    :return <class 'bool'>
    The function returns True of the button OK is pressed or window is closed
    """

    layout = [[sg.Text('ERROR:\nThe email format should be:\n****@***.***')],
              [sg.OK()]]

    window = sg.Window('Email Format Error', layout)
    event, values = window.read()
    window.close()
    return True


def run_window_main():
    """
    This function runs the main navigation window.

    With pressing the 'New Customer' button the current window closes and the 'New Customer' window opens.
    With pressing the 'Dashboard' button the current window closes and the 'Dashboard' window opens.
    The current window closes and the program finishes if the 'Quit' or the red 'X' (in the upper window corner)
    buttons are pressed.
    """

    layoutNav = [
        [
            sg.Text("Welcome to Our Very Special GUI!\nHere's where you can go:", size=(350, 2),
                    justification='center')
        ],
        [
            sg.Button("New Customer", size=(15, 2)),
            sg.Button('Dashboard', size=(15, 2))
        ],
        [
            sg.Button('Quit', size=(15, 1), pad=((100, 0), (1, 1)))
        ]
    ]

    # new layout needs to be specified each time a window is created, the same layout cannot be reused by
    # different windows as per PySimpleGUI principles, hence we had to put it in a function

    window_navigation = sg.Window("Main", layoutNav, size=(350, 200), element_padding=((20, 20), (10, 10)))

    # event loop for the window
    while True:

        # 'values' represent the input values in the input fields
        event, values = window_navigation.read()

        # in our case event names represent the buttons names,
        # however it can be specific keys assigned to certain elements of a window if it can trigger an event
        if event == "New Customer":
            window_navigation.close()
            run_window_new_customer()  # launching a function which opens the window for Task 3 - new customer

        elif event == 'Dashboard':
            window_navigation.close()
            run_window_dashboard()  # launching a function which opens the window for Task 4 - dashboard

        # in case the user presses the 'Quit' button or the red 'close' button on the top of the window
        elif event in (None, 'Quit'):
            break
    window_navigation.close()


def run_window_new_customer():
    """
    This function runs a 'New Customer' window.

    The window runs as long as it's not closed by the customer
    with buttons 'Quit' or usual red 'X' button in the upper corner of the window.
    It has input fields and the button 'Add' which adds a record of a new customer to the 'Customers' table.
    In order to do so, it uses 'run_sql_command' function
    """

    # gender_values, dob_values and lan_values are to be displayed in drop-down menus (element 'Combo')
    gender_values = ['Male', 'Female', 'Other']

    dob_values = []
    for i in range(1925, 2005):
        dob_values.append(i)

    lan_values = ['EN', 'RU', 'ES', 'FR', 'AR']

    # creating new layouts for our window
    new_customer_section = [
        [
            sg.Text("Create a New Account", font='Calibri 14 bold')
        ],
        [
            sg.Text("Name:", size=(15, 1)),
            sg.In(size=(25, 1))
        ],
        [
            sg.Text("Surname:", size=(15, 1)),
            sg.In(size=(25, 1))
        ],
        [
            sg.Text("Email:", size=(15, 1)),  # validate the email
            sg.Input(tooltip="Email should have format ****@***.***", size=(25, 1), key='email')
        ],
        [
            sg.Text("Gender:", size=(15, 1)),  # drop-down menu
            sg.Combo(values=gender_values, size=(25, 1), key='gender')
        ],
        [
            sg.Text("Year of Birth:", size=(15, 1)),  # drop-down menu
            sg.Combo(values=dob_values, size=(25, 1), key='dob')
        ],
        [
            sg.Text("Language:", size=(15, 1)),  # drop-down menu
            sg.Combo(values=lan_values, size=(25, 1), key='lan')
        ],
        [
            sg.Text("Delivery Address:", size=(15, 1)),
            sg.In(size=(25, 1))
        ],
        [
            sg.Text("Postal Code:", size=(15, 1)),
            sg.In(size=(25, 1))
        ],
        [
            sg.Button('Add', size=(15, 1))
        ]
    ]

    navigation_section = [

        [
            sg.Button('Main', size=(6, 2))
        ],
        [
            sg.Button('Quit', size=(6, 2))
        ]
    ]

    layout_customer = [
        [
            sg.Column(new_customer_section),
            sg.Column(navigation_section)
        ]
    ]

    window_new_customer = sg.Window("New Customer", layout_customer,
                                    element_padding=((5, 5), (5, 5)))

    # Event loop
    while True:
        event, values = window_new_customer.read()

        if event == 'Add':

            email_valid = re.search(".*@.*(\.).+", values['email']) #validating the entered email address
            if email_valid:
                # print("Adding the following values to the 'customers' table:\n", values)
                sql_command = f"""      INSERT INTO customers (akeed_customer_id, gender, 
                                                            dob, status, verified, language, 
                                                            created_at, updated_at)
                                        VALUES ('test12/01/2021', NULLIF('{values['gender']}', ''), 
                                            NULLIF('{values['dob']}', ''), 0, 0, NULLIF('{values['lan']}', ''), 
                                            datetime('now', 'localtime'), datetime('now', 'localtime')
                                            );
                                        """

                run_sql_command(sql_command)
                del sql_command
            else:
                # disabling the current window for the input
                # and displaying a warning window for incorrect email
                window_new_customer.disable()
                if email_validation_window():
                    window_new_customer.enable()

        elif event in (None, 'Quit'):
            break
        elif event == 'Main':
            # closing the current window without submitting anything and switching back to Main
            window_new_customer.close()
            run_window_main()

    window_new_customer.close()


def run_window_dashboard():
    """
    This function runs a 'Dashboard' window.

    With the help of buttons the average number of items per order and average cost of an order are displayed.
    By pressing the 'Plot The Histogram' button the customer can display the histogram plot of
    the delivery distance for orders. In order to do so, the 'draw_plot' as well as
    'run_sql_command' functions are used .
    """

    navigation_section = [

        [
            sg.Button('Main', size=(6, 2))
        ],
        [
            sg.Button('Quit', size=(6, 2))
        ]
    ]

    plot_layout = [
        [
            sg.Button('Plot The Histogram', key='hist',
                      tooltip='The graph changes its colors each time this button is pressed')
        ],
        [
            # the Canvas section is visible before displaying the plot there, as soon as the window is run
            sg.Canvas(size=(300 * 2, 400), key='plot_canvas', background_color='lightgrey')
        ]
    ]

    dashboard_section = [
        [
            sg.Text("Welcome to the Dashboard!", font='Calibri 14 bold')
        ],
        [
            # Print the mean ’item count’ (number of items per order)
            sg.Button("Mean Item Count", key='mean_num', size=(20,1), tooltip="Average Number of Items Per Order"),
            sg.Text(size=(20, 1), key='mean_num_out')
        ],
        [
            # Print the mean ’grand total’ (cost of the order)
            sg.Button("Mean Grand Total", key='mean_cost', size=(20,1), tooltip="Average Cost Of an Order"),
            sg.Text(size=(20, 1), key='mean_cost_out')
        ],
        [
            # Plot a histogram of the ’delivery distance’
            sg.Frame('Delivery Distance Histogram', plot_layout)
        ]
    ]

    layout_dshb = [
        [
            sg.Column(dashboard_section),
            sg.Column(navigation_section)
        ]
    ]
    window_dashboard = sg.Window("Dashboard", layout_dshb,
                                 size=(750, 600),
                                 element_padding=((5, 5), (5, 5)))

    # Create an event loop
    while True:
        event, values = window_dashboard.read()

        if event in (None, 'Quit'):
            break

        elif event == 'Main':
            window_dashboard.close()
            run_window_main()

        elif event == 'mean_num':
            sql_command = """
                SELECT AVG(item_count) 
                FROM orders;
            """
            number = run_sql_command(sql_command)
            del sql_command

            window_dashboard['mean_num_out'].update(round(number[0][0], 2))

        elif event == 'mean_cost':
            sql_command = """
                SELECT AVG(grand_total) 
                FROM orders;
            """
            number = run_sql_command(sql_command)
            del sql_command

            window_dashboard['mean_cost_out'].update(round(number[0][0], 3))

        elif event == 'hist':

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

            # plt.style.use('seaborn-pastel')
            plt.hist(delivery_distance, bins=range(15))
            plt.xlabel("Distance")
            plt.title("Delivery Distance Histogram")
            plt.xticks(rotation='vertical')
            plt.tight_layout()

            # putting the plot in the canvas
            # source: https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Matplotlib_Embedded_Toolbar.py
            fig = plt.gcf()  # if using Pyplot then get the figure from the plot
            DPI = fig.get_dpi()

            # fixing the size of the plot to make sure it doesn't expand drastically and fits the canvas
            fig.set_size_inches(304 * 2 / float(DPI), 404 / float(DPI))

            draw_plot(fig, window_dashboard['plot_canvas'].TKCanvas)

    window_dashboard.close()


# MAIN
dbFile = "../data/delivery-database.db"

# setting window theme and fonts before launching the first window
sg.theme('LightBlue3')
sg.set_options(font="Calibri 12", tooltip_font="Calibri 10 italic")

run_window_main()
