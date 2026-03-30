import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL = os.getenv("CHANNEL")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ================= تحقق الاشتراك =================
async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# ================= واجهة الأزرار =================
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("الحماية", callback_data="protection"),
        InlineKeyboardButton("التفعيل والتعطيل", callback_data="activation"),
        InlineKeyboardButton("المسح", callback_data="clear"),
        InlineKeyboardButton("الرفع", callback_data="promotion"),
        InlineKeyboardButton("المالكين", callback_data="owners"),
        InlineKeyboardButton("الأعضاء", callback_data="members"),
        InlineKeyboardButton("المطور", callback_data="dev"),
        InlineKeyboardButton("التسليه", callback_data="fun"),
        InlineKeyboardButton("القفل/الفتح", callback_data="lock_unlock"),
        InlineKeyboardButton("اشترك بالقناة", url=f"https://t.me/{CHANNEL.strip('@')}"),
    ]
    kb.add(*buttons)
    return kb

# ================= /start =================
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not await check_sub(message.from_user.id):
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("اشترك بالقناة", url=f"https://t.me/{CHANNEL.strip('@')}"))
        await message.reply("❌ يجب الاشتراك بالقناة أولاً", reply_markup=kb)
        return

    await message.reply("⭐️ أوامر البوت الرئيسية ⭐️", reply_markup=main_menu())

@dp.callback_query_handler(lambda c: True)
async def buttons(call: types.CallbackQuery):
    user_id = call.from_user.id

    if call.data == "dev":
        if user_id == ADMIN_ID:
            await call.message.edit_text("👨‍💻 أوامر المطور هنا …")
        else:
            await call.answer("❌ هذا القسم للمطور فقط", show_alert=True)
    else:
        await call.message.edit_text(f"📌 اخترت: {call.data}")

@dp.message_handler()
async def protect(message: types.Message):
    if "http" in message.text:
        await message.delete()
        await message.answer("🚫 يمنع نشر الروابط هنا")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
