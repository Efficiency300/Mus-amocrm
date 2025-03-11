from typing import Any, List, Callable, Dict, Annotated
from dataclasses import dataclass
from langchain_core.messages import HumanMessage
from langchain.schema import SystemMessage
from services.promt import promt
from langgraph.graph import END, START, StateGraph, add_messages
from langchain_openai import ChatOpenAI
from server.send_message import send_text_message
from config.config import Config
from services.tools_func import Tools
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition


@dataclass
class State:
    messages: Annotated[List[Any], add_messages]


class MainLlmService:
    """
    Класс для обработки сообщений пользователя с использованием LLM и графа обработки.
    """
    memory: MemorySaver = MemorySaver()
    react_graph: Any = None  # Глобальный граф для всех экземпляров

    def __init__(self, message_text: str, chat_id: str, lead_id: str) -> None:
        """
        Инициализация сервиса.
        :param message_text: Текст входящего сообщения.
        :param chat_id: Идентификатор чата.
        :param lead_id: Идентификатор лида.
        """
        self.llm = ChatOpenAI(
            model="gpt-4o",
            api_key=Config.OPENAI_API_KEY,
            temperature=0.2
        )
        self.sys_msg = SystemMessage(content=promt)
        self.message_text = message_text
        self.lead_id = lead_id
        self.chat_id = chat_id
        self.tools_instance = Tools(lead_id, chat_id)
        self.tools: List[Callable] = self._initialize_tools()

        # Инициализация графа, если он ещё не создан
        if MainLlmService.react_graph is None:
            self._create_graph()

    def _initialize_tools(self) -> List[Callable]:
        """
        Инициализирует и возвращает список инструментов для LLM.
        """
        return [
            self.tools_instance.get_company_name,
            self.tools_instance.get_name,
            self.tools_instance.get_number,
            self.tools_instance.get_email,
            self.tools_instance.get_address,
            self.tools_instance.get_work_position,
            self.tools_instance.get_region,
            self.tools_instance.get_machine,
            self.tools_instance.get_type_client,
            self.tools_instance.get_current_time,
            self.tools_instance.send_transport_file,
            self.tools_instance.change_client_stage,
        ]

    async def query_or_respond(self, state: State) -> Dict[str, Any]:
        """
        Обрабатывает сообщения с помощью LLM с подключенными инструментами и возвращает ответ.
        :param state: Объект состояния с сообщениями.
        :return: Словарь с результатирующими сообщениями.
        """
        llm_with_tools = self.llm.bind_tools(self.tools, parallel_tool_calls=True)
        response = await llm_with_tools.ainvoke([self.sys_msg] + state.messages)
        return {"messages": [response]}

    def _create_graph(self) -> None:
        """
        Создаёт граф обработки сообщений.
        """
        print("🚀 Создаем граф...")

        builder = StateGraph(State)
        builder.add_node("query_or_respond", self.query_or_respond)
        builder.add_node("tools", ToolNode(self.tools))
        builder.add_edge(START, "query_or_respond")
        builder.add_conditional_edges("query_or_respond", tools_condition)
        builder.add_edge("tools", "query_or_respond")
        builder.add_edge("query_or_respond", END)

        # Сохранение графа в атрибут класса
        MainLlmService.react_graph = builder.compile(checkpointer=self.memory)

    async def handle_user_message(self) -> str:
        """
        Обрабатывает входящие сообщения пользователя, инициирует обработку через граф и отправляет ответ.
        :return: Текст ответа.
        """
        config: Dict[str, Any] = {"configurable": {"thread_id": self.chat_id}}
        result = await MainLlmService.react_graph.ainvoke(
            {"messages": [HumanMessage(content=self.message_text)]}, config=config
        )


        # Извлечение и отправка ответа
        response_text = result["messages"][-1].content
        await send_text_message(response_text, self.chat_id)
        return response_text
