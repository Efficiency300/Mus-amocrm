import re
import aiohttp
from pathlib import Path
from config.config import Config
from server.amo_data import amo_api_data
from utils.logger import setup_logger
from utils.MarkdownProcessor import MarkdownProcessor

logger = setup_logger("send_message")
PHOTOS_DIR = Path(__file__).resolve().parent.parent / "photos"

async def file_send(photo: str, chat_id: str) -> None:
    amo_data = amo_api_data()
    photo_path = PHOTOS_DIR / f"{photo}.jpg"
    if not photo_path.exists():
        logger.warning(f"Файл {photo_path} не найден.")
        return

    form = aiohttp.FormData()
    for k, v in {
        "message": "",
        "chat_id": chat_id,
        "chat_token": amo_data['chat_token'],
        "amojo_id": amo_data['amojo_id'],
        "token": Config.SEND_ID
    }.items():
        form.add_field(k, v)

    with open(photo_path, "rb") as f:
        form.add_field(
            "file", f.read(),
            filename=photo_path.name,
            content_type="image/jpeg"
        )

    async with aiohttp.ClientSession() as s:
        async with s.post(Config.MESSAGE_SAND_URL, data=form) as r:
            r.raise_for_status()
            logger.info("Фотография отправлена: %s", await r.json())

async def send_text_message(massage, chat_id):
    amo_data = amo_api_data()
    clean_text = re.sub(r'~|【.*?】.*', '', await MarkdownProcessor.strip_markdown(massage))

    for part in re.split(r"\n\s*\n", clean_text):
        msg = part.strip()
        if not msg:
            continue

        data = {
            "message": msg,
            "chat_id": chat_id,
            "chat_token": amo_data["chat_token"],
            "amojo_id": amo_data["amojo_id"],
            "token": Config.SEND_ID
        }

        async with aiohttp.ClientSession() as s:
            async with s.post(Config.MESSAGE_SAND_URL, data=data) as r:
                r.raise_for_status()
                logger.info("Сообщение отправлено")
