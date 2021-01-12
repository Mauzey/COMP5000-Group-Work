


# import dependencies
import numpy as np
import os
import pandas as pd
import sqlite3

# establish database connection
connection = sqlite3.connect("../data/delivery-database.db")
cursor = connection.cursor()


# CUSTOMER DATA #
# import customer data and drop duplicate observations based on 'akeed_customer_id'
# customers_df = pd.read_csv("../data/customers.csv").drop_duplicates(subset=['akeed_customer_id'], keep='first')

# customers_df['customer_id'] = customers_df.index  # use the pandas index as the new 'customer_id'
customers_df = customers_df.rename(columns={'dob': 'birth_year'})  # rename 'dob' column


# VENDOR DATA #
# import vendor data and drop columns specified in the assessment brief
# vendors_df = pd.read_csv("../data/vendors.csv").drop([
#     'sunday_from_time1', 'sunday_to_time1', 'sunday_from_time2', 'sunday_to_time2', 'monday_from_time1',
#     'monday_to_time1', 'monday_from_time2', 'monday_to_time2', 'tuesday_from_time1', 'tuesday_to_time1',
#     'tuesday_from_time2', 'tuesday_to_time2', 'wednesday_from_time1', 'wednesday_to_time1', 'wednesday_from_time2',
#     'wednesday_to_time2', 'thursday_from_time1', 'thursday_to_time1', 'thursday_from_time2', 'thursday_to_time2',
#     'friday_from_time1', 'friday_to_time1', 'friday_from_time2', 'friday_to_time2', 'saturday_from_time1',
#     'saturday_to_time1', 'saturday_from_time2', 'saturday_to_time2'
# ], axis=1)

# vendors_df = vendors_df.rename(columns={'id': 'akeed_vendor_id'})  # rename the legacy 'id'
# vendors_df['vendor_id'] = vendors_df.index  # use the pandas index as the new 'vendor_id'

# rename columns
vendors_df = vendors_df.rename(columns={
    'delivery_charge': 'delivery_fee', 'serving_distance': 'max_serving_distance', 'OpeningTime': 'opening_time',
    'OpeningTime2': 'opening_time_2', 'prepration_time': 'avg_preparation_time', 'verified': 'is_verified',
    'vendor_rating': 'avg_rating', 'one_click_vendor': 'is_one_click', 'device_type': 'akeed_device_type'
})


# LOCATION DATA #
# locations_df = pd.read_csv("../data/locations.csv").rename(columns={'customer_id': 'akeed_customer_id'})  # import

locations_df['location_id'] = locations_df.index  # use the pandas index as the new 'location_id'

# get new 'customer_id' values
ids = customers_df.set_index('akeed_customer_id')['customer_id'].to_dict()
locations_df['customer_id'] = locations_df['akeed_customer_id'].map(ids)

# drop locations with no corresponding customer data
locations_df = locations_df.dropna(subset=['customer_id'])


# ORDERS DATA #
# import orders data and rename existing customer id column
# orders_df = pd.read_csv("../data/orders.csv").rename(columns={'customer_id': 'akeed_customer_id'})

# drop orders with no 'akeed_customer_id'
# orders_df['akeed_customer_id'].replace('', np.nan, inplace=True)
# orders_df = orders_df.dropna(subset=['akeed_customer_id'])
# # drop orders with no 'item_count'
# orders_df['item_count'].replace('', np.nan, inplace=True)
# orders_df = orders_df.dropna(subset=['item_count'])

# orders_df['order_id'] = orders_df.index  # use the pandas index as the new 'order_id'

# get new 'customer_id' values
# ids = customers_df.set_index('akeed_customer_id')['customer_id'].to_dict()
# orders_df['customer_id'] = orders_df['akeed_customer_id'].map(ids)
# drop the old 'akeed_customer_id' and 'akeed_order_id' columns
# orders_df = orders_df.drop(['akeed_customer_id', 'akeed_order_id'], axis=1)

