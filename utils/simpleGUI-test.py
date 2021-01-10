import PySimpleGUI as sg
import sqlite3

# sg.Window(title="Hello World", layout=[[]], margins=(200, 50)).read()
# layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button("OK")]]

# WHAT NEEDS TO BE INCLUDED:
# - email
# - name and surname
# - phone number
# - gender
# - date of birth
# - language
# - delivery address
# - zip code (postal code)


def create_new_customer(val):
    connection = sqlite3.connect("../data/delivery-database.db")

    if(len(val[0])) != 7:
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

input_column = [
    [
        sg.Text("Add a New Customer to the Database")
    ],
    [
        sg.Text("New Customer ID (7 letters)"),
        sg.In(size=(25, 1))
    ],
    [
        sg.Text("Gender"),
        sg.In(size=(25, 1))
    ],
    [
        sg.Text("Date of Birth"),
        sg.In(size=(25, 1))
    ],
    [
        sg.Text("Language"),
        sg.In(size=(25, 1))
    ]
]

submit_column = [
    [sg.Button("Add")]
]

layout = [
    [
        sg.Column(input_column),
        sg.Column(submit_column)
    ]
]
# Create the window
window = sg.Window("Demo", layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Add":
        create_new_customer(values)
    elif event == sg.WIN_CLOSED:
        break

window.close()
