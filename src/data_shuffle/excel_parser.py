import pandas as pd
from src.data_shuffle.common_constants import Paths


def load_csv(csv_path):
    return pd.read_csv(csv_path, header=0)


def write_csv_to_file(csv_path, out_filename):
    out_filepath = '{dir}\\{file}'.format(dir=Paths.ALL_DATA_FOLDER.value, file=out_filename)
    with open(out_filepath, 'w', encoding='utf-8') as f:
        df = load_csv(csv_path)
        f.write(df.to_string())
