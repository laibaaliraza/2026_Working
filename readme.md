#FastAPI demo project.
#17_July_2026
A simple FastAPI project demostrating how to build rest api's using routers , pydantic models, dependency injection and application configuration.


#Pre req.
Python 
FastAPI
uvicorn 
pydantic

#Install dependencies
pip install fastapi[all]

start fastapi server
uvicorn main:app --reload

application run at 
http://127.0.0.1:8000

FastAPI documentation
fast api automatically provide doc
http://127.0.0.1:8000/doc
http://127.0.0.1:8000/redoc

#Configuration
fast api demo gives a configuration to give details

class appconfig(BaseModel):
    name: str ='Demo'
    version: str = '1.0'
    description: Optional[str] = "Description of Demo."

this config is injected into endpoints using fastapi injection(Depends)
Depends(get_appconf)

#Endpoints
root endpoint
GET "/"
returns welcome message

users endpoint 
POST "/users/"
create new user
class UserReq(BaseModel):
    name: str = "user"
    age: Optional[str] = "Not added"

items endpoint
POST "/items/"
create new item
class ItemReq(BaseModel):
    name: str='item1'
    price: float= 100.0


#Features
-Fast api application setup
-API routing using APIRouter
-Request and Response velidation using pydantic model
-Dependency injection using Depends
-Centralized application configuration
-seperate routers for users and items
-Automatic documentation using swagger doc<http://127.0.0.1:8000/docs> and redoc<http://127.0.0.1:8000/redoc>

#FastAPI service demo structure
FastAPI_demo_service
|-__init__.py        #python package
|-main.py            #main application
|-config.py          #Centralized configuration
|-models.py          #pydantic request and response models
|-routers
     |-users.py          #users related api endpoint
     |-items.py          #items related api endpoint
|-readme.md 

