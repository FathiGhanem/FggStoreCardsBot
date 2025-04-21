import logging
import os
from PIL import Image, ImageDraw, ImageFont
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters
)
from datetime import datetime, timedelta
import arabic_reshaper
from bidi.algorithm import get_display
from dotenv import load_dotenv

load_dotenv()

AUTHORIZED_USER_ID = int(os.getenv("AUTHORIZED_USER"))
TOKEN = os.getenv("BOT_TOKEN")

PRICE, COUNTRY, CODE, NAME = range(4)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

FONT_PATH = "tahoma.ttf"
FONT_SIZE = int(40 * 3.125)

POSITIONS = {
    "الفئة": (300 * 3.125, 492 * 3.125),
    "رمز التفعيل": (150.5 * 3.125, 630 * 3.125),
    "اسم العميل": (300 * 3.125, 780 * 3.125),
    "تاريخ الاصدار": (30 * 3.125, 35 * 3.125),
    "وقت الاصدار": (30 * 3.125, 55 * 3.125)
}

def reshape_arabic_text(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def better_reshape_arabic_text(text):
    words = text.split()
    reshaped_words = []
    
    for word in words:
        reshaped = arabic_reshaper.reshape(word)
        displayed = get_display(reshaped)
        reshaped_words.append(displayed)
    
    return ' '.join(reshaped_words[::-1])

def fill_card(data: dict, base_image_path: str, output_path: str):
    image = Image.open(base_image_path).convert("RGBA")
    txt = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    bold_font = ImageFont.truetype(FONT_PATH, FONT_SIZE + 4)
    small_font = ImageFont.truetype(FONT_PATH, int(16 * 3.125))

    for key, value in data.items():
        pos = POSITIONS.get(key)
        if pos:
            if key in ["تاريخ الاصدار", "وقت الاصدار", "اسم العميل", "الفئة"]:
                if key == "اسم العميل" and "يا" in value:
                    value = better_reshape_arabic_text(value)
                else:
                    value = reshape_arabic_text(value)

            if key in ["تاريخ الاصدار", "وقت الاصدار"]:
                font_to_use = small_font
                draw.text(pos, value, font=font_to_use, fill=(255, 255, 255, 255))
            elif key == "رمز التفعيل":
                box_width = 320 * 3.125
                box_height = 70 * 3.125
                box_x = int((image.width - box_width) / 2)
                box_y = int(pos[1])

                max_font_size = int(60 * 3.125)
                min_font_size = int(10 * 3.125)
                current_font_size = max_font_size

                while current_font_size >= min_font_size:
                    test_font = ImageFont.truetype(FONT_PATH, current_font_size)
                    bbox = draw.textbbox((0, 0), value, font=test_font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    if text_width <= box_width and text_height <= box_height:
                        break
                    current_font_size -= 1

                final_font = ImageFont.truetype(FONT_PATH, current_font_size)
                text_width = draw.textlength(value, font=final_font)
                text_height = final_font.getbbox(value)[3]

                x_text = box_x + (box_width - text_width) / 2
                y_text = box_y + (box_height - text_height) / 2

                draw.text((x_text, y_text), value, font=final_font, fill=(255, 255, 255, 255))

            else:
                font_to_use = font
                bbox = draw.textbbox((0, 0), value, font=font_to_use)
                text_width = bbox[2] - bbox[0]
                x_center = (image.width - text_width) / 2
                y = pos[1] + 5
                draw.text((x_center, y), value, font=font_to_use, fill=(255, 255, 255, 255))

    combined = Image.alpha_composite(image, txt)
    combined.save(output_path)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("🚫 هذا البوت خاص بـ FGGSTORE فقط.")
        return ConversationHandler.END

    keyboard = [["10$", "20$", "25$"], ["50$", "100$"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text("📦 اختر قيمة البطاقة:", reply_markup=reply_markup)
    return PRICE

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["price"] = update.message.text.strip()

    keyboard = [["USA", "KSA", "UAE"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text("🌍 اختر الدولة:", reply_markup=reply_markup)
    return COUNTRY

async def country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    country = update.message.text.strip()
    price = context.user_data["price"]
    context.user_data["الفئة"] = f"{price} {country}"

    await update.message.reply_text("🔐 أدخل رمز التفعيل:")
    return CODE

async def code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip().upper()
    if user_input.count('-') == 2 and all(len(part) == 4 for part in user_input.split('-')):
        context.user_data["رمز التفعيل"] = user_input
    else:
        raw_code = user_input.replace(" ", "").replace("-", "")
        formatted_code = '-'.join([raw_code[i:i+4] for i in range(0, min(len(raw_code), 12), 4)])
        context.user_data["رمز التفعيل"] = formatted_code

    await update.message.reply_text("👤 ما اسم العميل؟")
    return NAME

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("🚫 هذا البوت خاص بـ FGGSTORE فقط.")
        return ConversationHandler.END

    name_input = update.message.text.strip()
    full_name = f"يا {name_input}"
    context.user_data["اسم العميل"] = full_name

    now = datetime.utcnow() + timedelta(hours=3)
    context.user_data["تاريخ الاصدار"] = now.strftime("%Y-%m-%d")
    context.user_data["وقت الاصدار"] = now.strftime("%I:%M %p")

    base_path = "card.png"
    output_path = f"output_{update.message.chat_id}.png"
    fill_card(context.user_data, base_path, output_path)

    with open(output_path, 'rb') as photo:
        await update.message.reply_photo(photo=photo)

    os.remove(output_path)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم إلغاء العملية.")
    return ConversationHandler.END

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, price)],
            COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, country)],
            CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, code)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()
