from telegram.ext import Updater, PicklePersistence, messagequeue as mq
# from telegram.utils.request import Request

from app.bot import MQBot
from settings.config import TG_TOKEN
from app.handlers import main, proccess_images


def run():
    # request = Request(con_pool_size=16)
    mqbot = MQBot(
        token=TG_TOKEN,
        # request=request,
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
