
# main.py
import asyncio
import random
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ====================== ДАННЫЕ ======================
SPY_LOCATIONS = [
    "Каток в Коломне", "Thialf Херенвен", "Utah Olympic Oval", "Адлер-Арена",
    "Калгари Olympic Oval", "Инцел", "Коллальбо", "Призовой подиум",
    "Комната заточки коньков", "Старт на 500 м", "Заливочная машина"
]

RUSSIAN_SKATERS = [
    "Павел Кулижников — 6-кратный чемпион мира на 500 м",
    "Руслан Мурашов — чемпион мира 2021 на 500 м",
    "Виктор Муштаков — один из лидеров российского спринта",
    "Ольга Фаткулина — серебро ОИ-2014 на 500 м",
    "Дарья Качанова — чемпионка Европы 2024",
    "Даниил Алдошкин — бронза ОИ-2022 в командной гонке",
    "Артём Арефьев — молодой спринтер",
    "Тимур Карамов — спринтер сборной",
    "Сергей Трофимов — стайер",
    "Иван Фруктов — перспективный юниор",
    "Даниил Найденышев — участник юниорских ЧМ",
    "Румпель — наш тигр",
]

FOREIGN_SKATERS = [
    "Nils van der Poel (Швеция) — двукратный олимпийский чемпион 2022",
    "Patrick Roest (Нидерланды) — многократный чемпион мира на длинных дистанциях",
    "Jutta Monica Leerdam (Нидерланды) — чемпионка мира 2023 на 1000 м",
    "Sven Kramer (Нидерланды) — 9-кратный чемпион мира на 5000 м",
    "Femke Kok (Нидерланды) — сенсация спринта 2024–2025",
    "Jenning de Boo (Нидерланды) — новый король спринта 2025",
    "Jordan Stolz (США) — 19-летний трёхкратный чемпион мира",
    "Kjeld Nuis (Нидерланды) — рекордсмен мира на 1500 м",
]

RECORDS = [
    "500 м мужчины → 33.61 Павел Кулижников",
    "1000 м мужчины → 1:05.69 Павел Кулижников",
    "1500 м мужчины → 1:40.17 Kjeld Nuis",
    "500 м женщины → 36.36 Ли Сан Хва",
    "1000 м женщины → 1:11.61 Бриттани Боу",
    "1500 м женщины → 1:49.83 Михо Такаги",
]

VENUES = [
    "Thialf Херенвен — мекка конькобежного спорта",
    "Utah Olympic Oval — самый быстрый лёд в мире",
    "Медео — 169 мировых рекордов",
    "Коломна — главный российский овал",
]

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Шпион: Конькобежцы", callback_data="spy")],
        [InlineKeyboardButton("Русские конькобежцы", callback_data="rus")],
        [InlineKeyboardButton("Иностранные конькобежцы", callback_data="foreign")],
        [InlineKeyboardButton("Рекорды и катки", callback_data="records")],
    ])

# ====================== ХЕНДЛЕРЫ ======================
@dp.message(CommandStart())
async def start(m: types.Message):
    await m.answer("⛸ <b>Конькобежец Бот 2025</b>\n\nВыбирай раздел:", reply_markup=main_menu())

@dp.callback_query(F.data == "menu")
async def menu(c: types.CallbackQuery):
    await c.message.edit_text("Выбирай раздел:", reply_markup=main_menu())

@dp.callback_query(F.data == "spy")
async def spy(c: types.CallbackQuery):
    loc = random.choice(SPY_LOCATIONS)
    is_spy = random.choice([True, False])
    text = "<b>ТЫ — ШПИОН! Выведай локацию!</b>" if is_spy else f"<b>Твоя локация:</b>\n<code>{loc}</code>"
    await c.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton("Назад", callback_data="menu")]]))

@dp.callback_query(F.data == "rus")
async def rus(c: types.CallbackQuery):
    await c.message.edit_text(f"<b>Русский конькобежец:</b>\n\n{random.choice(RUSSIAN_SKATERS)}",
                              reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                  [InlineKeyboardButton("Ещё русский!", callback_data="rus")],
                                  [InlineKeyboardButton("Назад", callback_data="menu")]
                              ]))

@dp.callback_query(F.data == "foreign")
async def foreign(c: types.CallbackQuery):
    await c.message.edit_text(f"<b>Иностранный конькобежец:</b>\n\n{random.choice(FOREIGN_SKATERS)}",
                              reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                  [InlineKeyboardButton("Ещё иностранец!", callback_data="foreign")],
                                  [InlineKeyboardButton("Назад", callback_data="menu")]
                              ]))

@dp.callback_query(F.data == "records")
async def records(c: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Мировые рекорды", callback_data="wr")],
        [InlineKeyboardButton("Легендарные катки", callback_data="venues")],
        [InlineKeyboardButton("Назад", callback_data="menu")],
    ])
    await c.message.edit_text("Рекорды и катки ↓", reply_markup=kb)

@dp.callback_query(F.data == "wr")
async def wr(c: types.CallbackQuery):
    text = "<b>Мировые рекорды (ноябрь 2025)</b>\n\n" + "\n".join(f"• {r}" for r in RECORDS)
    await c.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton("Назад", callback_data="records")]]))

@dp.callback_query(F.data == "venues")
async def venues(c: types.CallbackQuery):
    await c.message.edit_text(f"<b>Легендарный каток:</b>\n\n{random.choice(VENUES)}",
                              reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                  [InlineKeyboardButton("Ещё каток!", callback_data="venues")],
                                  [InlineKeyboardButton("Назад", callback_data="records")]
                              ]))

# ====================== ЗАПУСК ======================
async def main():
    print("Бот запущен и готов!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
