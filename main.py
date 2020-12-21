import environ
from telegram.ext import Updater, MessageHandler, Filters
from telegram import Bot
from integrations.google_dialogflow import get_agent_answer
import logging.config
from logs.logging_maintenace import logging_config_loading


def echo(update, context):
    get_google_bot_answer = get_agent_answer(project_id, update.effective_chat.id, update.message.text,
                                                language_code)
    if not get_google_bot_answer:
        return
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_google_bot_answer)


if __name__ == "__main__":
    env = environ.Env()
    env.read_env()
    logging_config_loading('logs/log_config.yaml', env('NOTIFICATION_TOKEN'), env('NOTIFICATION_CHAT_ID'))
    logger = logging.getLogger("DialogBot")
    logger.warning('Telegram Dialog Bot launched')

    telegram_token = env('TELEGRAM_TOKEN')
    bot = Bot(token=telegram_token)
    project_id = env('GOOGLE_PROJECT_ID')
    language_code = env('LANGUAGE_CODE')
    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)
    while True:
        try:
            updater.start_polling()
        except ConnectionError as er:
            logger.warning(er)
        except Exception as er:
            logger.exception(er)
