# import dependencies
import pandas as pd
import sqlite3


# import data
customers_df = pd.read_csv("../data/customers.csv")
vendors_df = pd.read_csv("../data/vendors.csv")
locations_df = pd.read_csv("../data/locations.csv")
promo_codes_df = pd.read_csv("../data/promo-codes.csv")
orders_df = pd.read_csv("../data/orders.csv")
vendor_cats_df = pd.read_csv("../data/vendor-categories.csv")
vendor_tags_df = pd.read_csv("../data/vendor-tags.csv")
vendor_ratings_df = pd.read_csv("../data/vendor-ratings.csv")
customer_fav_vendors_df = pd.read_csv("../data/customer-fav-vendors.csv")



# establish database connection
connection = sqlite3.connect("../delivery-database.db")
cursor = connection.cursor()


# create and populate customers table  ###
# ------------------------------------ ###
cursor.execute(
    """
    CREATE TABLE customers (
        id integer PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        gender VARCHAR(200),
        birth_year VARCHAR(200),
        status VARCHAR(200),
        verified VARCHAR(200),
        language VARCHAR(200),
        created_at VARCHAR(200),
        updated_at VARCHAR(200)
    );
    """
)

for index, row in customers_df.iterrows():
    sql_command = """
        INSERT INTO customers (
            id, gender, birth_year, status, verified, language, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """
    data = (row['customer_id'], row['gender'], row['birth_year'], row['status'], row['verified'], row['language'],
                  row['created_at'], row['updated_at'])

    cursor.execute(sql_command, data)


# create and populate vendors table ###
# --------------------------------- ###
cursor.execute(
    """
    CREATE TABLE vendors (
        id integer PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        auth_id INT,
        latitude FLOAT,
        longitude FLOAT,
        delivery_fee FLOAT,
        max_serving_dist FLOAT,
        opening_time VARCHAR(200),
        opening_time_2 VARCHAR(200),
        preparation_time INT,
        commission FLOAT,
        is_akeed_delivering VARCHAR(200),
        discount_percentage FLOAT,
        status FLOAT,
        verified INT,
        rank INT,
        language VARCHAR(200),
        avg_rating FLOAT,
        one_click_vendor VARCHAR(200),
        created_at VARCHAR(200),
        updated_at VARCHAR(200),
        device_type INT
    );
    """
)

