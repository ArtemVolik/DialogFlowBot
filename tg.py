import environ
from telegram.ext import Updater, MessageHandler, Filters
from telegram import Bot, TelegramError
from integrations.google_dialogflow import get_agent_answer
from logs.logging_maintenace import get_logger_from_config


def update_handling(update, context):
    get_google_bot_answer = get_agent_answer(
        project_id,
        update.effective_chat.id,
        update.message.text,
        language_code)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=get_google_bot_answer.fulfillment_text)


def error_callback(context):
    try:
        raise context.error
    except TelegramError as er:
        logger.exception(er)


if __name__ == "__main__":
    env = environ.Env()
    env.read_env()
    logger = get_logger_from_config(
        'logs/log_config.yaml', env('NOTIFICATION_TOKEN'),
        env('NOTIFICATION_CHAT_ID'), "DialogBot")
    logger.warning('Telegram Dialog Bot launched')
    project_id = env('GOOGLE_PROJECT_ID')
    language_code = env('LANGUAGE_CODE')
    telegram_token = env('TELEGRAM_TOKEN')

    bot = Bot(token=telegram_token)
    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher
    dialog_handler = MessageHandler(
        Filters.text & (~Filters.command),
        update_handling)
    dispatcher.add_handler(dialog_handler)
    dispatcher.add_error_handler(error_callback)
    updater.start_polling()
