from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, HTTPException

from middleware import sns_message_parse
from models import HelloMessage, ScheduledMessage, SNSMessage
from utils import create_scheduled_event, publish_message

app = FastAPI()


@app.post("/say-hello")
async def say_hello(message: HelloMessage) -> dict[str, str]:
    publish_message(message.message, message.subject)
    return {"message": "Message sent"}


@app.post("/hello")
@sns_message_parse
async def hello(_: SNSMessage) -> dict[str, Any]:
    return {"message": "Hello world"}


@app.post("/schedule-message")
async def schedule_message(scheduled_message: ScheduledMessage) -> dict[str, str]:
    now = datetime.now(timezone.utc)
    if scheduled_message.schedule_time <= now:
        raise HTTPException(
            status_code=400, detail="Scheduled date must be in the future."
        )
    return create_scheduled_event(
        scheduled_message.schedule_time, scheduled_message.message
    )


@app.post("/receive-scheduled-message")
@sns_message_parse
async def receive_schedule_message(_: SNSMessage) -> dict[str, Any]:
    return {"message": "Message scheduled received!"}
