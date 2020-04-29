from __future__ import division, print_function, unicode_literals
import numpy as np
import pandas as pd
from src.data_shuffle.plotting_utilities import *
from src.data_shuffle.bi_dict import BiDict
from src.data_shuffle.excel_parser import load_csv
from src.data_shuffle.common_constants import Paths
import pprint as pp
import json


def encode_attribute_from_column(dataframe_column):
    id_attribute_bi_dict = BiDict()
    encoded_column = []
    for idx, attr in enumerate(dataframe_column):
        if attr not in id_attribute_bi_dict.keys():
            id_attribute_bi_dict[attr] = idx
        encoded_column.append(id_attribute_bi_dict[attr])
    return encoded_column, id_attribute_bi_dict


def save_encoded_dict_to_file(dest_filepath, data_to_write):
    with open(dest_filepath, 'w') as f:
        out = json.dumps(data_to_write)
        f.write(pp.pformat(out))


def extract_values_from_columns(dataframe_column, value_sep=';'):
    unique_attribute_values = set()
    for attribute in dataframe_column:
        for value in attribute.split(value_sep):
            unique_attribute_values.add(value)
    return unique_attribute_values


def process_ratings_attribute(pos, neg):
    ratings = []
    for p, n in zip(pos, neg):
        total_reviews = int(p) + int(n)
        rating = np.round((int(p) / total_reviews) * 100)
        ratings.append(rating)
    return ratings


def process_release_date_attribute(release_date_column):
    dates = pd.to_datetime(release_date_column, format='%Y-%m-%d')
    months, years = [], []
    for date in dates:
        months.append(date.month)
        years.append(date.year)
    return months, years


def produce_encoded_dataframe(relevant_attributes, attributes_to_concat, raw_data, value_sep=';'):
    encoded_data = pd.DataFrame()
    for attr in attributes_to_concat:
        encoded_data = pd.concat([encoded_data, raw_data[attr].str.get_dummies(sep=value_sep)], axis=1)

    for attr in relevant_attributes.keys():
        encoded_data[attr] = relevant_attributes[attr]
    return encoded_data


def main():
    steam = load_csv(Paths.STEAM.value)
    steam_cp = steam.copy()
    create_and_show_hist_from_dataframe_column(steam_cp['platforms'])

    encoded_devs, _ = encode_attribute_from_column(steam_cp['developer'])
    encoded_publishers, _ = encode_attribute_from_column(steam_cp['publisher'])
    encoded_owners, _ = encode_attribute_from_column(steam_cp['owners'])
    ratings = process_ratings_attribute(steam_cp['positive_ratings'], steam_cp['negative_ratings'])
    months, years = process_release_date_attribute(steam_cp['release_date'])
    steam_cp = steam_cp.drop(columns=['appid', 'name', 'steamspy_tags', 'price', 'release_date'])

    relevant_attributes = {'Month': months, 'Year': years,
                           'English': steam_cp['english'], 'Developer': encoded_devs,
                           'Publisher': encoded_publishers, 'Required_Age': steam_cp['required_age'],
                           'Achievements': steam_cp['achievements'], 'Average_Playtime': steam_cp['average_playtime'],
                           'Median_Playtime': steam_cp['median_playtime'], 'Rating': ratings, 'Owners': encoded_owners}
    attributes_to_concat = ['genres', 'categories', 'platforms']
    final_encoded_df = produce_encoded_dataframe(relevant_attributes, attributes_to_concat, steam_cp)
    final_encoded_df.to_csv(Paths.ALL_DATA_FOLDER.value + '\\enc_steam.csv', index=False)


if __name__ == '__main__':
    main()
