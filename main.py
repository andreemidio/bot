import datetime
import logging

import pytz
from telegram.ext import Updater, CommandHandler

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def msg(context):
    context.bot.send_photo(
        chat_id=context.job.context,
        photo=open("images/tio-sam-blog-1024x576.png", "rb"),
        caption="Alimente o Azure DevOps que existe em Você"
    )


def start(update, context):
    context.job_queue.run_daily(msg,
                                datetime.time(hour=18, minute=53, tzinfo=pytz.timezone('America/Sao_Paulo')),
                                days=(0, 1, 2, 3, 4, 5, 6), context=update.message.chat_id)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater("1924902771:AAGH5c-EeFDSYPPZNS9hsjlQhNAPRFjI3Mw", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start, pass_job_queue=True))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