# drop 'promo_code', 'promo_code_discount_percentage', 'driver_rating', 'CID X LOC_NUM X VENDOR' and 'is_rated' columns
orders_df = orders_df.drop(['promo_code', 'promo_code_discount_percentage', 'is_rated', 'driver_rating',
                            'CID X LOC_NUM X VENDOR'], axis=1)

# get new 'vendor_id' values
# ids = vendors_df.set_index('akeed_vendor_id')['vendor_id'].to_dict()
# orders_df['vendor_id'] = orders_df['vendor_id'].map(ids)

#
#
# GET NEW 'location_id' VALUES
#
#


# rename columns
orders_df = orders_df.rename(columns={
    'item_count': 'n_items', 'grand_total': 'total_price', 'payment_mode': 'payment_method',
    'deliverydistance': 'distance', 'preparationtime': 'preparation_time', 'delivery_time': 'delivery_at',
    'order_accepted_time': 'order_accepted_at', 'driver_accepted_time': 'driver_accepted_at',
    'ready_for_pickup_time': 'ready_for_pickup_at', 'picked_up_time': 'pickup_at', 'delivered_time': 'delivered_at',
    'delivery_date': 'date'
})


# VENDOR CATEGORY DATA #
# extract vendor categories from 'vendors_df'
vendor_cat_df = vendors_df[['vendor_id', 'vendor_category_en']].copy().rename(
    columns={'vendor_category_en': 'category'}
)
vendors_df = vendors_df.drop(['vendor_category_en', 'vendor_category_id'], axis=1)  # drop 'vendors_df' columns

# VENDOR TAGS DATA #
# extract vendor tags from 'vendors_df'
vendor_tags_df = vendors_df[['vendor_id', 'vendor_tag_name']].copy().rename(
    columns={'vendor_tag_name': 'tag'}
)
vendor_tags_df['tag'] = vendor_tags_df['tag'].str.split(',').tolist()
vendor_tags_df = vendor_tags_df.explode('tag').reset_index(drop=True)

vendors_df = vendors_df.drop(['primary_tags', 'vendor_tag', 'vendor_tag_name'], axis=1)  # drop 'vendors_df' columns

# CUSTOMER FAVORITE VENDORS DATA #
# extract 'customer_id' and 'vendor_id' from 'orders_df' where 'is_favorite' is true
customer_fav_vendors_df = orders_df[orders_df['is_favorite'] == 'Yes'][['customer_id', 'vendor_id']].copy()
customer_fav_vendors_df = customer_fav_vendors_df.reset_index(drop=True)  # reset index

orders_df = orders_df.drop(['is_favorite'], axis=1)  # drop 'is_favorite' from 'orders_df'








# # import data
# locations_df = pd.read_csv("../data/locations.csv")
#
# # the assessment specification states that certain columns should be omitted; drop these columns
# vendors_df = pd.read_csv("../data/vendors.csv").drop([
#     'sunday_from_time1', 'sunday_to_time1', 'sunday_from_time2', 'sunday_to_time2', 'monday_from_time1',
#     'monday_to_time1', 'monday_from_time2', 'monday_to_time2', 'tuesday_from_time1', 'tuesday_to_time1',
#     'tuesday_from_time2', 'tuesday_to_time2', 'wednesday_from_time1', 'wednesday_to_time1', 'wednesday_from_time2',
#     'wednesday_to_time2', 'thursday_from_time1', 'thursday_to_time1', 'thursday_from_time2', 'thursday_to_time2',
#     'friday_from_time1', 'friday_to_time1', 'friday_from_time2', 'friday_to_time2', 'saturday_from_time1',
#     'saturday_to_time1', 'saturday_from_time2', 'saturday_to_time2'
# ], axis=1)
#
# # rename columns for readability
# # orders_df.rename(columns={
# #     'deliverydistance': 'delivery_distance', 'preparationtime': 'preparation_time',
# #     'LOCATION_NUMBER': 'location_number', 'LOCATION_TYPE': 'location_type',
# #     'CID X LOC_NUM X VENDOR': 'cid_locnum_vendor'
# # }, inplace=True)
#
# vendors_df.rename(columns={
#     'id': 'vendor_id', 'OpeningTime': 'opening_time', 'OpeningTime2': 'opening_time_2',
#     'prepration_time': 'preparation_time'
# }, inplace=True)
#
#
# print(customers_df.dtypes)
# print(customers_df.head())
#


