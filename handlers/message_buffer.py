import asyncio
import random
from collections import defaultdict
import json
from services.photo_service import PhotoService
from services.stt_service import STTService
from config.config import Config
from status_crm.lead_manager import LeadManager
from utils.JsonDataBase import JSONDatabase
from pathlib import Path
from typing import Dict, List, Union, Optional
from utils.logger import setup_logger
from services.llm_service import MainLlmService

logger = setup_logger("message_buffer")
BASE_DIR = Path(__file__).resolve().parent.parent
TALK_ID_JSON_PATH = BASE_DIR / "config/talk_id.json"


class BufferManager:
    def __init__(self, rand_first=8):
        self.user_buffers: Dict[str, List[Dict[str, str] | str]] = defaultdict(list)
        self.user_timers = {}
        self.rand_first = rand_first
        self.db = JSONDatabase(TALK_ID_JSON_PATH)
        self.photo_service = PhotoService()
        self.stt_service = STTService()
        self.lead_manager = LeadManager()

    async def add_to_buffer(self, chat_id: str, data: Union[Dict[str, str], str]) -> None:
        self.user_buffers[chat_id].append(data)

    async def check_and_return(self, talk_id: str, current_time: int, entity_id: str) -> Optional[dict]:
        past_time = await self.db.get(talk_id)
        if past_time and int(past_time) >= current_time:
            return {"status": "success", "data": {"entity_id": entity_id}}
        return None

    async def process_attachments(self, chat_id: str) -> tuple[str, str, str]:
        image_description = ""
        transcribed_text = ""
        processed_text_parts = []

        for msg in self.user_buffers.pop(chat_id, []):
            if isinstance(msg, dict):
                if msg.get("type") == "image":
                    image_url = msg.get("content")
                    image_response = await self.photo_service.process_image_from_url(image_url)
                    if image_response:
                        image_data = json.loads(image_response)
                        image_description += f"\n\nКонтекст изображения: {image_data.get('description', '')}"
                elif msg.get("type") == "voice":
                    voice_url = msg.get("content")
                    transcribed = await self.stt_service.transcribe(voice_url)
                    if transcribed:
                        transcribed_text += f"\n\nТранскрибированное голосовое сообщение: {transcribed}"
            else:
                processed_text_parts.append(msg)

        return "\n".join(processed_text_parts), image_description, transcribed_text

    async def process_target_audience(self, chat_id: str, entity_id: str, talk_id: str, current_time: int , client_lead_id: str) -> Optional[dict]:
        try:
            await asyncio.sleep(random.randint(5, self.rand_first))
            message_text = await self.process_attachments(chat_id)

            if client_lead_id == Config.UNSORTED:
                await asyncio.sleep(10)
                resuts = await self.lead_manager.stage_info(entity_id)
                if resuts == Config.AI_WORKS:
                    check_result = await self.check_and_return(talk_id, current_time, entity_id)
                    if check_result:
                        return check_result
                    content_messages = f"{message_text[0]}  {message_text[1]}  {message_text[0]}"
                    print(content_messages)
                    await asyncio.sleep(random.randint(5, self.rand_first))
                    llm_content = MainLlmService(content_messages, chat_id, entity_id)

                    await llm_content.handle_user_message()

                    await self.db.add(talk_id, current_time)
                return {"status": "success", "message": "User status updated"}


            self.user_buffers.pop(chat_id, None)
            self.user_timers.pop(chat_id, None)

        except Exception as e:
            logger.error(f"Error processing target audience for {chat_id}: {e}")


    async def start_processing(self, chat_id: str, entity_id: str) -> None:
        try:
            await asyncio.sleep(random.randint(4, self.rand_first))
            message_text = await self.process_attachments(chat_id)
            content_messages = f"{message_text[0]}  {message_text[1]}  {message_text[2]}"
            print(content_messages)
            await asyncio.sleep(random.randint(5, self.rand_first))
            llm_content = MainLlmService(content_messages, chat_id , entity_id)
          


            await llm_content.handle_user_message()
            self.user_buffers.pop(chat_id, None)
            self.user_timers.pop(chat_id, None)
        except Exception as e:
            logger.error(f"Error starting processing for {chat_id}: {e}")
