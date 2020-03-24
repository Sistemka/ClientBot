import os
import re
import io
import uuid
import shutil
import logging
import requests
from pathlib import Path

from telegram import ChatAction, InputMediaPhoto, InputMedia
from telegram.ext import Filters, MessageHandler

from src import PIPELINES
from utils import send_action
from settings.paths import FILES_DIR
from models import Users

logger = logging.getLogger(__name__)


@send_action(ChatAction.UPLOAD_PHOTO)
def full_process_image(update, context):

    # write in db and save files
    uid = update.effective_user.id
    username = update.effective_user.username
    user, _ = Users.get_or_create(
        telegram_id=uid,
    )
    user.username = username

    image_id = update.message.photo[-1].file_id

    image_to_download_path = Path(FILES_DIR, f"{uuid.uuid4()}.jpeg")

    if user.photos is None:
        user.photos = []
    user.photos.append(image_to_download_path.as_posix())
    user.save()

    file = context.bot.get_file(image_id)
    file.download(image_to_download_path)

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
        return

    images_in_directory = os.listdir(files_to_return_dir)

    # remove full image from list
    full_image = None
    for image in images_in_directory:
        if image.startswith('full'):
            full_image = image
            break

    cropped_images_in_directory = [
        image for image in images_in_directory
        if not image.startswith('full')
    ]

    images_in_directory = sorted(cropped_images_in_directory)
    images_pairs = [
        images_in_directory[n:n + 3] for n
        in range(0, len(images_in_directory), 3)
    ]

    if full_image:
        context.bot.send_photo(
            chat_id=update.effective_user.id,
            photo=open(Path(files_to_return_dir, full_image), 'rb')
        )

    for image_pair in images_pairs:
        try:
            link = open(Path(files_to_return_dir, image_pair[1]), 'r').readline().replace('\n','')
            text = requests.get(link).text
            pic_link = re.findall(r'https:\/\/cdn\.ennergiia\.com\/new-images\/ennergiia-catalog\/\w+\/\w+\/\w+\.jpg', text)[0]
            pic = io.BytesIO(requests.get(pic_link).content)
            context.bot.send_media_group(
                chat_id=update.effective_user.id,
                media=[
                    InputMediaPhoto(open(Path(files_to_return_dir, image_pair[0]), 'rb'),
                                    caption = open(Path(files_to_return_dir, image_pair[1]), 'r').read()),
                    InputMediaPhoto(pic)
                ]
            )
        except:
            context.bot.send_message(
                text=open(Path(files_to_return_dir, image_pair[1]), 'r').read(),
                chat_id=update.effective_user.id,
            )

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