for index, row in vendors_df.iterrows():
    sql_command = """
        INSERT INTO vendors (
            id, auth_id, latitude, longitude, delivery_fee, max_serving_dist, opening_time, opening_time_2,
            preparation_time, commission, is_akeed_delivering, discount_percentage, status, verified, rank, language,
            avg_rating, one_click_vendor, created_at, updated_at, device_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    data = (row['vendor_id'], row['auth_id'], row['latitude'], row['longitude'], row['delivery_fee'],
            row['max_serving_dist'], row['opening_time'], row['opening_time_2'], row['preparation_time'],
            row['commission'], row['is_akeed_delivering'], row['discount_percentage'], row['status'], row['verified'],
            row['rank'], row['language'], row['avg_rating'], row['one_click_vendor'], row['created_at'],
            row['updated_at'], row['device_type'])

    cursor.execute(sql_command, data)


# create and populate locations table ###
# ----------------------------------- ###
cursor.execute(
    """
    CREATE TABLE locations (
        id integer PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        location_type VARCHAR(200),
        latitude FLOAT,
        longitude FLOAT,
        customer_id INT NOT NULL,
        FOREIGN KEY (customer_id)
            REFERENCES customers (id)
    );
    """
)
for index, row in locations_df.iterrows():
    sql_command = """
        INSERT INTO locations (
            id, location_type, latitude, longitude, customer_id
        ) VALUES (?, ?, ?, ?, ?);
    """
    data = (row['location_id'], row['location_type'], row['latitude'], row['longitude'], row['customer_id'])

    cursor.execute(sql_command, data)


# create and populate promo_codes table ###
# ------------------------------------- ###
cursor.execute(
    """
    CREATE TABLE promo_codes (
        id integer PRIMARY KEY NOT NULL UNIQUE,
        code VARCHAR(200),
        discount_percentage FLOAT
    );
    """
)
for index, row in promo_codes_df.iterrows():
    sql_command = """
        INSERT INTO promo_codes (
            id, code, discount_percentage
        ) VALUES (?, ?, ?);
    """
    data = (row['code_id'], row['code'], row['discount_percentage'])

    cursor.execute(sql_command, data)


# create and populate orders table ###
# -------------------------------- ###
cursor.execute(
    """
    CREATE TABLE orders (
        id integer PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        customer_id INT,
        vendor_id INT,
        location_id INT,
        promo_code_id INT,
        n_items INT,
        price_due FLOAT,
        payment_method INT,
        is_rated VARCHAR(200),
        delivery_distance FLOAT,
        preparation_time VARCHAR(200),
        delivery_time VARCHAR(200),
        order_accepted_time VARCHAR(200),
        driver_accepted_time VARCHAR(200),
        ready_for_pickup_time VARCHAR(200),
        picked_up_time VARCHAR(200),
        delivered_time VARCHAR(200),
        delivery_date VARCHAR(200),
        created_at VARCHAR(200),
        FOREIGN KEY (customer_id) REFERENCES customers (id),
        FOREIGN KEY (vendor_id) REFERENCES vendors (id),
        FOREIGN KEY (location_id) REFERENCES locations (id),
        FOREIGN KEY (promo_code_id) REFERENCES promo_codes (id)
    );
    """
)
for index, row in orders_df.iterrows():
    sql_command = """
        INSERT INTO orders (
            id, customer_id, vendor_id, location_id, promo_code_id, n_items, price_due, payment_method, is_rated,
            delivery_distance, preparation_time, delivery_time, order_accepted_time, driver_accepted_time,
            ready_for_pickup_time, picked_up_time, delivered_time, delivery_date, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    data = (row['order_id'], row['customer_id'], row['vendor_id'], row['location_id'], row['promo_code_id'],
            row['n_items'], row['price_due'], row['payment_method'], row['is_rated'], row['delivery_distance'],
            row['preparation_time'], row['delivery_time'], row['order_accepted_time'], row['driver_accepted_time'],
            row['ready_for_pickup_time'], row['picked_up_time'], row['delivered_time'], row['delivery_date'],
            row['created_at'])

    cursor.execute(sql_command, data)


# create and populate vendor_categories table ###
# ------------------------------------------- ###
cursor.execute(
    """
    CREATE TABLE vendor_categories (
        id integer PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        vendor_id INT,
        category VARCHAR(200),
        FOREIGN KEY (vendor_id) REFERENCES vendors (id)
    );
    """
)
i = 0
for index, row in vendor_cats_df.iterrows():
    sql_command = """
        INSERT INTO vendor_categories (
            id, vendor_id, category
        ) VALUES (?, ?, ?);
    """
    data = (i, row['vendor_id'], row['category'])

    cursor.execute(sql_command, data)
    i += 1


# create and populate vendor_tags table ###
# ------------------------------------- ###
cursor.execute(
    """
    CREATE TABLE vendor_tags (
        id integer PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        vendor_id INT,
        tag VARCHAR(200),
        FOREIGN KEY (vendor_id) REFERENCES vendors (id)
    );
    """
)
i = 0
for index, row in vendor_tags_df.iterrows():
    sql_command = """
        INSERT INTO vendor_tags (
            id, vendor_id, tag
        ) VALUES (?, ?, ?);
    """
    data = (i, row['vendor_id'], row['tag'])

    cursor.execute(sql_command, data)
    i += 1


# create and populate vendor_ratings table ###
# ---------------------------------------- ###
cursor.execute(
    """
    CREATE TABLE vendor_ratings (
        id integer PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        vendor_id INT,
        customer_id INT,
        rating FLOAT,
        FOREIGN KEY (vendor_id) REFERENCES vendors (id),
        FOREIGN KEY (customer_id) REFERENCES customers (id)
    );
    """
)
for index, row in vendor_ratings_df.iterrows():
    sql_command = """
        INSERT INTO vendor_ratings (
            id, vendor_id, customer_id, rating
        ) VALUES (?, ?, ?, ?);
    """
    data = (i, row['vendor_id'], row['customer_id'], row['rating'])

    cursor.execute(sql_command, data)
    i += 1


# create and populate customer_fav_vendors table ###
# ---------------------------------------------- ###
cursor.execute(
    """
    CREATE TABLE customer_fav_vendors (
        id integer PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        customer_id INT,
        vendor_id INT,
        FOREIGN KEY (customer_id) REFERENCES customers (id),
        FOREIGN KEY (vendor_id) REFERENCES vendors (id)
    );
    """
)
for index, row in customer_fav_vendors_df.iterrows():
    sql_command = """
        INSERT INTO vendor_ratings (
            id, customer_id, vendor_id
        ) VALUES (?, ?, ?);
    """
    data = (i, row['customer_id'], row['vendor_id'])

    cursor.execute(sql_command, data)
    i += 1


# close database connection
connection.commit()
connection.close()