import PySimpleGUI as sg
import sqlite3


def run_main_window():
    layoutNav = [
        [
            sg.Text("Welcome to Our Own Special GUI!\nHere's where you can go:", size=(350, 2), justification='center')
        ],
        [
            sg.Button("New Customer", size=(15, 2)),
            sg.Button("Dashboard", size=(15, 2))
        ],
        [
            sg.Button("Close", size=(15, 1), pad=((100,0),(1,1)))
        ]
    ]

    window_navigation = sg.Window("Main", layoutNav, size=(350, 200), element_padding=((20, 20),(10, 10)))

    while True:
        event, values = window_navigation.read()
        if event == "New Customer":
            window_navigation.close()
            run_window_new_customer()
        elif event == "Close" or event == sg.WIN_CLOSED:
            break
    window_navigation.close()


def run_window_new_customer():
    # WHAT NEEDS TO BE INCLUDED:
    # - email
    # - name and surname
    # - phone number
    # - gender
    # - date of birth
    # - language
    # - delivery address
    # - zip code (postal code)
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
            sg.In(size=(25, 1))
        ],
        [
            sg.Text("Year of Birth:", size=(10, 1)),  # drop-down menu or if-condition to check the age
            sg.In(size=(25, 1))
        ],
        [
            sg.Text("Language:", size=(10, 1)),  # drop-down menu
            sg.In(size=(25, 1))
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
            sg.Button("Add", size=(10, 1))
        ]
    ]

    navigation_section = [
        [
            sg.Text("Navigation:")
        ],
        [
            sg.Button("Main", size=(6, 2))
        ],
        [
            sg.Button("Quit", size=(6, 2))
        ]
    ]

    layoutT3 = [
        [
            sg.Column(new_customer_section),
            sg.Column(navigation_section)
        ]
    ]
    window_new_customer = sg.Window("New Customer", layoutT3)
    # Create an event loop
    while True:
        event, values = window_new_customer.read()

        if event == "Add":
            create_new_customer(values)
        elif event == sg.WIN_CLOSED or event == "Quit":
            break
        elif event == "Main":
            window_new_customer.close()
            run_main_window()

    window_new_customer.close()


def create_new_customer(val):
    connection = sqlite3.connect("../data/delivery-database.db")

    if (len(val[0])) != 7:
        print("The ID should be exactly 7 letters long!")
        pass
    else:
        print("Adding the following values: ", val)

        cursor = connection.cursor()

        sql_command = f"""
        INSERT INTO customers(akeed_customer_id, gender, 
        dob, status, verified, language, created_at, updated_at)
        VALUES ('{str(val[0]).upper()}', NULLIF('{str(val[1])}', ''), NULLIF('{val[2]}', ''), 0, 0, NULLIF('{str(val[3])}', ''), 
            datetime('now', 'localtime'), datetime('now', 'localtime')
            );
        """
        cursor.execute(sql_command)
        connection.commit()

    connection.close()


# MAIN
run_main_window()
