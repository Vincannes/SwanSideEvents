import gazu
import logging
import discord
from config import config

# VARIABLES
TOKEN = config.get('Discord', 'TOKEN')
MESSAGE_TYPE = "{user} change status ({status}) for [{type_of_entity}] {entity_type} {entity}:\n    '{message}'"

# DISCORD
class DiscordBot(object):
    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = channel_id
        intents = discord.Intents.default()
        intents.messages = True
        intents.guilds = True
        intents.message_content = True
        self.client = discord.Client(intents=intents)

    def run(self, message):
        @self.client.event
        async def on_ready():
            logging.info(f'Bot connect has {self.client.user}')
            channel = self.client.get_channel(self.channel_id)
            if channel:
                logging.info(f'Channel found : {self.channel_id}')
                await channel.send(message)
            else:
                logging.error(f'Channel not found : {self.channel_id}')
            await self.client.close()

        self.client.run(self.token)


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
        logging.error(f"[Erreur] sur la récupération des données: {e}")
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
        logging.error(f"Failed to send message to event {event_id}")
        return

    logging.info(f"Message send:\n{msg}")
    channel_id = _get_channel_id(data)

    bot = DiscordBot(TOKEN, channel_id)
    bot.run(msg)

