from fastapi.responses import JSONResponse
from fastapi import FastAPI, status, HTTPException

from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

class Post(BaseModel):
    title:str
    working: str
    ranking: bool = True
    rating: Optional[int]=None

my_posts=[{"title":"post1","working":"working of post1","id":1},{"title":"post2","working":"working of post2","id":2}]

def find_posts(id):
    for p in my_posts:
        if p['id']==id:
            return p

def find_index_posts(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i


app=FastAPI()
@app.get("/")
async def root():
    return("Hello",
           "I am Laiba.")

@app.get("/posts")
async def posts():
    return{
        "i am in get posts."
    }

@app.get("/myposts")
async def myposts():
    return{"data":my_posts}

@app.get("/posts/latest")#we wrote this above /posts/id cause when we try /post/latest after id it gives an error cause it maps /posts/anyvariable and think of /{id} as latest
async def getlatest_post():
    post=len(my_posts)-1
    return post

@app.get("/posts/{id}")
async def getposts_id(id: int):
    post=find_posts(int(id))
    return{"post details":post}

@app.post("/createposts")
async def create_posts():
    return{"message":"successfully created posts"}

@app.post("/createposts2")
def create_posts2(payload: dict = Body(...)):
    print(payload)
    return{"message":"post2 created successfully"}

@app.post("/working")
async def create_posts3(payload2: dict = Body(...)):
    print(payload2)
    return{"newpost":f"title{payload2['title']} content{payload2['working']}"}

@app.post("/gettingposts")
async def getting_posts(new_post: Post):
    print(new_post)
    return{"new_post":"This is in getting post function."}

@app.post("/workingwithmyposts")
def w_myposts(post: Post):
    post_dict=post.dict()
    post_dict['id']=randrange(0,10000)
    my_posts.append(post_dict)
    return{"data": my_posts}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_id(id: int):
    index=find_index_posts(id)
    if index==None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f"detail: post with id={id} does not exists")
    my_posts.pop(index)
    #return(f"post at index {index} deleted successfully!  ")
    return JSONResponse(status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post( id:int,post:Post ):
    index=find_index_posts(id)
    if index==None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f"details: post with id {id} does not exist.")
    
    post_dict=post.dict()
    post_dict['id']=id
    my_posts[index]=post_dict

    print(post)
    return {"data of updated post": post_dict}