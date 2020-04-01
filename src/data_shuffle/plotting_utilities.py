import os
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def save_fig(fig, dest_folder, fig_id, tight_layout=True, fig_extension='png', resolution=300):
    print('Saving image...')
    if tight_layout:
        fig.tight_layout()
    fig.savefig(os.path.join(dest_folder, fig_id) + '.' + fig_extension, format=fig_extension, dpi=resolution)


def create_and_show_hist_from_dataframe_column(dataframe_column):
    fig = plt.figure(figsize=(12, 8))
    dataframe_column.value_counts().plot(kind='bar')
    plt.rcParams['axes.labelsize'] = 14
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12
    plt.xticks(rotation='horizontal')
    plt.grid(True)
    plt.show()
    return fig
