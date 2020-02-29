import os
import uuid
import shutil
import logging
from pathlib import Path

from telegram import ChatAction, InputMediaPhoto
from telegram.ext import Filters, MessageHandler

from src import PIPELINES
from utils import send_action
from settings.paths import FILES_DIR

logger = logging.getLogger(__name__)


@send_action(ChatAction.UPLOAD_PHOTO)
def full_process_image(update, context):
    image_id = update.message.photo[0].file_id

    image_to_download_path = Path(FILES_DIR, f"{uuid.uuid4()}.jpeg")
    file = context.bot.get_file(image_id)
    file.download(image_to_download_path)

    if update.message['caption'] == 'se':
        search_image(update, context)
        return

    context.bot.send_message(
        text='Взял в обработку, подожди немного 🧐',
        chat_id=update.effective_user.id,
    )

    files_to_return_dir = PIPELINES['full'](image_to_download_path)
    if files_to_return_dir is None:
        context.bot.send_message(
            text='Я не нашел никакой одежды на этой картинке 😑',
            chat_id=update.effective_user.id,
        )
        os.remove(image_to_download_path)
        return

    images_in_directory = sorted(os.listdir(files_to_return_dir))
    images_pairs = [
        images_in_directory[n:n + 2] for n
        in range(0, len(images_in_directory), 2)
    ]

    for image_pair in images_pairs:
        context.bot.send_media_group(
            chat_id=update.effective_user.id,
            media=[
                InputMediaPhoto(open(Path(files_to_return_dir, image_pair[0]), 'rb')),
                InputMediaPhoto(open(Path(files_to_return_dir, image_pair[1]), 'rb'))
            ]
        )
    os.remove(image_to_download_path)
    shutil.rmtree(files_to_return_dir)


def search_image(update, context):
    image_id = update.message.photo[0].file_id

    image_to_download_path = Path(FILES_DIR, f"{uuid.uuid4()}.jpeg")
    file = context.bot.get_file(image_id)
    file.download(image_to_download_path)

    context.bot.send_message(
        text='Начинаю искать похожие картинки в базе, подожди немного 🧐',
        chat_id=update.effective_user.id,
    )

    files_to_return_dir = PIPELINES['se'](image_to_download_path)
    images_in_directory = sorted(os.listdir(files_to_return_dir))

    media = []
    for image in images_in_directory:
        media.append(InputMediaPhoto(open(Path(files_to_return_dir, image), 'rb')))
    context.bot.send_media_group(
        chat_id=update.effective_user.id,
        media=media
    )
    os.remove(image_to_download_path)
    shutil.rmtree(files_to_return_dir)


def send_message(update, context):
    context.bot.send_message(
        text='Нужно скинуть фотку 😑',
        chat_id=update.effective_user.id,
    )


def error(update, context):
    logger.error('Update "%s" caused error "%s"', update, context.error)
    context.bot.send_message(
        text='Что-то пошло не так, простите 😞',
        chat_id=update.effective_user.id,
    )


def register(dp):
    dp.add_handler(MessageHandler(Filters.photo, full_process_image))
    dp.add_handler(MessageHandler(Filters.text, send_message))
    dp.add_error_handler(error)
