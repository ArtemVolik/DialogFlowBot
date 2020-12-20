import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import environ
import random
from func import detect_intent_texts
import logging.config
import yaml


def event_handle(event, vk_api):
    get_google_bot_answer = detect_intent_texts(
        project_id, event.user_id, event.text, language_code)
    if get_google_bot_answer:
        vk_api.messages.send(
            user_id=event.user_id,
            message=get_google_bot_answer,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    env = environ.Env()
    env.read_env()

    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        config['handlers']['BotLogHandler']['tg_bot'] = env('NOTIFICATION_TOKEN')
        config['handlers']['BotLogHandler']['chat_id'] = env('NOTIFICATION_CHAT_ID')
        logging.config.dictConfig(config)

    logger = logging.getLogger("DialogBot.Vkontakte")
    logger.warning('Vkontakte Dialog Bot launched')

    project_id = env('GOOGLE_PROJECT_ID')
    language_code = env('LANGUAGE_CODE')
    vk_group_token = env('VK_API_KEY')
    vk_session = vk_api.VkApi(token=vk_group_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    logger.warning('VK bot launched')

    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    event_handle(event, vk)
        except ConnectionError as er:
            logger.warning(er)
            continue
        except Exception as er:
            logger.exception(er)
            continue
