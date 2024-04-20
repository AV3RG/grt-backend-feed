from datetime import datetime

from pydantic import BaseModel


class PushData(BaseModel):
    User_id: str
    Timestamp: datetime
    Event: str
