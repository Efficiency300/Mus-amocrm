from fastapi import FastAPI, Request
import asyncio
from urllib.parse import parse_qs
import uvicorn
from config.config import Config
from handlers.message_buffer import BufferManager
from status_crm.lead_manager import LeadManager
from server.server_data import ServerData

app = FastAPI()
lead_manager = LeadManager()
buffer_manager = BufferManager()

@app.post("/")
async def client_data(r: Request):
    try:
        raw_body = await r.body()
        decoded_body = raw_body.decode("utf-8")
        parsed_data = parse_qs(decoded_body)
        data = ServerData.from_payload(parsed_data)


        if data.message_text:
            await buffer_manager.add_to_buffer(data.chat_id, data.message_text)
        if data.formatted_attachment:
                await buffer_manager.add_to_buffer(data.chat_id, data.formatted_attachment)

        results = await lead_manager.stage_info(data.lead_id)

        if results == Config.UNSORTED:
            if data.chat_id not in buffer_manager.user_timers or buffer_manager.user_timers[data.chat_id].done():
                buffer_manager.user_timers[data.chat_id] = asyncio.create_task(
                    buffer_manager.process_target_audience(data.chat_id, data.lead_id, data.talk_id, data.current_time , results)
                )

        if results == Config.AI_WORKS:

            check_result = await buffer_manager.check_and_return(data.talk_id, data.current_time, data.lead_id)
            if check_result:
                return check_result

            if data.chat_id not in buffer_manager.user_timers or buffer_manager.user_timers[data.chat_id].done():
                buffer_manager.user_timers[data.chat_id] = asyncio.create_task(
                    buffer_manager.start_processing(data.chat_id, data.lead_id)
                )
            await buffer_manager.db.add(data.talk_id, data.current_time)
            return {"status": "success", "data": {"entity_id": data.lead_id}}

    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2020)
