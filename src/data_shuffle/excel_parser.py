import pandas as ps
import os
from enum import Enum
import hashlib


class Paths(Enum):
    ALL_DATA_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '\\steam_store_games'
    STEAM = ALL_DATA_FOLDER + '\\steam.csv'
    STEAM_DESCRIPTION_DATA = ALL_DATA_FOLDER + '\\steam_description_data.csv'
    STEAM_MEDIA_DATA = ALL_DATA_FOLDER + '\\steam_media_data.csv'
    STEAM_REQUIREMENTS_DATA = ALL_DATA_FOLDER + '\\steam_requirements_data.csv'
    STEAM_SUPPORT_INFO = ALL_DATA_FOLDER + '\\steam_support_info.csv'
    STEAMSPY_TAG_DATA = ALL_DATA_FOLDER + '\\steamspy_tag_data.csv'


def read_csv(csv_path):
    return ps.read_csv(csv_path, header=0, dtype=str, low_memory=False)


def write_csv_to_file(csv_path, out_filename):
    out_filepath = '{dir}\\{file}'.format(dir=Paths.ALL_DATA_FOLDER.value, file=out_filename)
    with open(out_filepath, 'w', encoding='utf-8') as f:
        df = read_csv(csv_path)
        f.write(df.to_string())


def encode_dataset_values():
    game_dict = {}
    df = read_csv(Paths.STEAM.value)
    for label, content in df.items():
        for c in content:
            c_hash_hex = hashlib.md5(c.encode()).hexdigest()
            game_dict[c] = int(c_hash_hex, 16)

    print(game_dict['Team Fortress Classic'])
    print('size:' + str(len(game_dict.keys())))


def main():
    # write_csv_to_file(Paths.STEAM.value, 'parsed_steam.csv')
    encode_dataset_values()


if __name__ == '__main__':
    main()
