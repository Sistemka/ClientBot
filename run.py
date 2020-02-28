from telegram.ext import Updater, PicklePersistence, messagequeue as mq

from app.bot import MQBot
from settings.config import TG_TOKEN
from app.handlers import main, proccess_images


def run():
    mqbot = MQBot(
        token=TG_TOKEN,
        mqueue=mq.MessageQueue(),
    )
    updater = Updater(
        bot=mqbot,
        use_context=True,
        persistence=PicklePersistence(filename='persistent_data')
    )
    dp = updater.dispatcher

    main.register(dp=dp)
    proccess_images.register(dp=dp)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    run()
