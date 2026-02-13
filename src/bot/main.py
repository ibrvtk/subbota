from aiogram import Dispatcher
from aiogram.exceptions import TelegramBadRequest

from asyncio import run

from config import BOT
from app.handlers import RT as handlers_router

DP = Dispatcher()


async def main() -> None:
    DP.include_router(handlers_router)
    await BOT.delete_webhook(True)
    print("Телеграм бот запущен")
    await DP.start_polling(BOT, allowed_updates=DP.resolve_used_update_types())

if __name__ == "__main__":
    try:
        run(main())
    
    except KeyboardInterrupt:
        pass
    except TelegramBadRequest as e:
        print(f"ошибка - TelegramBadRequest: main.py: {e}")
    except Exception as e:
        print(f"ошибка: main.py: {e}")
