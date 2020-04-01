from enum import Enum
import os


class Paths(Enum):
    ALL_DATA_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '\\data'
    FIGURES_FOLDER = ALL_DATA_FOLDER + '\\figures'
    STEAM = ALL_DATA_FOLDER + '\\steam.csv'
    STEAM_DESCRIPTION_DATA = ALL_DATA_FOLDER + '\\steam_description_data.csv'
    STEAM_MEDIA_DATA = ALL_DATA_FOLDER + '\\steam_media_data.csv'
    STEAM_REQUIREMENTS_DATA = ALL_DATA_FOLDER + '\\steam_requirements_data.csv'
    STEAM_SUPPORT_INFO = ALL_DATA_FOLDER + '\\steam_support_info.csv'
    STEAMSPY_TAG_DATA = ALL_DATA_FOLDER + '\\steamspy_tag_data.csv'
