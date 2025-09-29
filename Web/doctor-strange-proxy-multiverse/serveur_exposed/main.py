# https://stackoverflow.com/a/71839736
from random import Random
from fastapi import APIRouter, Body, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import json

app = FastAPI(
    docs_url=None, # Disable docs (Swagger UI)
    redoc_url=None, # Disable redoc
    openapi_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

multirouter = APIRouter(prefix="/multiverse")
unirouter = APIRouter(prefix="/ckbjyluhiu")
ids = ["gc7aar1Lt74hfn939nn82nakk==","gc7aa8r47fja9834hidornakk==","gc7aa08idorh82hnianknakk==","gc7aalllp93jnh8192idornakk==",
       "gc7aam93hfhjsldi87083hnakk==", "gc7aaidorndi2ncdhjsnsnakk==","gc7aa0loidorpiojhh7ik8nakk==", "gc7aagidor90fchj52nu9fnakk==",
        "gc7aannnnnnidornnnnnnnakk==", "gc7aatesete892aaa0000nakk==", "gc7aac8492n721kf9skdddnakk==", "gc7aagc6gc3idoridor83hnnakk=="]
horoscope = [
    "Aries", 
    "Taurus", 
    "Gemini", 
    "Cancer", 
    "Leo", 
    "Virgo", 
    "Libra", 
    "Scorpio", 
    "Sagittarius", 
    "Capricorn", 
    "Aquarius", 
    "Pisces"
]
@unirouter.get("/xeheisefu")
def read_horoscope(yt: str = ids[0]):
    return {"ydjuhdqb_yt": ids[int(yt)], "dqcu": horoscope[int(yt)]}

@unirouter.get("/husyfu")
def read_item_recipe(ydjuhdqb_yt: str = "a"):
    if ydjuhdqb_yt == ids[0]:
        return {"description": "credentials for the next socks proxy : polycyber{found_univers_16_a00032}", "name": "Carpaccio de betteraves | Beet Carpaccio"}
    if ydjuhdqb_yt == ids[1]:
        return {"description": "Miam", "name": "Poulet a l'orange | Orange Chicken"}
    raise HTTPException(status_code=404)

@unirouter.get("/qfyjeaud")
def get_token():
    return Response(status_code=200, content="X-Token: lgcwfsha")

@multirouter.post("/entrance")
async def validate_drawing( request : Request ):
    
    content_type = request.headers.get("content-type", None)
    if content_type != "application/json":
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported media type.")
    
    with open("pixels.json", "r") as f:
        json_content = json.load(f)

        my_string = await request.body()

        if json.loads(my_string) == json_content:
            return FileResponse(f"multiverse_gateway.png")
        else:
            raise HTTPException(
            status_code=401,
            detail=f"Unauthorized")

    raise HTTPException(
            status_code=500,
            detail=f"General Error")

"""
@derek_router_v1.options("/ask")
def derek_options():
    headers = {
        "Allow": "OPTIONS, FLAG",
    }
    return Response(content="Please use a supported HTTP verb", headers=headers)


@janet_router_v1.post("/ask")
async def ask_janet_1(request: Request, body: str = Body(..., media_type="text/plain")):
    content_type = request.headers.get("content-type", None)
    if content_type != "text/plain":
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported media type {content_type}", headers={'Accept':'text/plain'})

    if body.lower().strip() == "flag":
        return FileResponse("flag.jpg")
    raise HTTPException(status_code=404, detail="Janet version one can only find a flag.")
"""
# Now add the router to the app
app.include_router(multirouter)
app.include_router(unirouter)