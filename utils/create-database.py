# Import dependencies --------------------------------------------------------------------------------------------------
import os
import pandas as pd
import sqlite3

# Establish database connection
connection = sqlite3.connect("./delivery-database.db")
cursor = connection.cursor()

# Import data ----------------------------------------------------------------------------------------------------------
customers_df = pd.read_csv("./data/customers.csv")
locations_df = pd.read_csv("./data/locations.csv")
orders_df = pd.read_csv("./data/orders.csv")

# The assessment specification states that certain columns should be omitted; drop these columns:
vendor_cols_to_drop = ['sunday_from_time1', 'sunday_to_time1', 'sunday_from_time2', 'sunday_to_time2',
                       'monday_from_time1', 'monday_to_time1', 'monday_from_time2', 'monday_to_time2',
                       'tuesday_from_time1', 'tuesday_to_time1', 'tuesday_from_time2', 'tuesday_to_time2',
                       'wednesday_from_time1', 'wednesday_to_time1', 'wednesday_from_time2', 'wednesday_to_time2',
                       'thursday_from_time1', 'thursday_to_time1', 'thursday_from_time2', 'thursday_to_time2',
                       'friday_from_time1', 'friday_to_time1', 'friday_from_time2', 'friday_to_time2',
                       'saturday_from_time1', 'saturday_to_time1', 'saturday_from_time2', 'saturday_to_time2']
vendors_df = pd.read_csv("./data/vendors.csv").drop(vendor_cols_to_drop, axis=1)

# Rename columns for the sake of continuity ----------------------------------------------------------------------------
orders_colnames = {'deliverydistance': 'delivery_distance', 'preparationtime': 'preparation_time',
                   'LOCATION_NUMBER': 'location_number', 'LOCATION_TYPE': 'location_type',
                   'CID X LOC_NUM X VENDOR': 'cid_locnum_vendor'}
orders_df.rename(columns=orders_colnames, inplace=True)

vendors_colnames = {'id': 'vendor_id', 'OpeningTime': 'opening_time', 'OpeningTime2': 'opening_time_2',
                    'prepration_time': 'preparation_time'}
vendors_df.rename(columns=vendors_colnames, inplace=True)

# Create tables for each of the dataframes -----------------------------------------------------------------------------


def construct_create_statement(table_name, dataframe):
    """ Construct an SQL CREATE statement for a specified dataframe

    :param table_name: (string) The name of the table to create
    :param dataframe: (object) The dataframe to create a statement for
    :return: (string) The constructed SQL CREATE statement
    """
    # Define the create statement and add the primary key
    c_statement = "CREATE TABLE {} (\n\tid INTEGER PRIMARY KEY,\n".format(table_name)

    # Determine which dtype the column contains and add it to the CREATE statement
    column_dtype = None
    for column in dataframe:
        if dataframe[column].dtype == 'object':
            column_dtype = "VARCHAR(200)"
        elif dataframe[column].dtype == 'int64':
            column_dtype = "INT"
        elif dataframe[column].dtype == 'float64':
            column_dtype = "FLOAT"

        c_statement += "\t{} {},\n".format(column, column_dtype)

    # Close the CREATE statement
    c_statement = c_statement[:-2]  # Remove the trailing comma (also removes the newline character)
    c_statement += "\n);"

    return c_statement


cursor.execute(construct_create_statement('customers', customers_df))
cursor.execute(construct_create_statement('locations', locations_df))
cursor.execute(construct_create_statement('orders', orders_df))
cursor.execute(construct_create_statement('vendors', vendors_df))


# Populate the tables using the dataframes -----------------------------------------------------------------------------


def construct_insert_statement(table_name, dataframe):
    """ Construct an SQL INSERT statement for a specified dataframe

    :param table_name: (string) The name of the table to create a statement for
    :param dataframe: (object) The dataframe of data to insert
    :return: (string) The constructed SQL INSERT statement
    """
    # Define the insert statement and add the id column
    i_statement = "INSERT INTO {} (\n\tid,\n".format(table_name)

    # Add each column to the statement
    for column in dataframe:
        i_statement += "\t{},\n".format(column)

    # Close the main body of the INSERT statement
    i_statement = i_statement[:-2]  # Remove the trailing comma (also removes the newline character)
    i_statement += "\n)\nVALUES ("

    # Add value placeholders for each column (plus one for the id column)
    for x in range(0, dataframe.shape[1] + 1):
        i_statement += "?, "

    # Close the values section of the INSERT statement
    i_statement = i_statement[:-2]  # Remove the trailing comma (also removes the newline character)
    i_statement += ");"

    return i_statement


def populate_table(table_name, dataframe):
    """ Populate a table using data from a specified dataframe

    :param table_name: (string) The name of the table to populate
    :param dataframe: (object) The dataframe to pull data from
    """
    # Construct the INSERT statement
    i_statement = construct_insert_statement(table_name, dataframe)

    # Iterate over each row in the dataframe
    id_count = 0
    for index, row in dataframe.iterrows():
        values = [id_count]  # Add an id to the row (sequential, from zero)

        # Append each column value to the list of values
        for column in dataframe:
            values.append(row[column])

        cursor.execute(i_statement, tuple(values))  # Execute the INSERT statement

        id_count += 1  # Increment the iterator


populate_table('customers', customers_df)
populate_table('locations', locations_df)
populate_table('vendors', vendors_df)
populate_table('orders', orders_df)

# Close database connection --------------------------------------------------------------------------------------------
connection.commit()
connection.close()
