# import dependencies
import numpy as np
import pandas as pd

# import data
customers_df = pd.read_csv("../data/raw/customers.csv")
vendors_df = pd.read_csv("../data/raw/vendors.csv")
locations_df = pd.read_csv("../data/raw/locations.csv")
orders_df = pd.read_csv("../data/raw/orders.csv")


# data cleaning ###
# ------------- ###


# remove duplicate customer observations
customers_df = customers_df.drop_duplicates(subset=['akeed_customer_id'], keep='first')

# drop vendor columns specified in the assessment brief
vendors_df = vendors_df.drop([
    'sunday_from_time1', 'sunday_to_time1', 'sunday_from_time2', 'sunday_to_time2', 'monday_from_time1',
    'monday_to_time1', 'monday_from_time2', 'monday_to_time2', 'tuesday_from_time1', 'tuesday_to_time1',
    'tuesday_from_time2', 'tuesday_to_time2', 'wednesday_from_time1', 'wednesday_to_time1', 'wednesday_from_time2',
    'wednesday_to_time2', 'thursday_from_time1', 'thursday_to_time1', 'thursday_from_time2', 'thursday_to_time2',
    'friday_from_time1', 'friday_to_time1', 'friday_from_time2', 'friday_to_time2', 'saturday_from_time1',
    'saturday_to_time1', 'saturday_from_time2', 'saturday_to_time2'
], axis=1)

# drop orders with empty 'customer_id' fields
orders_df['customer_id'].replace('', np.nan, inplace=True)
orders_df = orders_df.dropna(subset=['customer_id'])

# drop orders with empty 'item_count' fields
orders_df['item_count'].replace('', np.nan, inplace=True)
orders_df = orders_df.dropna(subset=['item_count'])

# rename legacy ID columns
customers_df = customers_df.rename(columns={'akeed_customer_id': 'legacy_customer_id'})
vendors_df = vendors_df.rename(columns={'id': 'legacy_vendor_id'})
locations_df = locations_df.rename(columns={'customer_id': 'legacy_customer_id'})
orders_df = orders_df.rename(columns={
    'akeed_order_id': 'legacy_order_id',
    'customer_id': 'legacy_customer_id',
    'vendor_id': 'legacy_vendor_id'
})


# create a new 'customer_id' indexing system ###
# ------------------------------------------ ###


# use pandas index as the new 'customer_id'
customers_df['customer_id'] = customers_df.index

# create a dict of 'legacy_customer_id' and corresponding 'customer_id'
cids = customers_df.set_index('legacy_customer_id')['customer_id'].to_dict()

# copy new 'customer_id' values to 'locations_df' and 'orders_df'
locations_df['customer_id'] = locations_df['legacy_customer_id'].map(cids)
orders_df['customer_id'] = orders_df['legacy_customer_id'].map(cids)

# drop 'legacy_customer_id' from 'customers_df', 'locations_df', and 'orders_df'
customers_df = customers_df.drop(columns=['legacy_customer_id'], axis=1)
locations_df = locations_df.drop(columns=['legacy_customer_id'], axis=1)
orders_df = orders_df.drop(columns=['legacy_customer_id'], axis=1)

# drop locations and orders which don't correspond to a valid customer
locations_df = locations_df.dropna(subset=['customer_id'])
orders_df = orders_df.dropna(subset=['customer_id'])


# create a new 'vendor_id' indexing system ###
# ---------------------------------------- ###


# use pandas index as the new 'vendor_id'
vendors_df['vendor_id'] = vendors_df.index

# create a dict of 'legacy_vendor_id' and corresponding 'vendor_id'
vids = vendors_df.set_index('legacy_vendor_id')['vendor_id'].to_dict()

# copy new 'vendor_id' values to 'orders_df'
orders_df['vendor_id'] = orders_df['legacy_vendor_id'].map(vids)

# drop 'legacy_vendor_id' from 'vendors_df' and 'orders_df'
vendors_df = vendors_df.drop(columns=['legacy_vendor_id'], axis=1)
orders_df = orders_df.drop(columns=['legacy_vendor_id'], axis=1)


# create a new 'order_id' indexing system ###
# --------------------------------------- ###


# use pandas index as the new 'order_id'
orders_df['order_id'] = orders_df.index

# drop 'legacy_order_id' from 'orders_df'
orders_df = orders_df.drop(columns=['legacy_order_id'], axis=1)


# create a new 'location_id' indexing system ###
# ------------------------------------------ ###


# use pandas index as the new 'location_id'
locations_df['location_id'] = locations_df.index


# match the new 'location_id' in 'orders_df'
def update_location_id(cid, loc_num):
    return locations_df.loc[
        (locations_df['customer_id'] == cid) & (locations_df['location_number'] == loc_num)]['location_id'].values[0]


orders_df['location_id'] = [update_location_id(*a) for a in tuple(
    zip(orders_df['customer_id'], orders_df['LOCATION_NUMBER']))]  # this executes faster than .apply()


