import uuid
from sqlalchemy import Column, UUID, String, DateTime, Boolean, create_engine
from sqlalchemy.orm import relationship
from datetime import datetime
from ..config.Conexion import Base

class CustomerModel(Base):
    __tablename__ = 'customers'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    start_date = Column(DateTime, default=None, nullable=True)
    end_date = Column(DateTime, default=None, nullable=True)
    is_active = Column(Boolean, default=False, nullable=False)
    create_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    workOrders = relationship('WorkOrderModel', back_populates='customer')

