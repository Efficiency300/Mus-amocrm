import asyncio
import json
from pathlib import Path
import aiofiles
import gspread
from gspread import GSpreadException
from icecream import ic
BASE_DIR = Path(__file__).resolve().parent.parent
TALK_ID_JSON_PATH = BASE_DIR / "Service_Account.json"
gc = gspread.service_account(filename=TALK_ID_JSON_PATH)


async def fetch_product_records():
    try:
        wks = gc.open('DonHamon').sheet1
        # Получение всех записей
        records = await asyncio.to_thread(wks.get_all_records)
        products_json = format_product_data_as_json(records)
        print(products_json)

        async with aiofiles.open('product_list.json', mode='w', encoding='utf-8') as f:
            await f.write(products_json)
        return products_json

    except GSpreadException as e:
        ic(f"Ошибка при получении записей: {e}")
        return []


def format_product_data_as_json(products_list):
    formatted_products = []
    for product in products_list:
        formatted_product = {
            'img_id': f"img_{product['ID фото']}",
            'Единица измерения': product['ед.им'],
            'Категория': product['Категория'],
            'Количество кг': product['количество кг'],
            'Примечания': product['Примечания'],
            'Продукт': product['Продукт'],
            'Цена': product['Цена'],
            'наличие свинины': product['без свинины']
        }
        formatted_products.append(formatted_product)
    return json.dumps(formatted_products, ensure_ascii=False, indent=4)



