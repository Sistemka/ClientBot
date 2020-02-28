from telegram import ParseMode
from telegram.ext import CommandHandler

from models import Users


def start(update, context):
    context.user_data.clear()

    uid = update.effective_user.id
    username = update.effective_user.username
    user, _ = Users.get_or_create(
        telegram_id=uid,
        username=username
    )
    user.save()

    context.bot.send_message(
        text="Привет! Я роспознаю одежду на картинке и ищу похожую 👋!",
        chat_id=update.effective_user.id,
        parse_mode=ParseMode.MARKDOWN
    )
    return -1


def register(dp):
    dp.add_handler(CommandHandler('start', start))
