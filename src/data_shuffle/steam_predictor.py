from __future__ import division, print_function, unicode_literals
import numpy as np
import pandas as pd
from src.data_shuffle.plotting_utilities import *
import src.data_shuffle.excel_parser as ep


def load_data(steam_path, file):
    csv_path = os.path.join(steam_path, file)
    return pd.read_csv(csv_path, error_bad_lines=False)


def encode_attribute_from_column(dataframe_column):
    col = pd.Series(dataframe_column)
    dictionary = {}
    enc_series = []
    i = 0
    for c in col:
        if c not in dictionary.keys():
            dictionary[c] = (i, c)
            i = i + 1
        x = dictionary[c][0]
        enc_series.append(x)
    return enc_series, dictionary


# ## TODO
# funckcja zapisująca słownik do pliku wraz z jej opisem
def extract_values_from_columns(dataframe_column):
    unique_attribute_values = set()

    for attribute in dataframe_column:
        for value in attribute.split(';'):
            unique_attribute_values.add(value)
    return unique_attribute_values


def produce_encoded_dataframe(relevant_attributes, raw_data):
    enc_data = pd.DataFrame()
    enc_data = pd.concat([enc_data, raw_data['platforms'].str.get_dummies(sep=';')], axis=1)
    enc_data = pd.concat([enc_data, raw_data['categories'].str.get_dummies(sep=';')], axis=1)
    enc_data = pd.concat([enc_data, raw_data['genres'].str.get_dummies(sep=';')], axis=1)
    for attr in relevant_attributes.keys():
        enc_data[attr] = relevant_attributes[attr]
    return enc_data


def process_ratings_attribute(steam_cp):
    pos = pd.Series(steam_cp['positive_ratings'])
    neg = pd.Series(steam_cp['negative_ratings'])
    ratings = []
    for p, n in zip(pos, neg):
        total = p + n
        i = np.round((p / total) * 100)
        ratings.append(i)
    steam_cp['Rating'] = ratings
    return ratings


def main():
    steam = ep.load_csv(ep.Paths.STEAM.value)
    steam.head()
    steam.info()

    steam_cp = steam.copy()
    steam_cp = steam_cp.drop(columns=['appid', 'name', 'steamspy_tags', 'price'])
    create_and_show_plot_from_dataframe_column(steam_cp['owners'], 'steam_cp_owners')

    enc_dev, dev_dict = encode_attribute_from_column('developer')
    enc_publ, publ_dict = encode_attribute_from_column('publisher')
    enc_own, own_dict = encode_attribute_from_column('owners')

    genres_set = extract_values_from_columns(steam_cp['genres'])
    cats_set = extract_values_from_columns(steam_cp['categories'])

    ratings = process_ratings_attribute(steam_cp)
    months, years = process_release_date_attribute(steam_cp)

    relevant_attributes = {'Month': months, 'Year': years,
                           'English': steam_cp['english'], 'Developer': enc_dev,
                           'Publisher': enc_publ, 'Required_Age': steam_cp['required_age'],
                           'Achievements': steam_cp['achievements'], 'Average_Playtime': steam_cp['average_playtime'],
                           'Median_Playtime': steam_cp['median_playtime'], 'Rating': ratings, 'Owners': enc_own}
    produce_encoded_dataframe(relevant_attributes, steam_cp)


def process_release_date_attribute(steam_cp):
    dates = pd.Series(steam_cp['release_date'])
    dates = pd.to_datetime(dates, format='%Y-%m-%d')
    months = []
    years = []
    for i in dates:
        d = i.month
        months.append(d)
        y = i.year
        years.append(y)
    steam_cp['Month'] = months
    steam_cp['Year'] = years
    steam_cp.head(20)
    return months, years


if __name__ == '__main__':
    steam = ep.load_csv(ep.Paths.STEAM.value)
    steam = steam.drop(columns=['appid', 'name', 'steamspy_tags', 'price'])
    enc_dev, dev_dict = encode_attribute_from_column('developer')
    enc_publ, publ_dict = encode_attribute_from_column('publisher')
    enc_own, own_dict = encode_attribute_from_column('owners')

    genres_set = extract_values_from_columns(steam['genres'])
    genres_set_new = extract_values_from_columns_new(steam['genres'])

