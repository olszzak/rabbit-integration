from fastapi import FastAPI, APIRouter

from ping.view import router as ping_router
from messages.view import router as message_router
from settings import get_settings

settings = get_settings()


def setup_routing(app: FastAPI):
    global_router = APIRouter()
    global_router.include_router(ping_router)
    global_router.include_router(message_router)
    app.include_router(global_router)


def create_app() -> FastAPI:
    app = FastAPI(debug=True)
    setup_routing(app)

    return app
