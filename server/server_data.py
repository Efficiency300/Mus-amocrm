from pydantic import BaseModel
from typing import Optional, Dict, Any

class ServerData(BaseModel):
    message_text: str
    chat_id: str
    talk_id: str
    current_time: int
    lead_id: Optional[str]
    attachment_type: Optional[str] = None
    attachment_link: Optional[str] = None
    formatted_attachment: Dict[str, Optional[str]]

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> "ServerData":
        message_text = payload.get("message[add][0][text]", [""])[0]
        chat_id = payload.get("message[add][0][chat_id]", [""])[0]
        talk_id = payload.get("message[add][0][talk_id]", [""])[0]
        current_time = int(payload.get("message[add][0][created_at]", ["0"])[0])
        lead_id = payload.get("message[add][0][entity_id]", [None])[0]
        attachment_type = payload.get("message[add][0][attachment][type]", [None])[0]
        attachment_link = payload.get("message[add][0][attachment][link]", [None])[0]

        formatted_attachment = {
            "type": attachment_type if attachment_type else "external_link",
            "content": attachment_link if attachment_link else None
        }

        return cls(
            message_text=message_text,
            chat_id=chat_id,
            talk_id=talk_id,
            current_time=current_time,
            lead_id=lead_id,
            formatted_attachment=formatted_attachment,
        )


