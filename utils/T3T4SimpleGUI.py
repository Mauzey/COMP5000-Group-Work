import PySimpleGUI as sg
import sqlite3


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


def run_window_new_customer():
    new_customer_section = [
        [
            sg.Text("Create a New Account")
        ],
        [
            sg.Text("Name:", size=(10, 1)),
            sg.In(size=(25, 1))
        ],
        [
            sg.Text("Surname:", size=(10, 1)),
            sg.In(size=(25, 1))
        ],
        [
            sg.Text("Email:", size=(10, 1)),  # validate the email
            sg.In(size=(25, 1))
        ],
        [
            sg.Text("Gender:", size=(10, 1)),  # drop-down menu
            sg.In(size=(25, 1), key='gender')
        ],
        [
            sg.Text("Year of Birth:", size=(10, 1)),  # drop-down menu or if-condition to check the age
            sg.In(size=(25, 1), key='dob')
        ],
        [
            sg.Text("Language:", size=(10, 1)),  # drop-down menu
            sg.In(size=(25, 1), key='lan')
        ],
        [
            sg.Text("Delivery Address:", size=(10, 1)),
            sg.In(size=(25, 1))
        ],
        [
            sg.Text("Postal Code:", size=(10, 1)),
            sg.In(size=(25, 1))
        ],
        [
            sg.Button('Add', size=(10, 1))
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
            print("Adding the following values to the 'customers' table:\n", values)
            sql_command = f"""
                        INSERT INTO customers (akeed_customer_id, gender, 
                                            dob, status, verified, language, 
                                            created_at, updated_at)
                        VALUES ('test123', NULLIF('{values['gender']}', ''), 
                            NULLIF('{values['dob']}', ''), 0, 0, NULLIF('{values['lan']}', ''), 
                            datetime('now', 'localtime'), datetime('now', 'localtime')
                            );
                        """

            run_sql_command(sql_command)
            del sql_command

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
    window_dashboard = sg.Window("New Customer", layout_dshb)
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
            draw_plot(delivery_distance)



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


def draw_plot(numbers):
    print("Test")


# Task 3 (20 marks) Write a GUI interface, using for example Tkinter, to input new customers
# to the database. Provide screen-shots of the software being used.
# Task 4 (25 marks) Use Tkinter or another python system to provide a simple GUI dashboard.
# Clicking on buttons should provide the following information from the SQLite database
# via SQL.
# • Print the mean ’item count’ (number of items per order)
# • Print the mean ’grand total’ (cost of the order)
# • Plot a histogram of the ’deliverydistance’.

# MAIN
dbFile = "../data/delivery-database.db"
run_window_main()
