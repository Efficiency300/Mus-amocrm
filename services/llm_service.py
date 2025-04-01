from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langgraph_supervisor import create_supervisor
from config.config import Config
from server.send_message import send_text_message
from services.tool_struc import get_tools
from services.promt import supervisor_promt




class MainTread:
    def __init__(self, chat_id: str, lead_id: str):
        self.model = ChatOpenAI(model="gpt-4o", api_key=Config.OPENAI_API_KEY)
        self.lead_id = lead_id
        self.chat_id = chat_id
        self.checkpointer = InMemorySaver()
        self.store = InMemoryStore()
        self.compiled_app = None
        self._initialized = False



    async def setup_supervisor(self, model):
        tools = await get_tools(self.lead_id, self.chat_id)
        role_agent = create_supervisor(
            agents=[],
            model=model,
            tools=tools,
            prompt=supervisor_promt,

        )
        return role_agent

    async def initialize(self):
        if not self._initialized:
            app = await self.setup_supervisor(self.model)
            self.compiled_app = app.compile(checkpointer=self.checkpointer, store=self.store)
            self._initialized = True
            print("Граф инициализирован:", self.compiled_app)

    async def main(self, message_text: str):
        if not self._initialized:
            await self.initialize()

        config = {"configurable": {"thread_id": self.chat_id}}

        # Загружаем текущее состояние
        state_snapshot = await self.compiled_app.aget_state(config)


        # Извлекаем values из StateSnapshot
        if state_snapshot is None or not hasattr(state_snapshot, 'values') or not state_snapshot.values:
            current_state = {"messages": []}
        else:
            current_state = state_snapshot.values

        if "messages" not in current_state:
            current_state["messages"] = []

        # Добавляем новое сообщение
        current_state["messages"].append({"type": "human", "content": message_text})


        # Выполняем вызов
        result = await self.compiled_app.ainvoke(input=current_state, config=config)

        # Сохраняем обновлённое состояние
        await self.compiled_app.aupdate_state(config, result)

        from vector_store.vector_db_message import QdrantSearch
        # Проверяем состояние после сохранения
        updated_state = await self.compiled_app.aget_state(config)
        qdrant = QdrantSearch()
        qdrant.process_snapshot(updated_state)
        print("Сырое состояние после сохранения:", updated_state)


        # Отправляем ответ
        response_text = result["messages"][-1].content
        await send_text_message(response_text, self.chat_id)
        return response_text