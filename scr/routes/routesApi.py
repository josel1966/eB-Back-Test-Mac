from datetime import datetime
import json
#import enum, jsonify
from lib2to3.pytree import Base
from operator import and_, or_
from typing import List
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from ..config.Conexion import SessionLocal, engine, session
from ..models import customerModels
from ..models.customerModels import CustomerModel
from ..models.workOrderModels import WorkOrderModel
from ..schemas.customerSchemas import CustomerSchema
from ..schemas.workOrderSchemas import WorkOrderSchema, Answer

appApi = APIRouter()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

customerModels.Base.metadata.create_all(engine)
#customerModels.Base.metadata.create_all(engine_from_config)

@appApi.get("/")
def main():
    return RedirectResponse(url="/docs/")

#-----------------------------------------------------------------------------------------------

@appApi.get('/customer/{id}',response_model=List[CustomerSchema])
def show_active_customers(id:str, db:Session=Depends(get_db)):
    customer = db.query(CustomerModel).filter_by(id=id)

    return customer

@appApi.get('/customers/',response_model=List[CustomerSchema])
def show_customers(db:Session=Depends(get_db)):
    customers = db.query(CustomerModel).all()

    return customers

@appApi.post('/create-customers/',response_model=CustomerSchema)
def create_customers(data_entry:CustomerSchema,db:Session=Depends(get_db)):
    customer = CustomerModel(first_name = data_entry.first_name,
                                            last_name=data_entry.last_name,
                                            address=data_entry.address)
                                            # start_date=data_entry.start_date,
                                            # end_date=data_entry.end_date, 
                                            # is_active=data_entry.is_active, 
                                            # create_at=data_entry.create_at) 
    db.add(customer)
    db.commit()

    db.refresh(customer)
    return customer

@appApi.put('/update-customers/{id}',response_model=CustomerSchema)
def update_customers(id:str,data_entry:CustomerSchema,db:Session=Depends(get_db)):
    customer = db.query(CustomerModel).filter_by(id=id).first()
    customer.first_name = data_entry.first_name
    customer.last_name=data_entry.last_name
    customer.address=data_entry.address
    customer.start_date=data_entry.start_date
    customer.end_date=data_entry.end_date
    customer.is_active=data_entry.is_active
    customer.create_at=data_entry.create_at

    db.commit()
    db.refresh(customer)
    
    return customer

@appApi.delete('/delete-customer/{id}',response_model=Answer)
def delete_customers(id:str,db:Session=Depends(get_db)):
    customer = db.query(CustomerModel).filter_by(id=id).first()
    db.delete(customer)
    db.commit()

    answer = Answer(mensaje="Cliente eliminado")
    return answer

@appApi.get('/active-customers/{isActiveT}/{isActiveF}',response_model=List[CustomerSchema])
def show_active_customers(isAT:bool, isAF:str, db:Session=Depends(get_db)):
    customers = db.query(CustomerModel).filter_by(is_active=isAT, address=isAF).all()

    return customers

#-----------------------------------------------------------------------------------------------
@appApi.get('/work-orders/',response_model=List[WorkOrderSchema])
def show_work_orders(db:Session=Depends(get_db)):
    workOrders = db.query(WorkOrderModel).all()
    
    return workOrders

@appApi.post('/create-work-orders/',response_model=WorkOrderSchema)
def create_work_orders(data_entry:WorkOrderSchema,db:Session=Depends(get_db)):
    workOrders = WorkOrderModel(customer_id = data_entry.customer_id,
                                title=data_entry.title)
                                # planned_date_begin=data_entry.planned_date_begin,
                                # planned_date_end=data_entry.planned_date_end, 
                                # status=data_entry.status, 
                                # create_at=data_entry.create_at) 
    
    db.add(workOrders)
    db.commit()
    db.refresh(workOrders)

    updateCustomerWokrOrder(data_entry.customer_id)

    return workOrders

