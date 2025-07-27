from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import time

API_ID = 22007191
API_HASH = "00d245870a4a90186925b6985fea0e81"
BOT_TOKEN = "8396790178:AAEkfaE8UyU5SuexXF409Q05LZgdlIvRw6M"

bot = Client("kukufm_fake_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# In-memory fake referral tracking
user_referrals = {}
user_free_unlocked = set()

# Generate fake license
def generate_license():
    return "KUKU-" + "-".join(["".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=4)) for _ in range(3)])

def generate_ref_code(user_id):
    return f"REF{user_id}"

# Start command
@bot.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    ref = message.text.split(" ")[1] if len(message.text.split()) > 1 else None

    # Fake referral count
    if ref and ref.startswith("REF") and ref != generate_ref_code(user_id):
        ref_user_id = int(ref.replace("REF", ""))
        user_referrals[ref_user_id] = user_referrals.get(ref_user_id, 0) + 1

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 Explore Premium Plans", callback_data="plans")],
        [InlineKeyboardButton("🎁 Refer & Get Free Premium", callback_data="refer")],
        [InlineKeyboardButton("ℹ️ How it Works", callback_data="how_it_works")]
    ])

    await message.reply_photo(
        photo="https://yourserver.com/kukufm_banner.jpg",
        caption=(
            "**🎧 Welcome to KukuFM Premium Bot!**\n\n"
            "Enjoy unlimited access to Audiobooks, Courses, and Podcasts.\n\n"
            "Choose an option below to begin."
        ),
        reply_markup=keyboard
    )

# Refer & Earn
@bot.on_callback_query(filters.regex("refer"))
async def refer_menu(client, callback_query):
    user_id = callback_query.from_user.id
    ref_code = generate_ref_code(user_id)
    count = user_referrals.get(user_id, 0)

    msg = (
        f"🎁 **Refer & Earn Premium**\n\n"
        f"Invite friends to get **Free Premium Access!**\n\n"
        f"🔗 Your Referral Link:\n"
        f"`https://t.me/{bot.me.username}?start={ref_code}`\n\n"
        f"👥 Referred: `{count}` users\n"
        f"🎉 Unlock at 3 referrals!"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Refresh", callback_data="refer")],
        [InlineKeyboardButton("⬅️ Back", callback_data="start")]
    ])

    # Check if free premium unlocked
    if count >= 3 and user_id not in user_free_unlocked:
        user_free_unlocked.add(user_id)
        fake_license = generate_license()
        msg += f"\n\n✅ *Free Premium Activated!*\n🔑 License: `{fake_license}`"

    await callback_query.message.edit_caption(msg, reply_markup=keyboard)

# Plans menu
@bot.on_callback_query(filters.regex("plans"))
async def show_plans(client, callback_query):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🥇 1 Month - ₹29", callback_data="get_plan_1")],
        [InlineKeyboardButton("🏅 3 Months - ₹59", callback_data="get_plan_3")],
        [InlineKeyboardButton("👑 12 Months - ₹99", callback_data="get_plan_12")],
        [InlineKeyboardButton("⬅️ Back", callback_data="start")]
    ])
    await callback_query.message.edit_caption(
        "**📦 Available Premium Plans:**\n\n"
        "🥇 1 Month – ₹29\n"
        "🏅 3 Months – ₹59\n"
        "👑 12 Months – ₹99\n\n"
        "Select a plan to activate fake premium.",
        reply_markup=keyboard
    )

@bot.on_callback_query(filters.regex("how_it_works"))
async def how_it_works(client, callback_query):
    await callback_query.message.edit_caption(
        "**ℹ️ How it Works:**\n\n"
        "1. Choose a premium plan or refer friends.\n"
        "2. Get a fake premium license key.\n"
        "3. Just for fun – this is a parody/demo bot!\n\n"
        "_Use /refer to get your link._",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Back", callback_data="start")]
        ])
    )

# Fake premium activation
@bot.on_callback_query(filters.regex("get_plan_(.*)"))
async def fake_activation(client, callback_query):
    duration_map = {
        "1": "1 Month",
        "3": "3 Months",
        "12": "12 Months"
    }
    plan = callback_query.data.split("_")[-1]
    duration = duration_map.get(plan, "1 Month")

    msg = await callback_query.message.edit_caption(f"🔄 Processing your {duration} Premium Activation...")
    time.sleep(2)

    await msg.edit_caption("🔐 Verifying payment...")
    time.sleep(2)

    fake_license = generate_license()
    await msg.edit_caption(
        f"✅ **KukuFM Premium Activated!**\n\n"
        f"📅 Duration: {duration}\n"
        f"🔑 License Key: `{fake_license}`\n\n"
        "Enjoy your fake premium! 🎧",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎧 Use License (Fake)", url="https://kukufm.com")],
            [InlineKeyboardButton("🔁 Activate Again", callback_data="plans")]
        ])
    )

bot.run()
