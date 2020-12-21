import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import environ
import random
from integrations.google_dialogflow import get_agent_answer
import logging.config
from logs.logging_maintenace import logging_config_loading


def event_handle(event, vk_api):
    get_google_bot_answer = get_agent_answer(
        project_id, event.user_id, event.text, language_code)
    if get_google_bot_answer.intent.is_fallback:
        return
    vk_api.messages.send(
        user_id=event.user_id,
        message=get_google_bot_answer.fulfillment_text,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    env = environ.Env()
    env.read_env()
    logging_config_loading('logs/log_config.yaml', env('NOTIFICATION_TOKEN'), env('NOTIFICATION_CHAT_ID'))
    logger = logging.getLogger("DialogBot.Vkontakte")
    logger.warning('Vkontakte Dialog Bot launched')
    project_id = env('GOOGLE_PROJECT_ID')
    language_code = env('LANGUAGE_CODE')
    vk_group_token = env('VK_API_KEY')
    vk_session = vk_api.VkApi(token=vk_group_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

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
