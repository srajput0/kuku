
from pyrogram import Client, filters
#from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#from pyrogram import InputFile

API_ID = 22007191
API_HASH = "00d245870a4a90186925b6985fea0e81"
BOT_TOKEN = "8396790178:AAEkfaE8UyU5SuexXF409Q05LZgdlIvRw6M"

bot = Client("kukufm_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

user_referrals = {}

def generate_ref_code(user_id):
    return f"REF{user_id}"

@bot.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    ref = message.text.split(" ")[1] if len(message.text.split()) > 1 else None

    # Fake referral tracking
    if ref and ref.startswith("REF") and ref != generate_ref_code(user_id):
        ref_user_id = int(ref.replace("REF", ""))
        user_referrals[ref_user_id] = user_referrals.get(ref_user_id, 0) + 1

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🧡 Explore Premium Plans", callback_data="plans")],
        [InlineKeyboardButton("🎁 Refer & Earn Free Premium", callback_data="refer")],
        [InlineKeyboardButton("ℹ️ How it Works", callback_data="how_it_works")]
    ])

    await message.reply_photo(
        photo="https://i.ibb.co/DggK7B5h/x.jpg",
        caption=(
            "**🎧 Welcome to KukuFM 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 Bot!**\n\n"
            "Enjoy unlimited access to **Audiobooks**, **Courses**, and **Podcasts** in your language.\n\n"
            "🔥 Get **P R E M I U M** access with a plan or refer friends!\n\n"
            "_Click below to begin._"
        ),
        reply_markup=keyboard
    )

@bot.on_callback_query()
async def handle_callbacks(client, callback_query):
    data = callback_query.data
    user_id = callback_query.from_user.id

    if data == "plans":
        await callback_query.message.edit_text(
            "**💼 Premium Plans**\n\nChoose a plan:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("1 Month Access - ₹49", callback_data="pay_49")],
                [InlineKeyboardButton("Back 🔙", callback_data="back")]
            ])
        )

    elif data == "refer":
        ref_code = generate_ref_code(user_id)
        await callback_query.message.edit_text(
            f"🎁 Refer your friends and earn FREE Premium!\n\nShare your referral link:\n"
            f"`https://t.me/SiDXTN?start={ref_code}`\n\n"
            f"✅ When 5 friends join using your link, you’ll get FREE access!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Back 🔙", callback_data="back")]
            ])
        )

    elif data == "how_it_works":
        await callback_query.message.edit_text(
            "ℹ️ **How KukuFM Premium Works**\n\n"
            "1. Choose a plan or refer friends\n"
            "2. Complete payment using UPI or earn free access\n"
            "3. Access unlocked within 15 minutes\n\n"
            "For support, contact @SiDXTN",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Back 🔙", callback_data="back")]
            ])
        )

    elif data == "pay_49":
        await callback_query.message.edit_text(
            f"🧾 **KukuFM Premium - ₹49 (1 Month)**\n\n"
            f"Your Telegram ID: `{user_id}`\n\n"
            f"Send payment via UPI to: `thakur@455463`\n"
            f"After payment, send screenshot with your ID to [@SiDXTN](http://t.me/SiDXTN)\n\n"
            f"⚠️ Fake payments will lead to a permanent ban.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ I have paid", callback_data="confirm_payment")],
                [InlineKeyboardButton("Back 🔙", callback_data="back")]
            ])
        )

    elif data == "confirm_payment":
        await callback_query.message.edit_text(
            "✅ Your payment is being verified.\n\n"
            "⏳ Please wait up to 15 minutes while we activate your Premium.\n"
            "Contact @SiDXTN if it takes longer."
        )

    elif data == "back":
        await callback_query.message.edit_text(
            "**🎧 Welcome to KukuFM 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 Bot!**\n\n"
            "Enjoy unlimited access to **Audiobooks**, **Courses**, and **Podcasts**.\n\n"
            "🔥 Get **P R E M I U M** access with a plan or refer friends!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🧡 Explore Premium Plans", callback_data="plans")],
                [InlineKeyboardButton("🎁 Refer & Earn Free Premium", callback_data="refer")],
                [InlineKeyboardButton("ℹ️ How it Works", callback_data="how_it_works")]
            ])
        )

print("Bot is running...")
bot.run()

