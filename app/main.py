import os
import gazu
import logging

from config import config
from send_discord import on_task_status_change

MAIN_DIR = os.path.dirname(os.path.dirname(__file__))
EVENT_LOG = os.path.join(MAIN_DIR, "discord_bot.log")

# VARIABLES
KITSU_URL = config.get('Kitsu', 'URL')
KITSU_EMAIL = config.get('Kitsu', 'EMAIL')
KITSU_PASSWORD = config.get('Kitsu', 'PASSWORD')

# Setup du LOGGER
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(EVENT_LOG),
        logging.StreamHandler()
    ]
)

# KITSU
gazu.set_host(KITSU_URL + "/api")
gazu.set_event_host(KITSU_URL)
gazu.log_in(KITSU_EMAIL, KITSU_PASSWORD)

try:
    event_client = gazu.events.init()
    gazu.events.add_listener(event_client, "task:status-changed", on_task_status_change)
    gazu.events.run_client(event_client)
    print("Kitsu event listener actif...")
except KeyboardInterrupt:
    print("Stop listening")
except TypeError:
    print("Authentification failed, please verify credential")