@appApi.put('/update-work-orders/{id}',response_model=WorkOrderSchema)
def update_work_orders(id:str,data_entry:WorkOrderSchema,db:Session=Depends(get_db)):
    workOrders = db.query(WorkOrderModel).filter_by(id=id).first()
    workOrders.customer_id=data_entry.customer_id
    workOrders.title=data_entry.title
    workOrders.planned_date_begin=data_entry.planned_date_begin
    workOrders.planned_date_end=data_entry.planned_date_end 
    workOrders.status=data_entry.status.name
    workOrders.create_at=data_entry.create_at

    db.commit()
    db.refresh(workOrders)

    return workOrders

@appApi.delete('/delete-work-orders/{id}',response_model=Answer)
def delete_work_orders(id:str,db:Session=Depends(get_db)):
    workOrders = db.query(WorkOrderModel).filter_by(id=id).first()

    db.delete(workOrders)
    db.commit()

    answer = Answer(mensaje="Successfully removed")
    return answer

@appApi.put('/plan-work-order-date/{id}',response_model=WorkOrderSchema)
def planWorkOrderDate(id:str,data_entry:WorkOrderSchema,db:Session=Depends(get_db)):
    workOrders = db.query(WorkOrderModel).filter_by(id=id).first()

    workOrders.planned_date_begin=data_entry.planned_date_begin

    db.commit()
    db.refresh(workOrders)

    # Pendiente por hacer la diferencia entre la fecha planeada de las órdenes, que no sea menor a 2 horas
    
    return workOrders

@appApi.get('/work-orders-date-range/{date-since}/{date-until}',response_model=List[WorkOrderSchema])
def show_work_orders_date_range(datesince:datetime, dateuntil:datetime,
                                db:Session=Depends(get_db)):
    
    plannedDateBeginS=WorkOrderModel.planned_date_begin
    plannedDateBeginU=WorkOrderModel.planned_date_begin

    workOrdersDateRange = db.query(WorkOrderModel).filter(and_(plannedDateBeginS >= datesince,
                                                             plannedDateBeginU <= dateuntil)).all()
    
    return workOrdersDateRange

@appApi.get('/work-orders-status/{status}',response_model=List[WorkOrderSchema])
def show_work_orders_date_range(status:str,db:Session=Depends(get_db)):
    workOrdersDateRange = db.query(WorkOrderModel).filter_by(status=status).all()
    
    return workOrdersDateRange

@appApi.get('/work-orders-customer/{customer_id}',response_model=List[WorkOrderSchema])
def show_work_orders_date_range(customer_id:str,db:Session=Depends(get_db)):
    workOrdersDateRange = db.query(WorkOrderModel).filter_by(customer_id=customer_id).all()
    
    return workOrdersDateRange

@appApi.get('/work-order-customer-data/{work_order_id}',response_model=List[WorkOrderSchema])
def show_work_orders_date_range(work_order_id:str,db:Session=Depends(get_db)):
    workOrder = db.query(WorkOrderModel).filter_by(id=work_order_id)

    if workOrder:
        customer = [{'id': customer.id, 'work_orders': customer.work_order} for customer in workOrder.customers]
        db.close
        return json.decoder({'workorder_id': id, 
                    'first_name': customer.first_name, 
                    'last_name': customer.last_name,
                    'address': customer.address,
                    'start_date': customer.start_date,
                    'end_date': customer.end_date,
                    'is_active': customer.is_active})

def updateCustomerWokrOrder(id: str):
    workOrdersCount = session.query(WorkOrderModel).filter(WorkOrderModel.customer_id==id).count()
    result_count = workOrdersCount
    print(result_count)
    if result_count == 1:
        customer = session.query(CustomerModel).filter(CustomerModel.id==id).first()
        customer.is_active=True
        date_currency = datetime.now()
        customer.start_date = date_currency
        session.commit()
    
