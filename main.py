
from fastapi import FastAPI,status
#import models
#from database import engine
from routers import posts, users,auth,like
from fastapi.middleware.cors import CORSMiddleware


#models.Base.metadata.create_all(bind=engine)

app=FastAPI()

origins=[]
#if you have a webapp you can allow it to talk with your API and send request

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(like.router)

@app.get("/home", status_code=status.HTTP_200_OK)
def home():
    return "Donya,if I could keep looking at your eyes for rest of my life,I would be the happiest person in the world!!!"

@app.get("/home/{id}",status_code=status.HTTP_200_OK)
async def get_info(id,skip:int=0,limit:int=10,published:bool=True):
    return {f"the id is {id} and published code is{published}":f"the limit is {limit} and skip is {skip}"}



