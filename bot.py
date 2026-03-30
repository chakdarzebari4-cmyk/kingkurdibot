import logging
import random
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 2011675494
CHANNEL = "@ybpi1"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("الحماية", callback_data="1"),
        InlineKeyboardButton("التفعيل/التعطيل", callback_data="2"),
        InlineKeyboardButton("المسح", callback_data="3"),
        InlineKeyboardButton("الرفع", callback_data="4"),
        InlineKeyboardButton("المالكين", callback_data="5"),
        InlineKeyboardButton("الأعضاء", callback_data="6"),
        InlineKeyboardButton("القفل/الفتح", callback_data="lockunlock"),
        InlineKeyboardButton("التسليه", callback_data="games"),
        InlineKeyboardButton("إسلاميات", callback_data="islamic"),
        InlineKeyboardButton("اشترك بالقناة", url=f"https://t.me/{CHANNEL.strip('@')}")
    )
    return kb

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not await check_sub(message.from_user.id):
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("اشترك بالقناة", url=f"https://t.me/{CHANNEL.strip('@')}"))
        await message.reply("❌ لازم تشترك بالقناة أولاً", reply_markup=kb)
        return

    await message.reply("⭐️ أوامر البوت ⭐️", reply_markup=main_menu())

@dp.callback_query_handler(lambda c:
