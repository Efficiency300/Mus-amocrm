import openai
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Filter
from config.config import Config


class QdrantSearch:
    def __init__(self, qdrant_host="localhost", qdrant_port=6333):
        self.openai_client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        self.qdrant_client = QdrantClient(qdrant_host, port=qdrant_port)

    def _initialize_collection(self, collection_name):
        """Создает коллекцию в Qdrant, если она не существует."""
        if not self.qdrant_client.collection_exists(collection_name):
            self.qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=1536, distance="Cosine")
            )

    def get_embedding(self, text):
        """Получает эмбеддинг текста с использованием OpenAI."""
        response = self.openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding

    def get_existing_message_ids(self, collection_name):
        """Получает список уже сохраненных ID сообщений."""
        try:
            response, _ = self.qdrant_client.scroll(
                collection_name=collection_name,
                scroll_filter=Filter(must=[]),
                limit=1000  # Максимальное количество сообщений, загружаемых за раз
            )
            return {point.payload["message_id"] for point in getattr(response, "points", [])}
        except Exception as e:
            print(f"Ошибка при получении сохраненных сообщений: {e}")
            return set()

    def process_snapshot(self, state_snapshot):
        """Обрабатывает StateSnapshot, извлекает последние два сообщения и сохраняет в Qdrant."""
        try:
            thread_id = state_snapshot.config.get("configurable", {}).get("thread_id")
            messages = state_snapshot.values.get("messages", [])

            if not thread_id or not messages:
                raise ValueError("Неверные данные: нет thread_id или сообщений")

            collection_name = {thread_id}
            self._initialize_collection(collection_name)
            existing_message_ids = self.get_existing_message_ids(collection_name)

            # Оставляем только два последних сообщения и сортируем их по порядку добавления
            messages = sorted(messages[-2:], key=lambda msg: msg.id)
            points = []

            for msg in messages:
                if hasattr(msg, "content") and msg.id not in existing_message_ids:
                    embedding = self.get_embedding(msg.content)
                    message_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, msg.id))  # Преобразуем в UUID
                    points.append(PointStruct(id=message_uuid, vector=embedding, payload={
                        "thread_id": thread_id,
                        "message_id": msg.id,
                        "message": msg.content,
                        "role": "human" if "HumanMessage" in str(type(msg)) else "ai"
                    }))

            if points:
                self.qdrant_client.upsert(collection_name=collection_name, points=points)
                print(f"Сохранено {len(points)} новых сообщений в Qdrant (thread_id={thread_id})")
            else:
                print("Нет новых данных для сохранения.")

        except Exception as e:
            print(f"Ошибка при обработке snapshot: {e}")

