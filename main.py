
# speed_skating_bot_final.py
import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage

BOT_TOKEN = "8195091477:AAEg2KaCHZsBaFfLHTedOp2NFycU6z_4nEw"

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ====================== ЛОКАЦИИ ДЛЯ ШПИОНА ======================
SPY_LOCATIONS = [
    "Каток в Коломне", "Thialf Херенвен", "Utah Olympic Oval", "Адлер-Арена",
    "Калгари Olympic Oval", "Инцел", "Коллальбо",
    "Призовой подиум", "Комната заточки коньков", "Старт на 500м"
]

# ====================== РУССКИЕ КОНЬКОБЕЖЦЫ ======================
RUSSIAN_SKATERS = [
    {"name": "Павел Кулижников",      "fact": "6-кратный чемпион мира на 500 м"},
    {"name": "Руслан Мурашов",        "fact": "Чемпион мира 2021 на 500 м"},
    {"name": "Виктор Муштаков",       "fact": "Один из лидеров спринта"},
    {"name": "Ольга Фаткулина",       "fact": "Серебро ОИ-2014 на 500 м"},
    {"name": "Дарья Качанова",        "fact": "Чемпионка Европы 2024"},
    {"name": "Даниил Алдошкин",       "fact": "Бронза ОИ-2022 в команде"},
    {"name": "Артем Арефьев",         "fact": "Юниорский рекордсмен"},
    {"name": "Тимур Карамов",         "fact": "Спринтер сборной РФ"},
    {"name": "Сергей Трофимов",       "fact": "Стайер сборной РФ"},
    {"name": "Иван Фруктов",          "fact": "Точно не спринтер"},
    {"name": "Даниил Найденышев",     "fact": "Участник ЧМ 2026"},
    {"name": "Румпель",               "fact": "Наш тигр"},
]

# ====================== ИНОСТРАННЫЕ КОНЬКОБЕЖЦЫ ======================
FOREIGN_SKATERS = [
    {"name": "Nils van der Poel",     "country": "Швеция",    "fact": "Двукратный олимпийский чемпион 2022"},
    {"name": "Patrick Roest",         "country": "Нидерланды","fact": "Многократный чемпион мира на длинных дистанциях"},
    {"name": "Jutta Monica Leerdam",  "country": "Нидерланды","fact": "Чемпионка мира 2023 на 1000 м"},
    {"name": "Sven Kramer",           "country": "Нидерланды","fact": "9-кратный чемпион мира на 5000 м"},
    {"name": "Femke Kok",             "country": "Нидерланды","fact": "Сенсация спринта 2023–2025"},
    {"name": "Jenning de Boo",        "country": "Нидерланды","fact": "Новый король спринта 2025"},
    {"name": "Jordan Stolz",          "country": "США",       "fact": "19-летний трёхкратный чемпион мира 2023"},
    {"name": "Kjeld Nuis",            "country": "Нидерланды","fact": "Действующий рекордсмен мира 1500 м"},
]

# ====================== РЕКОРДЫ И КАТКИ ======================
RECORDS = [
    "500 м мужчины — 33.61 Павел Кулижников",
    "1000 м мужчины — 1:05.69 Павел Кулижников",
    "1500 м мужчины — 1:40.17 Kjeld Nuis",
    "500 м женщины — 36.36 Ли Сан Хва",
    "1000 м женщины — 1:11.61 Бриттани Боу",
    "1500 м женщины — 1:49.83 Михо Такаги",
]

VENUES = [
    {"name": "Thialf Херенвен",      "desc": "Мекка конькобежного спорта"},
    {"name": "Utah Olympic Oval",    "desc": "Самый быстрый лёд мира"},
    {"name": "Медео",                "desc": "169 мировых рекордов"},
    {"name": "Коломна",              "desc": "Главный российский овал"},
]

# ====================== МЕНЮ ======================
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Шпион: Конькобежцы", callback_data="spy")],
        [InlineKeyboardButton(text="Русские конькобежцы", callback_data="rus")],
        [InlineKeyboardButton(text="Иностранные конкьобежцы", callback_data="foreign")],
        [InlineKeyboardButton(text="Рекорды и катки", callback_data="records")],
    ])

# ====================== ХЕНДЛЕРЫ ======================
@dp.message(CommandStart())
async def start(m: types.Message):
    await m.answer("<b>⛸ Конькобежец Бот 2025</b>\n\nВыбирай раздел:", reply_markup=main_menu())

@dp.callback_query(F.data == "menu")
async def menu(c: types.CallbackQuery):
    await c.message.edit_text("Выбирай раздел:", reply_markup=main_menu())

@dp.callback_query(F.data == "spy")
async def spy(c: types.CallbackQuery):
    loc = random.choice(SPY_LOCATIONS)
    spy = random.choice([True, False])
    text = "<b>ТЫ - ШПИОН! 🕵️‍" if spy else f"<b>Локация:</b>\n<code>{loc}</code>"
    await c.message.edit_text(text + "\n\n<i>Играйте в группе через /new</i>", 
                              reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton("Назад", callback_data="menu")]]))

@dp.callback_query(F.data == "rus")
async def rus(c: types.CallbackQuery):
    s = random.choice(RUSSIAN_SKATERS)
    await c.message.delete()
    await bot.send_photo(c.message.chat.id, s["photo"],
                         caption=f"<b>{s['name']}</b>\n\n{s['fact']}",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [InlineKeyboardButton("Ещё русский!", callback_data="rus")],
                             [InlineKeyboardButton("Назад", callback_data="menu")]
                         ]))

@dp.callback_query(F.data == "foreign")
async def foreign(c: types.CallbackQuery):
    s = random.choice(FOREIGN_SKATERS)
    await c.message.delete()
    await bot.send_photo(c.message.chat.id, s["photo"],
                         caption=f"<b>{s['name']}</b> ({s['country']})\n\n{s['fact']}",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [InlineKeyboardButton("Ещё иностранец!", callback_data="foreign")],
                             [InlineKeyboardButton("Назад", callback_data="menu")]
                         ]))

@dp.callback_query(F.data == "records")
async def rec_menu(c: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Мировые рекорды", callback_data="wr")],
        [InlineKeyboardButton("Легендарные катки", callback_data="venues")],
        [InlineKeyboardButton("Назад", callback_data="menu")],
    ])
    await c.message.edit_text("Рекорды и катки ⬇️", reply_markup=kb)

@dp.callback_query(F.data == "wr")
async def wr(c: types.CallbackQuery):
    text = "<b>Мировые рекорды (ноябрь 2025)</b>\n\n" + "\n".join(f"• {r}" for r in RECORDS)
    await c.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton("Назад", callback_data="records")]]))

@dp.callback_query(F.data == "venues")
async def venues(c: types.CallbackQuery):
    v = random.choice(VENUES)
    await c.message.delete()
    await bot.send_photo(c.message.chat.id, v["photo"],
                         caption=f"<b>{v['name']}</b>\n\n{v['desc']}",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                             [InlineKeyboardButton("Ещё каток!", callback_data="venues")],
                             [InlineKeyboardButton("Назад", callback_data="records")]
                         ]))

# ====================== ЗАПУСК ======================
async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
