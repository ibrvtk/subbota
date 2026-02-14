from aiogram import Dispatcher, Bot, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties

from os import getenv
from dotenv import load_dotenv; load_dotenv()
from asyncio import new_event_loop, set_event_loop

import database as db

TOKEN=getenv('BOT_TOKEN')
BOT = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
DP = Dispatcher()


# КЛАВИАТУРЫ
def kb_choose_player(session_id: str) -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardBuilder()

    inline_keyboard.add(InlineKeyboardButton(
        text="Игрок 1 (СЛЕВА)",
        callback_data=f"role_1_{session_id}"
    ))
    inline_keyboard.add(InlineKeyboardButton(
        text="Игрок 2 (СПРАВА)",
        callback_data=f"role_2_{session_id}"
    ))

    return inline_keyboard.adjust(2).as_markup()

def kb_area_action(session_id: str, player_priority: int, is_attacker: bool) -> InlineKeyboardMarkup:
    action = "⚔️ Атаковать" if is_attacker else "🛡️ Защитить"

    inline_keyboard = InlineKeyboardBuilder()

    for area in ["ГОЛОВА", "КОРПУС", "НОГИ"]:
        inline_keyboard.add(InlineKeyboardButton(
            text=f"{action}: {area}",
            callback_data=f"act_{player_priority}_{session_id}_{area}"
        ))

    return inline_keyboard.adjust(1).as_markup()


# ХЭНДЛЕРЫ И КОЛЛБЭКИ
@DP.message(Command('start', ignore_case=True))
async def cmd_start(message: Message, command: CommandObject) -> None:
    args = command.args

    if not args or len(args) != 1:
        return await message.answer("⚠️ <b>Введите код из игры.</b>\nПример: <code>/start 123456</code>")

    session_id = args[0]

    await message.answer(
        text=f"🕹️ <b>Сессия <code>{session_id}</code> найдена.</b> Кто Вы?",
        reply_markup=kb_choose_player(session_id)
    )

@DP.callback_query(F.data.startswith('role_'))
async def cb_role(callback: CallbackQuery) -> None:
    cb_data = callback.data.split('_')
    player_priority = int(cb_data[1])
    session_id = cb_data[2]

    db_data = db.get_session_data(session_id)

    if not db_data:
        return await callback.answer("🤷‍♂️ Сессия не найдена в БД")

    is_attacker = (player_priority == '1' and db_data['attacker_side'] == 1) or (player_priority == '2' and db_data['attacker_side'] == 2)

    await callback.message.edit_text(
        text="*️⃣ <b>Выберите действие.</b>",
        reply_markup=kb_area_action(session_id, player_priority, is_attacker)
    )

@DP.callback_query(F.data.startswith('act_'))
async def cb_action(callback: CallbackQuery):
    data = callback.data.split('_')
    player_priority = int(data[1])
    session_id = data[2]
    area = data[3]

    if db.set_choice(session_id, player_priority, area):
        await callback.message.edit_text("✅ <b>Действие отправлено.</b>\n<blockquote></blockquote>")
    else:
        await callback.answer("❌ Выбор уже сделан")


def main():
    loop = new_event_loop()
    set_event_loop(loop)
    loop.run_until_complete(DP.start_polling(BOT, handle_signals=False)) # handle_signals=False обязателен для Mac/Linux в потоке