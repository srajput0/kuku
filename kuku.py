
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = 22007191
API_HASH = "00d245870a4a90186925b6985fea0e81"
BOT_TOKEN = "8396790178:AAGdB6U1SahvrhUyG8xCMCRYaHVNpvlMGx8"

bot = Client("kukufm_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

user_referrals = {}
required_referrals = 5
premium_users = set()

def generate_ref_code(user_id):
    return f"REF{user_id}"

@bot.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    ref = message.text.split(" ")[1] if len(message.text.split()) > 1 else None

    if ref and ref.startswith("REF") and ref != generate_ref_code(user_id):
        ref_user_id = int(ref.replace("REF", ""))
        user_referrals[ref_user_id] = user_referrals.get(ref_user_id, 0) + 1
        if user_referrals[ref_user_id] >= required_referrals:
            premium_users.add(ref_user_id)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎁 Refer & Earn Free Premium", callback_data="refer")],
        [InlineKeyboardButton("ℹ️ How it Works", callback_data="how_it_works")]
    ])

    await message.reply_photo(
        photo="https://i.ibb.co/DggK7B5h/x.jpg",
        caption=(
            "**🎧 Welcome to KukuFM 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 Bot!**\n\n"
            "Enjoy unlimited access to **Audiobooks**, **Courses**, and **Podcasts** in your language.\n\n"
            "🔥 Refer your friends and get **P R E M I U M** access for free!\n\n"
            "_Click below to begin._"
        ),
        reply_markup=keyboard
    )

@bot.on_callback_query()
async def handle_callbacks(client, callback_query):
    data = callback_query.data
    user_id = callback_query.from_user.id

    if data == "refer":
        ref_code = generate_ref_code(user_id)
        count = user_referrals.get(user_id, 0)
        has_premium = user_id in premium_users
        msg = (
            f"🎁 **Refer & Earn Premium**\n\n"
            f"Your Referral Link:\nhttps://t.me/{client.me.username}?start={ref_code}\n\n"
            f"👥 Referrals: {count}/{required_referrals}\n"
        )
        if has_premium:
            msg += "🎉 Congratulations! You have received a PREMIUM access code.\nPlease send this code to @SiDXTN to activate your premium."
        else:
            msg += "🔓 Invite 5 friends to unlock free premium access.\nOnce done, you will receive your code."

        await callback_query.message.edit_text(
            msg,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Back 🔙", callback_data="back")]
            ]),
            disable_web_page_preview=True
        )

    elif data == "how_it_works":
        await callback_query.message.edit_text(
            "ℹ️ **How to Get KukuFM Premium FREE**\n\n"
            "1. Share your referral link with friends.\n"
            "2. When 5 friends join via your link, you qualify for free access.\n"
            "3. Bot will send you a premium code.\n"
            "4. Send that code to @SiDXTN to activate your Premium.\n\n"
            "No payment required! Just refer and enjoy. 🧡",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Back 🔙", callback_data="back")]
            ])
        )

    elif data == "back":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎁 Refer & Earn Free Premium", callback_data="refer")],
            [InlineKeyboardButton("ℹ️ How it Works", callback_data="how_it_works")]
        ])

        await callback_query.message.edit_text(
            "**🎧 Welcome to KukuFM 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 Bot!**\n\n"
            "Enjoy unlimited access to **Audiobooks**, **Courses**, and **Podcasts** in your language.\n\n"
            "🔥 Refer your friends and get **P R E M I U M** access for free!",
            reply_markup=keyboard
        )

print("Bot is running...")
bot.run()
