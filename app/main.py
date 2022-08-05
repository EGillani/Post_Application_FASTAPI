from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth,vote
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

#this will create our models (this will create the posts table automatically)
#now uncommented since I implemented alembic (handles updates of our table schema and changes which sqlalchemy lacks)
#July 31st - so I discovered that if you are starting from scratch...you need this :( ...tutorial lied 
#models.Base.metadata.create_all(bind=engine)

#fastapi instance
app = FastAPI()

origins = ["*"]
#CORSMiddleware runs before any request 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#router object - split our path operations cleaner into files 
#include all the routes in the file we indicated
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


#path of lookalike google digital asset file to supress warnings
asset_link_file = './assetlinks.json'

#path operation
@app.get("/", include_in_schema=False) 
def root(): 
    return {"message": "Welcome to my post application", 
            "instructions" : 
                [f"""type "/docs" in the url to access the api schema""", 
                 f"""register for an account using "Creater User" """, 
                 f"""login to access the other api endpoints (all endpoints authenticated automatically for session)"""]} 

@app.get("/.well-known/assetlinks.json", response_class=FileResponse, include_in_schema=False)
def suppress_google_warnings():
    return asset_link_file