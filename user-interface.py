# user-interface.py
#
# Task 3: Write a GUI interface (using tkinter for example) to input new customers into the database.
#
# Task 4: Provide a simple GUI dashboard. Clicking on buttons should provide the following information from the SQLite
#         database via SQL:
#           - Print the mean 'item_count' (number of items per order)
#           - Print the mean 'grand_total' (cost of the order)
#           - Plot a histogram of the 'delivery_distance' in the 'orders' table

# Import dependencies --------------------------------------------------------------------------------------------------
import tkinter as tk
import os

# Define constants -----------------------------------------------------------------------------------------------------
LARGE_FONT = ('Verdana', 12)


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)  # Initialize tkinter

        # Instantiate tkinter window_new_customer
        window = tk.Frame(self)
        window.pack(side='top', fill='both', expand=True)
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        #
        self.frames = {}
        frame = SplashPage(window, self)
        self.frames[SplashPage] = frame

        frame.grid(row=0, column=0, sticky='nsew')  # Position the frame

        self.show_frame(SplashPage)

    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()  # Bring the frame to the top


def create_db():
    os.system("python3 ./utils/create-database.py")


class SplashPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Title label
        title_label = tk.Label(self, text="COMP5000 | Database Interface", font=LARGE_FONT)
        title_label.pack(padx=10, pady=10)

        # If a database doesn't exist locally, prompt the user to create and populate a database
        if not os.path.exists("./delivery-database.db"):
            btn_create_db = tk.Button(self, text="Create and Populate Database", command=create_db)
            btn_create_db.pack()
        # Otherwise, prompt the user to import the existing data
        else:
            btn_import_db = tk.Button(self, text="Import Database")
            btn_import_db.pack()


app = App()
app.mainloop()
