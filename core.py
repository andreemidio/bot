import datetime
import logging
import os

import pytz
from decouple import config
from telegram.ext import Updater, CommandHandler

from Bot import Bot
from features import request

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

bender_bot = Bot(False, False)

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
BOT_NAME = config("BOT_NAME")
DEBUG = True if os.getenv("DEBUG") else False

PORT = int(os.environ.get('PORT', '5000'))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info(str(PORT))


def msg(context):
    context.bot.send_photo(
        chat_id=context.job.context,
        photo=open("images/tio-sam-blog-1024x576.png", "rb"),
        caption="Alimente o Azure DevOps que existe em Você"
    )


def start(update, context):
    context.job_queue.run_daily(msg,
                                datetime.time(hour=17, minute=00, tzinfo=pytz.timezone('America/Sao_Paulo')),
                                days=(0, 1, 2, 3, 4, 5, 6), context=update.message.chat_id)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    request.DontStopmeNOW()

    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start, pass_job_queue=True))
    # dp.add_handler(CommandHandler("start", start, pass_job_queue=True))
    dp.add_error_handler(error)

    # updater.start_polling()

    logging.info(f'Porta de comunicação {PORT}')
    #
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=PORT,
    #                       url_path=TELEGRAM_TOKEN,
    #                       webhook_url=WEBHOOK_URL + TELEGRAM_TOKEN)
    updater.idle()


if __name__ == "__main__":
    main()
