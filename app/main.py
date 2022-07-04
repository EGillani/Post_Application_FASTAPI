from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth,vote
#will create our models (this will create the posts table automatically)
models.Base.metadata.create_all(bind=engine)

#fastapi instance
app = FastAPI()

#router object - split our path operations cleaner into files 
#include all the routes in the file we indicated
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#path operation
@app.get("/") 
def root(): 
    return {"message": "Hello World"} 

