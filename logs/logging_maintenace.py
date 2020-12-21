import logging

from telegram import Bot
import yaml


class BotLogHandler(logging.Handler):
    def __init__(self, tg_token, chat_id):
        super().__init__()
        self.telegram_bot = Bot(token=tg_token)
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.telegram_bot.send_message(chat_id=self.chat_id, text=log_entry)


def logging_config_loading(log_config: str, notification_token: str, notification_chat_id: str):
    log_config = log_config
    with open(log_config, 'r') as f:
        config = yaml.safe_load(f.read())
        config['handlers']['BotLogHandler']['tg_token'] = notification_token
        config['handlers']['BotLogHandler']['chat_id'] = notification_chat_id
        logging.config.dictConfig(config)
