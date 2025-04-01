import openai
import json
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams
from config.config import Config

class QdrantSearch:
    def __init__(self,  qdrant_host="localhost", qdrant_port=6333, collection_name="excavators"):
        self.openai_client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        self.qdrant_client = QdrantClient(qdrant_host, port=qdrant_port)
        self.collection_name = collection_name
        self._initialize_collection()

    def _initialize_collection(self):
        """Создает коллекцию в Qdrant, если она не существует."""
        if not self.qdrant_client.collection_exists(self.collection_name):
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=1536, distance="Cosine")
            )

    def get_embedding(self, text):
        """Получает эмбеддинг текста с использованием OpenAI."""
        response = self.openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding

    def load_data(self, file_path):
        """Загружает данные из JSON-файла и вставляет их в Qdrant."""
        with open(file_path, "r", encoding="utf-8") as file:
            data_list = json.load(file)

        points = []
        for idx, data in enumerate(data_list, start=1):
            text_representation = " ".join([f"{k}: {v}" for k, v in data.items()])
            vector = self.get_embedding(text_representation)
            points.append(PointStruct(id=idx, vector=vector, payload=data))

        self.qdrant_client.upsert(collection_name=self.collection_name, points=points)
        print(f"Загружено {len(points)} объектов в Qdrant!")

    def search(self, query, top_k=3):
        """Ищет объекты в Qdrant на основе запроса."""
        query_vector = self.get_embedding(query)

        search_result = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=top_k,
            with_payload=True
        )

        # Получаем все payload
        payloads = [point.payload for point in search_result.points]

        return payloads


