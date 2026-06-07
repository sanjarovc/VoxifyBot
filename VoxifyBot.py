from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

import edge_tts
from langdetect import detect
import os

TOKEN = "8423933846:AAE85hEEalAWdLNliQVKZNAm03SNbHFEOms"


def normalize_uzbek_text(text):

    replacements = {
        "o‘": "o'",
        "g‘": "g'",
        "sh": "sh",
        "ch": "ch",
        "ng": "ng",
        "yo‘q": "yok",
        "bo‘ldi": "boldi",
        "to‘g‘ri": "togri",
        "Assalomu alaykum": "Assalomu aleykum"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text



# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "🎤 VoxifyBot ishga tushdi!\n\n"
        "Menga istalgan matn yuboring.\n"
        "Men uni AI ovozga aylantiraman 🔥"
    )

    await update.message.reply_text(text)


# Tilga qarab voice tanlash
def get_voice(language):

    voices = {
        "uz": "uz-UZ-MadinaNeural",
        "ru": "ru-RU-DmitryNeural",
        "en": "en-US-GuyNeural",
        "tr": "tr-TR-AhmetNeural",
        "ar": "ar-SA-HamedNeural",
        "fr": "fr-FR-HenriNeural",
        "de": "de-DE-ConradNeural"
    }

    return voices.get(language, "en-US-GuyNeural")


# Matnni ovoz qilish
async def text_to_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = normalize_uzbek_text(update.message.text)

    try:

        # Tilni aniqlash
        language = detect(text)

        # Voice tanlash
        voice = get_voice(language)

        filename = f"{update.message.chat_id}.mp3"

        # AI voice yaratish
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice
        )

        await communicate.save(filename)

        # Telegramga yuborish
        with open(filename, "rb") as audio:
            await update.message.reply_voice(audio)

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(
            f"Xatolik: {e}"
        )


# Bot yaratish
app = Application.builder().token(TOKEN).build()

# Handlerlar
app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        text_to_voice
    )
)

print("🎤 VoxifyBot ishga tushdi...")

app.run_polling()