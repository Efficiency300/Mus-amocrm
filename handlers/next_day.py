import asyncio
from datetime import datetime, timedelta
from pathlib import Path
import json
from utils.logger import setup_logger
from status_crm.lead_manager import LeadManager
logging = setup_logger("next_day")
lead_manager = LeadManager()

# Константы
BASE_DIR = Path(__file__).resolve().parent.parent
TALK_ID_JSON = BASE_DIR / "config/next_day_order.json"
CHECK_TIME = "23:08"  # Время запуска задачи
TO_DAYS_TIME = 72349682
DAY_BEFORE = 72349674

async def read_json(file_path):
    """Асинхронное чтение JSON файла."""
    if not file_path.exists():
        logging.error(f"Файл {file_path} не найден.")
        return {}
    try:
        return await asyncio.to_thread(lambda: json.load(open(file_path, 'r')))
    except json.JSONDecodeError as e:
        logging.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
    except Exception as e:
        logging.error(f"Ошибка чтения файла {file_path}: {e}")
    return {}


async def write_json(file_path, data):
    """Асинхронная запись JSON файла."""
    try:
        # Open the file with 'with' context to ensure it's properly handled
        with open(file_path, 'w') as f:
            # Pass the file object directly to json.dump within the async thread
            await asyncio.to_thread(json.dump, data, f, indent=4)
        logging.info("JSON файл успешно обновлен.")
    except Exception as e:
        logging.error(f"Ошибка записи файла {file_path}: {e}")

async def check_dates(file_path):
    """Проверка дат, обновление статусов и удаление обработанных записей."""
    current_date = datetime.now().strftime("%d-%m-%Y")
    next_day_date = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")

    json_data = await read_json(file_path)
    if not json_data:
        return

    keys_to_delete = []

    for key, date in json_data.items():
        try:
            if date == next_day_date:
                await lead_manager.change_stage(key, DAY_BEFORE)
                logging.info(f"Обновлен этап для ключа {key} на {DAY_BEFORE}")
            elif date == current_date:
                await lead_manager.change_stage(key, TO_DAYS_TIME)
                logging.info(f"Обновлен этап для ключа {key} на {TO_DAYS_TIME}")
                keys_to_delete.append(key)
        except Exception as e:
            logging.error(f"Ошибка при обработке ключа {key}: {e}")

    # Удаление обработанных ключей
    for key in keys_to_delete:
        json_data.pop(key, None)

    await write_json(file_path, json_data)

async def scheduler():
    """Планировщик задач."""
    while True:
        now = datetime.now().strftime("%H:%M")
        if now == CHECK_TIME:
            logging.info(f"Запуск check_dates в {now}")
            await check_dates(TALK_ID_JSON)
        await asyncio.sleep(60)  # Проверка каждую минуту

if __name__ == "__main__":
    logging.info("Программа запущена. Ожидает выполнения задач...")
    try:
        asyncio.run(scheduler())
    except KeyboardInterrupt:
        logging.info("Программа завершена пользователем.")
