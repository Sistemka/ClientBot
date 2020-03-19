import uuid
from pathlib import Path

from utils import segmentator, search_engine, image_manager
from settings.paths import FILES_DIR


def generate_path_for_similar_image(image_path):
    image_path = Path(image_path)
    similar_image_name = f"{image_path.with_suffix('').name}_sim{image_path.suffix}"
    return Path(image_path.parent, similar_image_name)


def generate_path_for_similar_image_descr(image_path):
    image_path = Path(image_path)
    similar_image_name = f"{image_path.with_suffix('').name}_descr.txt"
    return Path(image_path.parent, similar_image_name)


def process(image_path):
    cropped_images_dir = Path(FILES_DIR, str(uuid.uuid4()))
    cropped_and_full_images = segmentator.get_files(
        image_path=image_path,
        cropped_images_dir=cropped_images_dir
    )
    if cropped_and_full_images is None:
        return None

    # remove full image from cropped list
    cropped_images = [
        image for image in cropped_and_full_images
        if not image.split('/')[-1].startswith('full')
    ]

    simular_urls = []
    for image in cropped_images:
        urls = search_engine.search(
            image_path=image
        )
        simular_urls.append(urls[0])
    for url, image in zip(simular_urls, cropped_images):
        image_manager.download_image(
            url=url,
            path_to_download=generate_path_for_similar_image(image)
        )
        with open(generate_path_for_similar_image_descr(image), 'w') as f:
            info = image_manager.get_image_info(url)
            for i in info.keys():
                if str(i) == 'link':
                    f.write(str(info.get(i))+'\n')
                elif str(i) not in {'path', 'пол', 'type', 'link'}:
                    f.write(f'{i}: {info.get(i)}\n')

    return cropped_images_dir
