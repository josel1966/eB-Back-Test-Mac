from enum import Enum
import uuid
from sqlalchemy import create_engine, Column, UUID, String, DateTime, ForeignKey, Enum as EnumField
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from ..config.Conexion import Base

class StatusTypeEnum(Enum):
    NEW = 'NEW'
    DONE = 'DONE'
    CANCELLED = 'CANCELLED'

class WorkOrderModel(Base):
    __tablename__ = 'work_orders'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey('customers.id'), nullable=False)
    title = Column(String(100), nullable=False)
    planned_date_begin = Column(DateTime, default=None, nullable=True)
    planned_date_end = Column(DateTime, default=None, nullable=True)
    status = Column(EnumField(StatusTypeEnum), default=StatusTypeEnum.NEW, nullable=False)
    create_at = Column(DateTime, default=datetime.now(), nullable=False)

    customer = relationship('CustomerModel', back_populates='workOrders')

