from langchain.tools import StructuredTool
from services.tools_func import Tools


async def get_tools(lead_id: str, chat_id: str):
    tools_instance = Tools(lead_id, chat_id)

    return [

        StructuredTool.from_function(
            name="get_name",
            func=None,
            coroutine=tools_instance.get_name,
            description="""Запись имени клиента при предоставлении в CRM-системе""",
        ),

        StructuredTool.from_function(
            name="get_number",
            func=None,
            coroutine=tools_instance.get_number,
            description='''Запись номера телефона клиента при предоставлении в CRM-системе''',
        ),

        StructuredTool.from_function(
            name="get_company_name",
            func=None,
            coroutine=tools_instance.get_company_name,
            description='''Запись названия компании  клиента при предоставлении в CRM-системе''',
        ),

        StructuredTool.from_function(
            name="get_current_time",
            func=None,
            coroutine=tools_instance.get_current_time,
            description="Returns the current time."
        ),
        StructuredTool.from_function(
            name="get_email",
            func=None,
            coroutine=tools_instance.get_email,
            description="""Запись электроную почту  клиента при предоставлении в CRM-системе""",
        ),

        StructuredTool.from_function(
            name="get_address",
            func=None,
            coroutine=tools_instance.get_address,
            description="""Запись адрес клиента при предоставлении в CRM-системе""",
        ),

        StructuredTool.from_function(
            name="get_work_position",
            func=None,
            coroutine=tools_instance.get_work_position,
            description="""Запись позицию  клиента на работе при предоставлении в CRM-системе""",
        ),

        StructuredTool.from_function(
            name="get_region",
            func=None,
            coroutine=tools_instance.get_region,
            description='''Запись региона клиента при предоставлении в CRM-системе''',
        ),

        StructuredTool.from_function(
            name="get_machine",
            func=None,
            coroutine=tools_instance.get_machine,
            description="Запись название машины клиента для приобретиния при предоставлении в CRM-системе",
        ),

        StructuredTool.from_function(
            name="get_type_client",
            func=None,
            coroutine=tools_instance.get_type_client,
            description="Запись типа клиента при предоставлении в CRM-системе",
        ),

        StructuredTool.from_function(
            name="get_machine_data",
            func=None,
            coroutine=tools_instance.get_machine_data,
            description='''используй для получения информации о техники при запросе клиентом о техники''',

        ),



    ]


