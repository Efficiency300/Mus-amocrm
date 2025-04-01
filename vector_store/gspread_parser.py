import asyncio
import json
import gspread
from gspread import GSpreadException
from icecream import ic

# Загрузка Service Account
TALK_ID_JSON_PATH = "Service_Account.json"
gc = gspread.service_account(filename=TALK_ID_JSON_PATH)

# Список нужных колонок
REQUIRED_COLUMNS = [
    "Название техники", "Альтернативное название", "Модель", "Двигатель",
    "Мощность двигателя (KW)", "Тип двигателя", "Вес (т)", "Объем ковши (m³)",
    "Альтернативное название ковша", "Гидравлический насос", "Гидрораспределитель",
    "Мотор хода", "Поворотный мотор", "Опции", "Трансмиссия"
]

async def fetch_product_records():
    try:
        # Открываем Google Sheet
        wks = gc.open('mus').sheet1

        # Получаем все данные
        records = await asyncio.to_thread(wks.get_all_values)

        if not records:
            ic("Таблица пустая")
            return []

        # Извлекаем заголовки
        headers = records[0]

        # Проверяем, какие нужные колонки есть в таблице
        column_indices = {col: headers.index(col) for col in REQUIRED_COLUMNS if col in headers}

        if not column_indices:
            ic("Не найдены нужные заголовки")
            return []

        # Обрабатываем строки (начиная со 2-й, т.к. 1-я — заголовки)
        parsed_data = []
        for row in records[1:]:
            parsed_row = {col: row[idx] if idx < len(row) else "" for col, idx in column_indices.items()}
            parsed_data.append(parsed_row)

        filename = "data.json"

        filename = "data.json"
        with open(filename, mode="w", encoding="utf-8") as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=4)

        ic(parsed_data)
        # Выводим результат
        return parsed_data

    except GSpreadException as e:
        ic(f"Ошибка при получении записей: {e}")
        return []


if __name__ == "__main__":
    asyncio.run(fetch_product_records())
