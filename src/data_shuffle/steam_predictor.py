from __future__ import division, print_function, unicode_literals
import numpy as np
import pandas as pd
from src.data_shuffle.plotting_utilities import *
import src.data_shuffle.excel_parser as ep
from src.data_shuffle.bi_dict import BiDict


def load_data(steam_path, file):
    csv_path = os.path.join(steam_path, file)
    return pd.read_csv(csv_path, error_bad_lines=False)


def encode_attribute_from_column(dataframe_column):
    id_attribute_bi_dict = BiDict()
    encoded_column = []
    for idx, attribute in enumerate(dataframe_column):
        if attribute not in id_attribute_bi_dict.keys():
            id_attribute_bi_dict[attribute] = idx
            encoded_column.append(idx)
    return encoded_column, id_attribute_bi_dict


# ## TODO
# funckcja zapisująca słownik do pliku wraz z jej opisem
def extract_values_from_columns(dataframe_column):
    unique_attribute_values = set()
    for attribute in dataframe_column:
        for value in attribute.split(';'):
            unique_attribute_values.add(value)
    return unique_attribute_values


def process_ratings_attribute(pos, neg):
    ratings = []
    for p, n in zip(pos, neg):
        total_reviews = p + n
        rating = np.round((p / total_reviews) * 100)
        ratings.append(rating)
    return ratings


def process_release_date_attribute(release_date_column):
    dates = pd.to_datetime(release_date_column, format='%Y-%m-%d')
    months, years = [], []
    for date in dates:
        months.append(date.month)
        years.append(date.year)
    return months, years


def produce_encoded_dataframe(relevant_attributes, raw_data):
    encoded_data = pd.DataFrame()
    encoded_data = pd.concat([encoded_data, raw_data['platforms'].str.get_dummies(sep=';')], axis=1)
    encoded_data = pd.concat([encoded_data, raw_data['categories'].str.get_dummies(sep=';')], axis=1)
    encoded_data = pd.concat([encoded_data, raw_data['genres'].str.get_dummies(sep=';')], axis=1)
    for attr in relevant_attributes.keys():
        encoded_data[attr] = relevant_attributes[attr]
    return encoded_data


def main():
    steam = ep.load_csv(ep.Paths.STEAM.value)

    steam_cp = steam.copy()
    create_and_show_plot_from_dataframe_column(steam_cp['owners'], 'steam_cp_owners')

    encoded_devs, _ = encode_attribute_from_column('developer')
    encoded_publishers, _ = encode_attribute_from_column('publisher')
    encoded_owners, _ = encode_attribute_from_column('owners')
    ratings = process_ratings_attribute(steam_cp['positive_ratings'], steam_cp['negative_ratings'])
    months, years = process_release_date_attribute(steam_cp['release_date'])

    steam_cp = steam_cp.drop(columns=['appid', 'name', 'steamspy_tags', 'price', 'release_date'])
    relevant_attributes = {'Month': months, 'Year': years,
                           'English': steam_cp['english'], 'Developer': encoded_devs,
                           'Genres'
                           'Publisher': encoded_publishers, 'Required_Age': steam_cp['required_age'],
                           'Achievements': steam_cp['achievements'], 'Average_Playtime': steam_cp['average_playtime'],
                           'Median_Playtime': steam_cp['median_playtime'], 'Rating': ratings, 'Owners': encoded_owners}
    produce_encoded_dataframe(relevant_attributes, steam_cp)


if __name__ == '__main__':
    main()


