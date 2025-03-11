import aiohttp
from utils.logger import setup_logger
from config.config import Config

logger = setup_logger("customer_card_manager")

class CustomerCardManager:
    def __init__(self):
        self.base_url = Config.URL
        self.headers = {
            "Authorization": f"Bearer {Config.SEND_ID}",
            "Content-Type": "application/json"
        }



    async def update_field_company_name(self, lead_id: str, company_name: str) -> None:
        url = f"{self.base_url}/{lead_id}"
        data = {
            'custom_fields_values': [
                {'field_id': 1033997, 'values': [{'value': company_name}]}
            ]
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(url, headers=self.headers, json=data) as response:
                    if response.status == 200:
                        logger.info("company name fields successfully updated.")
                    else:
                        try:
                            error_details = await response.json()
                        except aiohttp.ContentTypeError:
                            logger.error(f"Error updating company name fields: {response.status}, URL: {url}, Details: {error_details}")

        except aiohttp.ClientError as e:
            logger.error(f"Network error while updating company name fields: {e}, URL: {url}")
        except Exception as e:
            logger.error(f"Unexpected error in update_company_name: {e}")

    async def update_field_name(self, lead_id: str, name: str) -> None:
        url = f"{self.base_url}/{lead_id}"
        data = {
            'custom_fields_values': [
                {'field_id': 1033999, 'values': [{'value': name}]}
            ]
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(url, headers=self.headers, json=data) as response:
                    if response.status == 200:
                        logger.info("Name fields successfully updated.")
                    else:
                        try:
                            error_details = await response.json()
                        except aiohttp.ContentTypeError:
                            logger.error(f"Error updating Name fields: {response.status}, URL: {url}, Details: {error_details}")

        except aiohttp.ClientError as e:
            logger.error(f"Network error while updating Name fields: {e}, URL: {url}")
        except Exception as e:
            logger.error(f"Unexpected error in update_field_Name: {e}")

    async def update_field_number(self, lead_id: str, number: str) -> None:
        url = f"{self.base_url}/{lead_id}"
        data = {
            'custom_fields_values': [
                {'field_id': 1034001, 'values': [{'value': number}]}
            ]
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(url, headers=self.headers, json=data) as response:
                    if response.status == 200:
                        logger.info("Number fields successfully updated.")
                    else:
                        try:
                            error_details = await response.json()
                        except aiohttp.ContentTypeError:
                            logger.error(f"Error updating number fields: {response.status}, URL: {url}, Details: {error_details}")

        except aiohttp.ClientError as e:
            logger.error(f"Network error while updating number fields: {e}, URL: {url}")
        except Exception as e:
            logger.error(f"Unexpected error in update_field_number: {e}")

    async def update_field_email(self, lead_id: str, email: str) -> None:
        url = f"{self.base_url}/{lead_id}"
        data = {
            'custom_fields_values': [
                {'field_id': 1034001, 'values': [{'value': email}]}
            ]
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(url, headers=self.headers, json=data) as response:
                    if response.status == 200:
                        logger.info("email fields successfully updated.")
                    else:
                        try:
                            error_details = await response.json()
                        except aiohttp.ContentTypeError:
                            logger.error(f"Error updating email fields: {response.status}, URL: {url}, Details: {error_details}")

        except aiohttp.ClientError as e:
            logger.error(f"Network error while updating products fields: {e}, URL: {url}")
        except Exception as e:
            logger.error(f"Unexpected error in update_field_products: {e}")

    async def update_field_address(self, lead_id: str, address: str) -> None:
        url = f"{self.base_url}/{lead_id}"
        data = {
            'custom_fields_values': [
                {'field_id': 1368365, 'values': [{'value': address}]}
            ]
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(url, headers=self.headers, json=data) as response:
                    if response.status == 200:
                        logger.info("address fields successfully updated.")
                    else:
                        try:
                            error_details = await response.json()
                        except aiohttp.ContentTypeError:
                            logger.error(f"Error updating address fields: {response.status}, URL: {url}, Details: {error_details}")

        except aiohttp.ClientError as e:
            logger.error(f"Network error while updating address fields: {e}, URL: {url}")
        except Exception as e:
            logger.error(f"Unexpected error in update_field_address: {e}")

    async def update_field_work_position(self, lead_id: str, work_position: str) -> None:
        url = f"{self.base_url}/{lead_id}"
        data = {
            'custom_fields_values': [
                {'field_id': 1368367, 'values': [{'value': work_position}]}
            ]
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(url, headers=self.headers, json=data) as response:
                    if response.status == 200:
                        logger.info("work_position fields successfully updated.")
                    else:
                        try:
                            error_details = await response.json()
                        except aiohttp.ContentTypeError:
                            logger.error(f"Error updating work_position fields: {response.status}, URL: {url}, Details: {error_details}")

        except aiohttp.ClientError as e:
            logger.error(f"Network error while updating work_position fields: {e}, URL: {url}")
        except Exception as e:
            logger.error(f"Unexpected error in update_field_work_position: {e}")

    async def update_field_region(self, lead_id: str, region: str) -> None:
        url = f"{self.base_url}/{lead_id}"
        data = {
            'custom_fields_values': [
                {'field_id': 1368369, 'values': [{'value': region}]}
            ]
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(url, headers=self.headers, json=data) as response:
                    if response.status == 200:
                        logger.info("region fields successfully updated.")
                    else:
                        try:
                            error_details = await response.json()
                        except aiohttp.ContentTypeError:
                            logger.error(f"Error updating region fields: {response.status}, URL: {url}, Details: {error_details}")

        except aiohttp.ClientError as e:
            logger.error(f"Network error while updating region fields: {e}, URL: {url}")
        except Exception as e:
            logger.error(f"Unexpected error in update_field_region: {e}")


    async def update_field_machine(self, lead_id: str, machine: str) -> None:
        url = f"{self.base_url}/{lead_id}"
        data = {
            'custom_fields_values': [
                {'field_id': 1368371, 'values': [{'value': machine}]}
            ]
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(url, headers=self.headers, json=data) as response:
                    if response.status == 200:
                        logger.info("machine fields successfully updated.")
                    else:
                        try:
                            error_details = await response.json()
                        except aiohttp.ContentTypeError:
                            logger.error(f"Error updating machine fields: {response.status}, URL: {url}, Details: {error_details}")

        except aiohttp.ClientError as e:
            logger.error(f"Network error while updating machine fields: {e}, URL: {url}")
        except Exception as e:
            logger.error(f"Unexpected error in update_field_machine: {e}")

    async def update_field_type_client(self, lead_id: str, type_client: str) -> None:
        url = f"{self.base_url}/{lead_id}"
        data = {
            'custom_fields_values': [
                {'field_id': 1368373, 'values': [{'value': type_client}]}
            ]
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(url, headers=self.headers, json=data) as response:
                    if response.status == 200:
                        logger.info("type_client fields successfully updated.")
                    else:
                        try:
                            error_details = await response.json()
                        except aiohttp.ContentTypeError:
                            logger.error(f"Error updating type_client fields: {response.status}, URL: {url}, Details: {error_details}")

        except aiohttp.ClientError as e:
            logger.error(f"Network error while updating type_client fields: {e}, URL: {url}")
        except Exception as e:
            logger.error(f"Unexpected error in update_field_type_client: {e}")


