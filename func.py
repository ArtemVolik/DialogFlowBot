import logging
from google.cloud import dialogflow
from telegram import Bot


class BotLogHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.telegram_bot = Bot(token=tg_bot)
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.telegram_bot.send_message(chat_id=self.chat_id, text=log_entry)


logger = logging.getLogger("DialogBot.GoogleRequest")


def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    logger.debug('Session path: {}\n'.format(session))

    text_input = dialogflow.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(
            request={'session': session, 'query_input': query_input})
        logger.info('Make request to google DialogFlow')
    except ConnectionError as er:
        logger.exception(er)
    except Exception as er:
        logging.exception(er)

    if response.query_result.intent.is_fallback:
        return

    return response.query_result.fulfillment_text
