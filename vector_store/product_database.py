import os
from pathlib import Path
import chromadb
import json
from config.config import Config
from chromadb.utils.embedding_functions.openai_embedding_function import OpenAIEmbeddingFunction
from utils.logger import setup_logger

logger = setup_logger("product_database.py")

class ProductDatabase:
    def __init__(self):
        # Определяем путь к корневой директории проекта
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.chroma_db_path = os.path.join(root_dir, 'chroma_db')

        # Проверяем, существует ли папка, и создаем ее, если нет
        if not os.path.exists(self.chroma_db_path):
            os.makedirs(self.chroma_db_path)

        # Инициализируем клиент с абсолютным путем к папке chroma_db
        self.client = chromadb.PersistentClient(path=self.chroma_db_path)
        self.embedding_function = OpenAIEmbeddingFunction(
            api_key=Config.OPENAI_API_KEY,
            model_name="text-embedding-ada-002"
        )
        self.collection = self.client.get_or_create_collection(
            name="product_database",
            embedding_function=self.embedding_function,
            metadata={"hnsw:space": "cosine"}
        )

    async def save_to_chroma(self):
        # Чтение JSON-файла асинхронно
        try:
            base_dir = Path(__file__).resolve().parent.parent
            produsts_list = base_dir / "vector_store/product_list.json"
            with open(produsts_list, "r", encoding="utf-8") as f:
                data = json.load(f)  # data — это список словарей (блоков данных)
                print(data)
        except Exception as e:
            logger.error(f"Ошибка при чтении файла product_list.json: {e}")
            return

        documents = []
        metadatas = []
        ids = []

        # Обработка каждого блока данных
        # Обработка каждого блока данных
        for idx, block in enumerate(data):
            # Преобразуем словарь в отформатированную JSON-строку
            product_data = json.dumps(block, indent=4, ensure_ascii=False)
            documents.append(product_data)

            product_name = block.get("Продукт")
            photo_id = block.get("ID фото")
            quantity = block.get("Количество кг")

            # Заменяем None на значение по умолчанию
            product_name = product_name if product_name is not None else "Unknown"
            photo_id = photo_id if photo_id is not None else ""
            quantity = quantity if quantity is not None else 0

            metadatas.append({
                "product_name": product_name,
                "photo_id": photo_id,
                "product_quantity": quantity,
            })

            # Генерация уникального идентификатора (можно заменить на свое поле, если оно есть)
            ids.append(str(idx))

            logger.debug(f"Обработан продукт: {product_name}, фото: {photo_id}, количество: {quantity}")

        # Сохранение данных в ChromaDB
        try:
            self.collection.upsert(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info("Данные успешно сохранены в ChromaDB")
        except Exception as e:
            logger.error(f"Ошибка при сохранении в ChromaDB: {str(e)}")
            raise

        # Сохраняем список id в отдельном файле для последующего удаления
        ids_file = os.path.join(self.chroma_db_path, 'saved_ids.json')
        try:
            with open(ids_file, 'w', encoding='utf-8') as f:
                json.dump(ids, f)
            logger.info(f"Список id сохранён в файле {ids_file}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении id: {e}")

    async def find_product_from_db(self, required_data: str, n_results: int = 5) -> dict:
        try:
            results = self.collection.query(
                query_texts=[required_data],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            num_results = len(results.get("documents", [[]])[0])
            logger.info(f"Найдено {num_results} результатов для запроса '{required_data}'")
            return results
        except Exception as e:
            logger.error(f"Ошибка при поиске по запросу '{required_data}': {e}")
            raise

    async def delete_all_saved_data(self):

        ids_file = os.path.join(self.chroma_db_path, 'saved_ids.json')

        # Проверка существования файла
        if not os.path.exists(ids_file):
            logger.warning(f"Файл {ids_file} не найден, удаление данных не требуется.")
            return

        try:
            with open(ids_file, 'r', encoding='utf-8') as f:
                saved_ids = json.load(f)
            logger.info(f"Считан список id для удаления: {saved_ids}")
        except Exception as e:
            logger.error(f"Ошибка при чтении файла {ids_file}: {e}")
            return

        try:
            self.collection.delete(ids=saved_ids)
            logger.info("Все данные успешно удалены из базы данных")
            # Опционально: удаляем файл с id после успешного удаления данных
            os.remove(ids_file)
            logger.info(f"Файл {ids_file} удалён")
        except Exception as e:
            logger.error(f"Ошибка при удалении данных: {e}")
