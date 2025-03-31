# https://stackoverflow.com/a/71839736
from random import Random
from fastapi import APIRouter, Body, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

BASE_CACTUS_PREFIX = "cactus"

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

janet_router_v2 = APIRouter(prefix="/janet/v2")
janet_router_v1 = APIRouter(prefix="/janet/v1")
derek_router_v1 = APIRouter(prefix="/derek/v1")


@janet_router_v2.post("/ask")
def ask_janet_2( request : Request ):
    content_type = request.headers.get("content-type", None)
    if content_type != "multipart/form-data":
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported media type {content_type}")
    rnd = Random()
    choice = rnd.choice([1,2,3])
    return FileResponse(f"{BASE_CACTUS_PREFIX}{choice}.jpg")


@derek_router_v1.options("/ask")
def derek_options():
    headers = {
        "Allow": "OPTIONS, FLAG",
    }
    return Response(content="Please use a supported HTTP verb", headers=headers)


@derek_router_v1.api_route("/ask", methods=["FLAG"])
def ask_derek_1():
    return FileResponse("derek.jpg")

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

# Now add the router to the app
app.include_router(janet_router_v1)
app.include_router(janet_router_v2)
app.include_router(derek_router_v1)