'''Data expecting from client when sending a request.
   Response api sends back after processing a request.
   Request from item related work.
   Response returned after processing item request.'''

from pydantic import BaseModel
from typing import Optional

class UserReq(BaseModel):
    name: str = "user"
    age: Optional[str] = "Not added"

class UserResponse(BaseModel):
    message: str="This is  User response message in Models."

class ItemReq(BaseModel):
    name: str='item1'
    price: float= 100.0

class ItemResponse(BaseModel):
    message: str ='This is item response message in Models.'