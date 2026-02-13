from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

RT = Router(name='handlers')


@RT.message(Command('start', ignore_case=True))
async def cmd_start(message: Message) -> None:
    await message.answer("Hello, World!")