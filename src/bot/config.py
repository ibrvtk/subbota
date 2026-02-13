from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from os import getenv
from dotenv import load_dotenv; load_dotenv('.env')


TOKEN=getenv('BOT_TOKEN')
BOT = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode='HTML')
)

DATABASE_DB=getenv('DATABASE_DB')
DATABASE_SQL=getenv('DATABASE_SQL')