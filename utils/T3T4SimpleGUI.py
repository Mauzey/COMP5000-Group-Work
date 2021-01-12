import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import re

def run_window_main():
    layoutNav = [
        [
            sg.Text("Welcome to Our Very Special GUI!\nHere's where you can go:", size=(350, 2), justification='center')
        ],
        [
            sg.Button("New Customer", size=(15, 2)),
            sg.Button('Dashboard', size=(15, 2))
        ],
        [
            sg.Button('Quit', size=(15, 1), pad=((100, 0), (1, 1)))
        ]
    ]

    window_navigation = sg.Window("Main", layoutNav, size=(350, 200), element_padding=((20, 20), (10, 10)))

    while True:
        event, values = window_navigation.read()
        if event == "New Customer":
            window_navigation.close()
            run_window_new_customer()

        elif event == 'Dashboard':
            window_navigation.close()
            run_window_dashboard()

        elif event in (None, 'Quit'):
            break
    window_navigation.close()


def email_validation_window():
    layout = [[sg.Text('The email is incorrect!\nPlease enter correct format:\n****@***.***')],
              [sg.OK()]]

    window = sg.Window('Second Form', layout)
    event, values = window.read()
    window.close()


def run_window_new_customer():

    gender_values = ['Male', 'Female', 'Other']
    dob_values = []
    for i in range(1925, 2005):
        dob_values.append(i)

    lan_values = ['EN', 'RU', 'ES', 'FR', 'AR']
    new_customer_section = [
        [
            sg.Text("Create a New Account")
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
            sg.Text("Year of Birth:", size=(15, 1)),  # drop-down menu or if-condition to check the age
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
            sg.Text("Navigation:")
        ],
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

    window_new_customer = sg.Window("New Customer", layout_customer)

    # Create an event loop
    while True:
        event, values = window_new_customer.read()

        if event == 'Add':

            email_valid = re.search('.*@.*(\.).+', values['email'])
            if email_valid:
                print("Adding the following values to the 'customers' table:\n", values)
                sql_command = f"""
                                        INSERT INTO customers (akeed_customer_id, gender, 
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
                email_validation_window()

        elif event in (None, 'Quit'):
            break
        elif event == 'Main':
            window_new_customer.close()
            run_window_main()

    window_new_customer.close()


def run_window_dashboard():

    navigation_section = [
        [
            sg.Text("Navigation:")
        ],
        [
            sg.Button('Main', size=(6, 2))
        ],
        [
            sg.Button('Quit', size=(6, 2))
        ]
    ]

    plot_layout = [
        [
            sg.Button("Oh Come the Great Histogram!", key='hist')
        ],
        [
            sg.Canvas(size=(300 * 2, 300), key='plot_canvas', background_color='grey')
        ]
    ]

    dashboard_section = [
        [
            # • Print the mean ’item count’ (number of items per order)
            sg.Button("Mean Item Count", key='mean_num', size=(20,1), tooltip="Average Number of Items Per Order"),
            sg.Text(size=(20, 1), key='mean_num_out')
        ],
        [
            # • Print the mean ’grand total’ (cost of the order)
            sg.Button("Mean Grand Total", key='mean_cost', size=(20,1), tooltip="Average Cost Of an Order"),
            sg.Text(size=(20, 1), key='mean_cost_out')
        ],
        [
            # • Plot a histogram of the ’delivery distance’
            sg.Frame("Here the Greatest Histogram of The Century Shall Be Displayed:", plot_layout)
        ]
    ]

    layout_dshb = [
        [
            sg.Column(dashboard_section),
            sg.Column(navigation_section)
        ]
    ]
    window_dashboard = sg.Window("New Customer", layout_dshb, force_toplevel=True, finalize=True)

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

            plt.figure(1)
            fig = plt.gcf()  # if using Pyplot then get the figure from the plot
            DPI = fig.get_dpi()

            fig.set_size_inches(304 * 2 / float(DPI), 304 / float(DPI))

            plt.hist(delivery_distance)
            plt.xlabel("Distance")
            plt.title("Delivery Distance Histogram")
            plt.xticks(rotation='vertical')

            draw_plot(fig, window_dashboard['plot_canvas'].TKCanvas)


    window_dashboard.close()


def run_sql_command(command):
    global dbFile

    connection = sqlite3.connect(dbFile)
    cursor = connection.cursor()
    cursor.execute(command)
    result = cursor.fetchall()

    connection.commit()
    connection.close()

    return result


def draw_plot(figure, canvas):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()

    figure_canvas_agg = FigureCanvasTkAgg(figure, master=canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)


# MAIN
dbFile = "../data/delivery-database.db"
run_window_main()