#
# # Create tables for each of the dataframes -----------------------------------------------------------------------------
#
#
# def construct_create_statement(table_name, dataframe):
#     """ Construct an SQL CREATE statement for a specified dataframe
#
#     :param table_name: (string) The name of the table to create
#     :param dataframe: (object) The dataframe to create a statement for
#     :return: (string) The constructed SQL CREATE statement
#     """
#     # Define the create statement and add the primary key
#     c_statement = "CREATE TABLE {} (\n\tid INTEGER PRIMARY KEY,\n".format(table_name)
#
#     # Determine which dtype the column contains and add it to the CREATE statement
#     column_dtype = None
#     for column in dataframe:
#         if dataframe[column].dtype == 'object':
#             column_dtype = "VARCHAR(200)"
#         elif dataframe[column].dtype == 'int64':
#             column_dtype = "INT"
#         elif dataframe[column].dtype == 'float64':
#             column_dtype = "FLOAT"
#
#         c_statement += "\t{} {},\n".format(column, column_dtype)
#
#     # Close the CREATE statement
#     c_statement = c_statement[:-2]  # Remove the trailing comma (also removes the newline character)
#     c_statement += "\n);"
#
#     return c_statement
#
#
# cursor.execute(construct_create_statement('customers', customers_df))
# cursor.execute(construct_create_statement('locations', locations_df))
# cursor.execute(construct_create_statement('orders', orders_df))
# cursor.execute(construct_create_statement('vendors', vendors_df))
#
#
# # Populate the tables using the dataframes -----------------------------------------------------------------------------
#
#
# def construct_insert_statement(table_name, dataframe):
#     """ Construct an SQL INSERT statement for a specified dataframe
#
#     :param table_name: (string) The name of the table to create a statement for
#     :param dataframe: (object) The dataframe of data to insert
#     :return: (string) The constructed SQL INSERT statement
#     """
#     # Define the insert statement and add the id column
#     i_statement = "INSERT INTO {} (\n\tid,\n".format(table_name)
#
#     # Add each column to the statement
#     for column in dataframe:
#         i_statement += "\t{},\n".format(column)
#
#     # Close the main body of the INSERT statement
#     i_statement = i_statement[:-2]  # Remove the trailing comma (also removes the newline character)
#     i_statement += "\n)\nVALUES ("
#
#     # Add value placeholders for each column (plus one for the id column)
#     for x in range(0, dataframe.shape[1] + 1):
#         i_statement += "?, "
#
#     # Close the values section of the INSERT statement
#     i_statement = i_statement[:-2]  # Remove the trailing comma (also removes the newline character)
#     i_statement += ");"
#
#     return i_statement
#
#
# def populate_table(table_name, dataframe):
#     """ Populate a table using data from a specified dataframe
#
#     :param table_name: (string) The name of the table to populate
#     :param dataframe: (object) The dataframe to pull data from
#     """
#     # Construct the INSERT statement
#     i_statement = construct_insert_statement(table_name, dataframe)
#
#     # Iterate over each row in the dataframe
#     id_count = 0
#     for index, row in dataframe.iterrows():
#         values = [id_count]  # Add an id to the row (sequential, from zero)
#
#         # Append each column value to the list of values
#         for column in dataframe:
#             values.append(row[column])
#
#         cursor.execute(i_statement, tuple(values))  # Execute the INSERT statement
#
#         id_count += 1  # Increment the iterator
#
#
# populate_table('customers', customers_df)
# populate_table('locations', locations_df)
# populate_table('vendors', vendors_df)
# populate_table('orders', orders_df)
#
# # Close database connection --------------------------------------------------------------------------------------------
# connection.commit()
# connection.close()

