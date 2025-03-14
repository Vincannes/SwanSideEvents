import os
import configparser

MAIN_DIR = os.path.dirname(os.path.dirname(__file__))

config = configparser.ConfigParser()
config.read(os.path.join(MAIN_DIR, "config_discord_scipts.ini"))