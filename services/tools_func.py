
from utils.logger import setup_logger
from datetime import datetime
from status_crm.customer_card_manager import CustomerCardManager
from status_crm.lead_manager import LeadManager
from langchain_core.tools import tool

logger = setup_logger("llm_tools")
customer_card_manager = CustomerCardManager()
lead_manager = LeadManager()

class Tools:
    def __init__(self, lead_id: str, chat_id: str):
        self.lead_ids = lead_id
        self.chat_id = chat_id


    async def get_company_name(self, company_name: str) -> None:
        """используй когда клиент предоставляет название компании где работает

        :arg company_name:
        """
        await customer_card_manager.update_field_company_name(self.lead_ids, company_name)


    async def get_name(self, name: str) -> None:
        """используй когда клиент предоставляет свое имя

        :arg name:
        """
        await customer_card_manager.update_field_name(self.lead_ids, name)


    async def get_number(self, number: str) -> None:
        """используй когда клиент предоставляет свой номер

        :arg number:
        """
        await customer_card_manager.update_field_number(self.lead_ids, number)


    async def get_email(self, email: str) -> None:
        """используй когда клиент предоставляет свой email

        :arg email:
        """
        await customer_card_manager.update_field_email(self.lead_ids, email)


    async def get_address(self, address: str) -> None:
        """используй когда клиент предоставляет свой адресс

        :arg address:
        """
        await customer_card_manager.update_field_address(self.lead_ids, address)


    async def get_work_position(self, work_position: str) -> None:
        """используй когда клиент предоставляет свою позицию на работе

        :arg work_position:
        """
        await customer_card_manager.update_field_work_position(self.lead_ids, work_position)


    async def get_region(self, region: str) -> None:
        """используй когда клиент предоставляет регион где он работает

        :arg region:
        """
        await customer_card_manager.update_field_region(self.lead_ids, region)


    async def get_machine(self, machine: str) -> None:
        """используй когда клиент предоставляет выбрал определеную машину и верни ее имя

        :arg machine:
        """
        await customer_card_manager.update_field_machine(self.lead_ids, machine)


    async def get_type_client(self, type_client: str) -> None:
        """используй когда клиент предоставляется юр лицом или физ лицом
        :arg type_client:
        """
        await customer_card_manager.update_field_name(self.lead_ids, type_client)


    async def get_current_time(self, time_today: str) -> str:
        """используй чтобы узнать текуший день
        """

        today = datetime.now()
        current_time = today.strftime("%Y-%m-%d %H:%M:%S")

        return current_time


    async def send_transport_file(self , files: str) -> None:
        """используй когда просят отправимть файл с трансортом

        :arg files:
        """

        await send_photo(files, self.chat_id)


    async def change_client_stage(self , stage_ids: int) -> None:
        """используй когда нужно передать клиента на менеджера

        :arg stage_ids: 77777777
        """
        await lead_manager.change_stage(self.lead_ids, stage_ids)




