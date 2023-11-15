import datetime, uuid
from typing import Optional
from pydantic import BaseModel

class CustomerSchema(BaseModel):
    id: Optional[uuid.UUID]
    first_name: str
    last_name: str
    address: str
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    is_active: Optional[bool]
    create_at: datetime.datetime

    class Config:
        from_attributes = True

class Answer(BaseModel):   
    mensaje:str
   


   