# drop 'location_number' from 'locations_df'
locations_df = locations_df.drop(columns=['location_number'])

# drop 'LOCATION_NUMBER' and 'LOCATION_TYPE' from 'orders_df'
orders_df = orders_df.drop(columns=['LOCATION_NUMBER', 'LOCATION_TYPE'])


# extract vendor category information ###
# ----------------------------------- ###


# extract 'vendor_id' and 'vendor_category_en' from 'vendors_df'
vendor_cats_df = vendors_df[['vendor_id', 'vendor_category_en']].copy().rename(
    columns={'vendor_category_en': 'category'}
)

# drop 'vendor_category_en' and 'vendor_category_id' from 'vendors_df'
vendors_df = vendors_df.drop(['vendor_category_en', 'vendor_category_id'], axis=1)


# extract vendor tags information ###
# ------------------------------- ###


# extract 'vendor_id' and 'vendor_tag_name' from 'vendors_df'
vendor_tags_df = vendors_df[['vendor_id', 'vendor_tag_name']].copy().rename(
    columns={'vendor_tag_name': 'tag'}
)

# split tags into a list and explode that list into a new row for each item
vendor_tags_df['tag'] = vendor_tags_df['tag'].str.split(',').tolist()
vendor_tags_df = vendor_tags_df.explode('tag').reset_index(drop=True)

# drop 'primary_tags', 'vendor_tag', and 'vendor_tag_name' from 'vendors_df'
vendors_df = vendors_df.drop(['primary_tags', 'vendor_tag', 'vendor_tag_name'], axis=1)


# extract customer favorite vendors information ###
# --------------------------------------------- ###


# extract 'customer_id' and 'vendor_id' from 'orders_df' where 'is_favorite' == 'Yes'
customer_fav_vendors_df = orders_df[orders_df['is_favorite'] == 'Yes'][
    ['customer_id', 'vendor_id']
].copy().reset_index(drop=True)

# drop 'is_favorite' from 'orders_df'
orders_df = orders_df.drop(['is_favorite'], axis=1)


# extract promo codes information ###
# ------------------------------- ###


# extract 'promo_code' and 'promo_code_discount_percentage' from 'orders_df'
promo_codes_df = orders_df[['promo_code', 'promo_code_discount_percentage']].copy().rename(
    columns={'promo_code': 'code', 'promo_code_discount_percentage': 'discount_percentage'}
)

# convert all codes to lowercase
promo_codes_df['codes'] = promo_codes_df['code'].str.lower()

# remove missing codes and those with missing 'discount_percentage'
promo_codes_df['code'].replace('', np.nan, inplace=True)
promo_codes_df['discount_percentage'].replace(0.0, np.nan, inplace=True)
promo_codes_df = promo_codes_df.dropna(subset=['code', 'discount_percentage'])

# remove duplicate codes
promo_codes_df = promo_codes_df.drop_duplicates(subset=['code'], keep='first')

# use the pandas index as 'code_id'
promo_codes_df['code_id'] = promo_codes_df.index

# create a dict of 'code' and corresponding 'code_id'
code_ids = promo_codes_df.set_index('code')['code_id'].to_dict()

# copy new 'code_id' into 'orders_df'
orders_df['promo_code'] = orders_df['promo_code'].str.lower()
orders_df['promo_code_id'] = orders_df['promo_code'].map(code_ids)

# drop 'promo_code' and 'promo_code_discount_percentage' from 'orders_df'
orders_df = orders_df.drop(['promo_code', 'promo_code_discount_percentage'], axis=1)


# extract vendor ratings information ###
# ---------------------------------- ###


# extract 'vendor_id', 'customer_id', and 'vendor_rating' from 'orders_df'
vendor_ratings_df = orders_df[['vendor_id', 'customer_id', 'vendor_rating']].copy().rename(
    columns={'vendor_rating': 'rating'}
)

# remove observations with missing 'rating' fields or those where 'rating' == 0
vendor_ratings_df['rating'].replace(0.0, np.nan, inplace=True)
vendor_ratings_df = vendor_ratings_df.dropna(subset=['rating']).reset_index(drop=True)

# drop 'vendor_rating' from 'orders_df'
orders_df = orders_df.drop(['vendor_rating'], axis=1)


# export data
customers_df.to_csv("../data/customers.csv")
vendors_df.to_csv("../data/vendors.csv")
locations_df.to_csv("../data/locations.csv")
orders_df.to_csv("../data/orders.csv")

vendor_cats_df.to_csv("../data/vendor-categories.csv")
vendor_tags_df.to_csv("../data/vendor-tags.csv")
customer_fav_vendors_df.to_csv("../data/customer-fav-vendors.csv")
promo_codes_df.to_csv("../data/promo-codes.csv")
vendor_ratings_df.to_csv("../data/vendor-ratings.csv")
