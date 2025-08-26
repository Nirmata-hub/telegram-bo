import logging
import random
import datetime
import asyncio
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# 🔑 Данные
TOKEN = "8134220896:AAE6WjqS_JBw3Xo_tL05hd_LIS2IBkDIwqE"   # вставь сюда свой токен
CHAT_ID = 123456789    # твой chat_id

logging.basicConfig(level=logging.INFO)

# --- Сообщения ---
love_compliments = [
    "Ты самая прекрасная на свете ❤️",
    "Моя любовь к тебе безгранична 💕",
    "Ты — моя вселенная 🌌",
    "Ты делаешь меня счастливым каждый день 😘",
    "Ты — чудо из чудес ✨",
    "Ты моя мечта и реальность одновременно 💖"
]

tender_compliments = [
    "Ты моё нежное чудо 🌸",
    "Обнять тебя — моё самое большое желание 🤗",
    "Ты мягче облачка и теплее солнца ☀️",
    "Твои глаза — как два океана, в которых я тону 💕",
    "Ты нежность, воплощённая в человеке ✨",
    "С тобой мир становится добрее и светлее 💖",
    "Ты моя самая сладкая радость 🍯",
    "Моя девочка — самая нежная на свете 🌹"
]

morning_messages = [
    "Доброе утро, любовь моя ☀️",
    "Просыпайся, Солнышко 🌸",
    "Пусть твой день будет лёгким и радостным 💕",
    "С добрым утром, моя самая Любимая 😘"
]

night_messages = [
    "Спокойной ночи, моя любовь 🌙",
    "Сладких снов, моя радость 💖",
    "Пусть тебе приснюсь я 😘",
    "Нежных снов, моя Девочка ✨"
]

love_messages = [
    "Люблю тебя всем сердцем малыш ❤️",
    "Ты моя единственная 💕",
    "Ты моё счастье 🌸",
    "С тобой моя жизнь имеет смысл 😘"
]

miss_messages = [
    "Я так скучаю по тебе, любовь моя 💕",
    "Каждая минута без тебя кажется вечностью ⏳❤️",
    "Хочу скорее к тебе 🤗",
    "Скучаю так сильно, что сердце тоскует 💖",
    "Ты в моих мыслях каждую секунду 😘",
    "Скучаю и жду нашей встречи ✨",
    "Без тебя всё становится пустым… 😔",
    "Моё счастье — быть рядом, а пока очень скучаю 🌹"
]

surprise_messages = [
    "Думаю о тебе прямо сейчас 💭❤️",
    "Ты моё счастье и вдохновение ✨",
    "Моя любимая, ты у меня самая лучшая 🌹",
    "Хочу обнять тебя прямо сейчас 🤗",
    "Ты всегда в моём сердце 💖",
    "Я улыбаюсь, потому что думаю о тебе 😘",
    "Люблю тебя бесконечно 🔥"
]

kiss_messages = [
    "Целую тебя нежно 😘",
    "Один поцелуй для моей любимой 💋",
    "Ты моя сладкая конфетка 🍭💖",
    "Посылаю миллион поцелуев 💌",
    "Лови поцелуйчик от меня 😘"
]

# --- Функция для случайного выбора ---
def choose_random(messages):
    return random.choice(messages)

# --- Обработчики ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Комплимент тебе 💖"), KeyboardButton("Нежные комплименты 🌸")],
        [KeyboardButton("Доброе утро ☀️"), KeyboardButton("Спокойной ночи 🌙")],
        [KeyboardButton("Скучаю очень 😘"), KeyboardButton("Сюрприз 🎁")],
        [KeyboardButton("Люблю тебя ❤️"), KeyboardButton("Поцелуйчики 💋")],
        [KeyboardButton("Мега-сюрприз 🎉")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет, моя любовь ❤️", reply_markup=reply_markup)

async def compliment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(choose_random(love_compliments))

async def tender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(choose_random(tender_compliments))

async def morning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(choose_random(morning_messages))

async def night(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(choose_random(night_messages))

async def miss(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(choose_random(miss_messages))

async def surprise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(choose_random(surprise_messages))

async def love(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(choose_random(love_messages))

async def kiss(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(choose_random(kiss_messages))

async def mega_surprise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    all_messages = (love_compliments + tender_compliments + morning_messages +
                    night_messages + love_messages + miss_messages +
                    surprise_messages + kiss_messages)
    await update.message.reply_text(choose_random(all_messages))

# --- Автосообщения ---
def setup_scheduler(app: Application):
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    scheduler.add_job(lambda: asyncio.create_task(app.bot.send_message(CHAT_ID, random.choice(morning_messages))),
                      "cron", hour=9, minute=0)
    scheduler.add_job(lambda: asyncio.create_task(app.bot.send_message(CHAT_ID, random.choice(love_compliments))),
                      "cron", hour=15, minute=0)
    scheduler.add_job(lambda: asyncio.create_task(app.bot.send_message(CHAT_ID, random.choice(love_messages))),
                      "cron", hour=19, minute=0)
    scheduler.add_job(lambda: asyncio.create_task(app.bot.send_message(CHAT_ID, random.choice(night_messages))),
                      "cron", hour=23, minute=0)

    scheduler.start()

# --- Случайные сюрпризы ---
async def send_random_surprise(app: Application):
    while True:
        wait_hours = random.randint(1, 3)
        await asyncio.sleep(wait_hours * 3600)

        now = datetime.datetime.now().hour
        if 10 <= now <= 22:
            await app.bot.send_message(CHAT_ID, random.choice(surprise_messages))

async def on_startup(app: Application):
    setup_scheduler(app)
    asyncio.create_task(send_random_surprise(app))

# --- Запуск ---
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("^Комплимент тебе 💖$"), compliment))
    app.add_handler(MessageHandler(filters.Regex("^Нежные комплименты 🌸$"), tender))
    app.add_handler(MessageHandler(filters.Regex("^Доброе утро ☀️$"), morning))
    app.add_handler(MessageHandler(filters.Regex("^Спокойной ночи 🌙$"), night))
    app.add_handler(MessageHandler(filters.Regex("^Скучаю очень 😘$"), miss))
    app.add_handler(MessageHandler(filters.Regex("^Сюрприз 🎁$"), surprise))
    app.add_handler(MessageHandler(filters.Regex("^Люблю тебя ❤️$"), love))
    app.add_handler(MessageHandler(filters.Regex("^Поцелуйчики 💋$"), kiss))
    app.add_handler(MessageHandler(filters.Regex("^Мега-сюрприз 🎉$"), mega_surprise))

    # Запуск бота
    app.post_init = on_startup
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()