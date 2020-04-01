import pandas as pd
import hashlib
from src.data_shuffle.common_constants import Paths


def load_csv(csv_path):
    return pd.read_csv(csv_path, header=0, dtype=str, low_memory=False)


def write_csv_to_file(csv_path, out_filename):
    out_filepath = '{dir}\\{file}'.format(dir=Paths.ALL_DATA_FOLDER.value, file=out_filename)
    with open(out_filepath, 'w', encoding='utf-8') as f:
        df = load_csv(csv_path)
        f.write(df.to_string())


def encode_dataset_values():
    game_dict = {}
    df = load_csv(Paths.STEAM.value)
    for label, content in df.items():
        for c in content:
            c_hash_hex = hashlib.md5(c.encode()).hexdigest()
            game_dict[c] = int(c_hash_hex, 16)
