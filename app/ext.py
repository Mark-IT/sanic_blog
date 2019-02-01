from sanic_auth import Auth
from sanic_session import Session
from tortoise import Tortoise

from config import DB_URL


async def db_setup(_create_db=False):
    await Tortoise.init(
        db_url=DB_URL,
        modules={'models': ['app.models']},
    )


auth = Auth()
session = Session()

