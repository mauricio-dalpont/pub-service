from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SNSMessage(BaseModel):
    Type: str
    MessageId: str
    TopicArn: str
    Message: str
    Timestamp: str
    SignatureVersion: str
    Signature: str
    SigningCertURL: str
    UnsubscribeURL: Optional[str] = None
    SubscribeURL: Optional[str] = None  # Only included in SubscriptionConfirmation
    Subject: Optional[str] = None  # Optional field for the subject of the message

    class Config:
        extra = "ignore"


class ScheduledMessage(BaseModel):
    schedule_time: datetime
    message: str


class HelloMessage(BaseModel):
    message: str
    subject: Optional[str] = None
