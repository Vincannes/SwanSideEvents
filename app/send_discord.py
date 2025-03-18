import gazu

from adapters.discord_wrapper import DiscordBot
from adapters.logging_wrapper import get_logger
from adapters.config_file import get_config_file

LOGGER = get_logger()
config = get_config_file()

# VARIABLES
TOKEN = config.get('Discord', 'TOKEN')
MESSAGE_TYPE = "{user} change status ({status}) for [{type_of_entity}] {entity_type} {entity}:\n    '{message}'"

def _get_channel_id(event):
    project_id = event.get("project_id")
    prod_name = gazu.project.get_project(project_id).get('name')
    channel_id = config.getint(prod_name.lower(), 'CHANNEL_ID')
    return channel_id


def _get_kitsu_data(data):
    task_id = data.get("task_id")
    user_id = data.get("person_id")
    project_id = data.get("project_id")
    status_id = data.get("new_task_status_id")

    try:
        status = gazu.task.get_task_status(status_id).get("name")
        kt_task = gazu.task.get_task(task_id)
        comment = gazu.task.get_last_comment_for_task(kt_task)
    except gazu.exception.RouteNotFoundException as e:
        LOGGER.error(f"[Erreur] sur la récupération des données: {e}")
        return None

    type_of_entity = kt_task.get("task_type").get("for_entity")
    username = "{} {}".format(
        comment.get("person").get("last_name"), comment.get("person").get("first_name")
    )
    message = comment.get("text") or "Missing value"

    if type_of_entity.lower() == "asset":
        entity_type = kt_task.get("entity_type").get("name")
    else:
        entity_type = kt_task.get("sequence").get("name")

    entity = kt_task.get("entity").get("name")
    return MESSAGE_TYPE.format(
        status=status,
        entity_type=entity_type,
        entity=entity,
        user=username,
        type_of_entity=type_of_entity,
        message=message
    )


def on_task_status_change(data):
    print(f" Tâche modifiée : {data}")
    msg = _get_kitsu_data(data)
    if not msg:
        event_id = data.get("task_id")
        LOGGER.error(f"Failed to send message to event {event_id}")
        return

    LOGGER.info(f"Message send:\n{msg}")
    channel_id = _get_channel_id(data)

    bot = DiscordBot(TOKEN, channel_id)
    bot.run(msg)
