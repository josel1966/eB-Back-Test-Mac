import datetime, uuid
import enum
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class WorkOrderSchema(BaseModel):
    id: Optional[uuid.UUID]
    customer_id: uuid.UUID
    title: str
    planned_date_begin: Optional[datetime.datetime]
    planned_date_end: Optional[datetime.datetime]
    status: Optional[str]
    #status: Enum
    create_at: datetime.datetime

    class Config:
        from_attributes = True

class Answer(BaseModel):   
    mensaje:str
   