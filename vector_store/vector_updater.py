import asyncio
from datetime import datetime, timedelta
from utils.logger import setup_logger
from vector_store.sheet_data import fetch_product_records
from vector_store.product_database import ProductDatabase

logging = setup_logger("vector_updater")
product_database = ProductDatabase()

CHECK_TIME = "00:25"

def get_next_run_time(target_time: str) -> datetime:
    """Вычисляет время следующего запуска задачи на основе указанного времени (HH:MM)."""
    now = datetime.now()
    target = datetime.strptime(target_time, "%H:%M").time()
    next_run = datetime.combine(now.date(), target)
    if next_run <= now:
        next_run += timedelta(days=1)
    return next_run

async def run_tasks():
    """Выполняет необходимые задачи по обновлению данных."""
    logging.info(f"Запуск check_dates в {datetime.now().strftime('%H:%M')}")
    await product_database.delete_all_saved_data()
    await fetch_product_records()
    await product_database.save_to_chroma()

async def scheduler():
    """Планировщик задач, запускающий run_tasks() каждый день в заданное время."""
    while True:
        next_run = get_next_run_time(CHECK_TIME)
        wait_seconds = (next_run - datetime.now()).total_seconds()
        logging.info(f"Ожидание {wait_seconds:.2f} секунд до следующего запуска задачи в {CHECK_TIME}")
        await asyncio.sleep(wait_seconds)
        await run_tasks()

if __name__ == "__main__":
    logging.info("Программа запущена. Ожидает выполнения задач...")
    try:
        asyncio.run(scheduler())
    except KeyboardInterrupt:
        logging.info("Программа завершена пользователем.")
