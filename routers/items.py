# Creates an item router to handle item related API endpoints.
# Accepts and validates item data using the ItemReq model.
# Used Depends to inject application configuration into the endpoint.
# Returns an item response using ItemResponse model.

from fastapi import APIRouter, Depends
from config import appconfig, get_appconf
from models import ItemReq,ItemResponse

routers= APIRouter(prefix="/items", tags=["items"])

@routers.post("/",response_model=ItemResponse)
async def createitem(item: ItemReq, conf: appconfig=Depends(get_appconf),):
    return ItemResponse(message=f"{item.name} is added to {conf.name}")
