"""Imports BaseModel from Pydantic.BaseModel is used to create models that store data and validate it automatically.
   conf creates an instance/object of the appconfig/class model.when no values are passed, Pydantic uses all the default values."""
from pydantic import BaseModel
from typing import Optional

class appconfig(BaseModel):
    name: str ='Demo'
    version: str = '1.0'
    description: Optional[str] = "Description of Demo."

conf=appconfig( name= 'Test API', version='1.1', description='This is test api')
async def get_appconf():
    print(conf)
    return conf
