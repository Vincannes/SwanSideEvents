import gazu

from adapters.config_file import get_config_file
from send_discord import on_task_status_change


def run():
    config = get_config_file()

    # VARIABLES
    KITSU_URL = config.get('Kitsu', 'URL')
    KITSU_EMAIL = config.get('Kitsu', 'EMAIL')
    KITSU_PASSWORD = config.get('Kitsu', 'PASSWORD')

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


if __name__ == "__main__":
    run()