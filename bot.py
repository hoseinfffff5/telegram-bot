from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8327721407:AAFBC0roX62msgJtMVsQ9k0JdTbm3_8tDXs"
CHANNEL_ID = -1005872940869          # آیدی عددی کانال
CHANNEL_USERNAME = "okmoallem"       # یوزرنیم کانال
FILE_PATH = "file.zip"               # فایل ارسالی

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# ---------------------- چک عضویت ----------------------
async def is_member(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# ---------------------- /start ----------------------
@dp.message_handler(commands=["start"])
async def start(msg: types.Message):

    join_btn = InlineKeyboardMarkup().add(
        InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME}"),
        InlineKeyboardButton("🔄 بررسی عضویت", callback_data="check")
    )

    await msg.answer(
        "سلام! 👋\nبرای دریافت فایل ابتدا باید در کانال زیر عضو شوید:",
        reply_markup=join_btn
    )


# ---------------------- بررسی عضویت ----------------------
@dp.callback_query_handler(lambda c: c.data == "check")
async def check_member(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if not await is_member(user_id):
        await callback.answer("❌ هنوز عضو نشدی! اول عضو شو.", show_alert=True)
        return

    # اگر عضو بود → دکمه دریافت فایل
    get_file = InlineKeyboardMarkup().add(
        InlineKeyboardButton("📥 دریافت فایل", callback_data="get_file")
    )

    await callback.message.answer("✅ عضویت شما تأیید شد!", reply_markup=get_file)
    await callback.answer()


# ---------------------- ارسال فایل ----------------------
@dp.callback_query_handler(lambda c: c.data == "get_file")
async def send_file(callback: types.CallbackQuery):

    if not await is_member(callback.from_user.id):
        await callback.answer("❌ هنوز عضو کانال نیستی!", show_alert=True)
        return

    await callback.message.answer_document(open(FILE_PATH, "rb"))
    await callback.answer()


# ---------------------- اجرا ----------------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
