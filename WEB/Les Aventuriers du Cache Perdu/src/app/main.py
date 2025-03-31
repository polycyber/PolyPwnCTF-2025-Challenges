from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from bot import Bot
import threading

dr_jones = Bot()
threading.Thread(target=dr_jones.run).start()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def user_page(request: Request, name: str = ""):
    """Affiche la page de l'aventurier."""
    if (name == "DrProxy" or name == "Proxy") and request.headers.get(
        "User-Agent"
    ) != dr_jones.flag1:
        dr_jones.urls_to_visit = [name] + dr_jones.urls_to_visit
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "name": name,
        },
    )


@app.get("/journal", response_class=HTMLResponse)
async def journal_page(request: Request, OTP: str = ""):
    """Affiche le journal du Dr Proxy Jones."""
    authorized = request.query_params.get("OTP") == dr_jones.OTP
    return templates.TemplateResponse(
        "journal.html",
        {
            "request": request,
            "authorized": authorized,
            "flag": dr_jones.flag3,
        },
    )


@app.get("/api/clues", response_class=JSONResponse)
async def get_clues():
    """Retourne la liste des films avec le nombre de votes."""
    return [
        "Les étoiles guident vers l’artefact caché.",
        "Une clé en pierre contient un message secret.",
        "La jungle abrite une énigme oubliée.",
    ]
