import os
import matplotlib.pyplot as plt


plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

PROJECT_ROOT_DIR = '.'
CHAPTER_ID = 'preparing_dataset'
IMAGES_PATH = os.path.join(PROJECT_ROOT_DIR, 'pictures', CHAPTER_ID)


def save_fig(fig_id, tight_layout=True, fig_extension='png', resolution=300):
    path = os.path.join(IMAGES_PATH, fig_id + '.' + fig_extension)
    print('Saving image', fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)


def create_and_show_plot_from_dataframe_column(dataframe_column, fig_title):
    plt.figure(figsize=(12, 8))
    dataframe_column.hist(bins=15)
    save_fig(fig_title)
    plt.show()
