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

description = """
_RESTful API to keep track of your posts!_ 🚀

## First-Time Users
* You can **create** a brand new account with _/users_.

## Authentication 
* On FastAPI docs select the green **`Authorize`** button to **login** and unlock all endpoints.
* For custom use (ex. Postman), use _/token_ with your account details to retrieve a oauth2.0 **bearer token**.
"""

tags_metadata = [
    {
        "name": "Users",
        "description": "You can create a new user and obtain user details by id (**Authentication** required)."
    },
    {
        "name": "Posts",
        "description": "CRUD Operations with posts. **Authentication** required for all endpoints except Get Posts.",
    },
    {
        "name": "Vote",
        "description": "Vote on your favorite posts. _dir_ of 1 means upvoting a post, 0 means downvoting. **Authentication** required.",
    },
    {
        "name": "Authentication",
        "description": "Login with your account credentials to obtain bearer token (does **not** authenticate endpoints directly on FastAPI docs).",
    }
]

#fastapi instance
app = FastAPI(
    title="Post It",
    description=description,
    version="2.1.0",
    contact={
        # "name": "Eve",
        # "url": "https://www.linkedin.com/in/erajg/",
        "email": "e_gillani@fanshaweonline.com",
    },
    openapi_tags=tags_metadata
)

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
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(vote.router)




#path of lookalike google digital asset file to supress warnings
asset_link_file = './assetlinks.json'

#path operation
@app.get("/", include_in_schema=False) 
def root(): 
    return {"message": "Welcome to my post application", 
            "instructions" : f"""type "/docs" in the url to access the api schema"""} 

@app.get("/.well-known/assetlinks.json", response_class=FileResponse, include_in_schema=False)
def suppress_google_warnings():
    return asset_link_file