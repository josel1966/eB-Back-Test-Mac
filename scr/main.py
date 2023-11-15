from fastapi import FastAPI
from .routes.routesApi import appApi

app = FastAPI(title="eB Backen Test")
app.include_router(appApi)
