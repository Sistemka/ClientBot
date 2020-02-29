import uuid
from pathlib import Path

from utils import search_engine, image_manager
from settings.paths import FILES_DIR


def process_se(image_path):
    urls = search_engine.search(
        image_path=image_path
    )[:3]

    files_to_return_dir = Path(FILES_DIR, str(uuid.uuid4()))
    for url in urls:
        image_manager.download_image(
            url=url,
            path_to_download=Path(files_to_return_dir, str(uuid.uuid4()))
        )

    return files_to_return_dir
