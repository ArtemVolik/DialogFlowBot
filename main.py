import environ
from telegram.ext import Updater, MessageHandler, Filters
from telegram import Bot
from func import detect_intent_texts
import logging.config
import yaml


def echo(update, context):
    get_google_bot_answer = detect_intent_texts(project_id, update.effective_chat.id, update.message.text,
                                                language_code)
    if not get_google_bot_answer:
        return
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_google_bot_answer)


if __name__ == "__main__":
    env = environ.Env()
    env.read_env()

    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        config['handlers']['BotLogHandler']['tg_bot'] = env('NOTIFICATION_TOKEN')
        config['handlers']['BotLogHandler']['chat_id'] = env('NOTIFICATION_CHAT_ID')
        logging.config.dictConfig(config)

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
