import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    Message, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    CallbackQuery,
    ChatJoinRequest
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

TOKEN = os.getenv("TOKEN")

ADMIN_IDS = [1861529838, 7130847181]

VIP_CHANNEL_ID = "-1002535791299"
ONLINE_CLASS_CHANNEL_ID = "-1002667237249"

RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")
WEBHOOK_URL = f"{RENDER_EXTERNAL_URL}" if RENDER_EXTERNAL_URL else "https://kasn-bot-d7if.onrender.com"
WEBHOOK_PATH = f"/bot/{TOKEN}"
BASE_WEBHOOK_URL = f"{WEBHOOK_URL}{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)
dp = Dispatcher()

admin_msg_tracker = {}

# အကိုပေးထားသော လမ်းညွှန်စာရင်းအသစ်အတိုင်း ထည့်သွင်းထားပါသည်
ADS_CHANNELS = [
    {"name": "@kasnreviews", "id": "@kasnreviews"},
    {"name": "@movieblablabla", "id": "@movieblablabla"},
    {"name": "@kasnactions", "id": "@kasnactions"},
    {"name": "@indiamovieslovers", "id": "@indiamovieslovers"},
    {"name": "@kasnseries", "id": "@kasnseries"},
    {"name": "@kasncartoon", "id": "@kasncartoon"},
    {"name": "@horrorcrazymalay", "id": "@horrorcrazymalay"},
    {"name": "@myintmyatkar", "id": "@myintmyatkar"},
    {"name": "@romanticloverkasn", "id": "@romanticloverkasn"},
    {"name": "@japankaronlykasn", "id": "@japankaronlykasn"},
    {"name": "@onlyin18kasn", "id": "@onlyin18kasn"},
    {"name": "@kasnvivamax", "id": "@kasnvivamax"},
    {"name": "@fullkarkyichilar", "id": "@fullkarkyichilar"},
    {"name": "@allkarkyimalar", "id": "@allkarkyimalar"},
    {"name": "@pornworldkasn1", "id": "@pornworldkasn1"},
    {"name": "@kasnmoviewworld", "id": "@kasnmoviewworld"},
    {"name": "@kasnreviews1", "id": "@kasnreviews1"},
    {"name": "@kasnreviews3", "id": "@kasnreviews3"},
    {"name": "https://t.me/+jS8kwg4rG1ZkYWU1", "id": -1002514229884},
    {"name": "https://t.me/+ngM9sYGvAU44NDA1", "id": -1002761097664},
    {"name": "https://t.me/+laf6oHxHWklmMzE1", "id": -1002772827878},
    {"name": "https://t.me/+xK8FCmgVEd5kZWNl", "id": -1002568530868},
    {"name": "@moviewreviews", "id": "@moviewreviews"},
    {"name": "@mwzkarsones", "id": "@mwzkarsones"},
    {"name": "@mwaction", "id": "@mwaction"},
    {"name": "@mwromantic", "id": "@mwromantic"},
    {"name": "@mvonlyin18", "id": "@mvonlyin18"},
    {"name": "@vivamaxmw", "id": "@vivamaxmw"},
    {"name": "@mwjapankar", "id": "@mwjapankar"},
    {"name": "@mvloecar", "id": "@mvloecar"},
    {"name": "https://t.me/+GK1Vd9PJWpRjNmZl", "id": -1002778825049},
    {"name": "https://t.me/+-VzQ3zcPb1c1YzJl", "id": -1002771343903},
    {"name": "https://t.me/+Z_5OIp2otRI3YTE1", "id": -1002704169981},
]

class UserState(StatesGroup):
    waiting_for_vip_slip = State()
    waiting_for_class_slip = State()

def get_main_menu():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎬 Free Movie Channels များကို ဝင်ရန်", callback_data="free_movies")],
            [InlineKeyboardButton(text="📚 Online Class တက်ရောက်ရန်", callback_data="online_class")],
            [InlineKeyboardButton(text="💎 VIP Channel သို့ ဝင်ရောက်ရန်", callback_data="vip_channel")],
            [InlineKeyboardButton(text="📢 ကြော်ငြာစုံစမ်းဆွေးနွေးရန်", callback_data="ads_inquiry")],
            [InlineKeyboardButton(text="💬 ဆက်သွယ်ရန် / Admin သို့ စကားပြောရန်", callback_data="contact_admin")]
        ]
    )
    return keyboard

@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    welcome_text = (
        "မင်္ဂလာပါခင်ဗျာ 👋\n"
        "KASN Movie Platform မှ ကြိုဆိုပါတယ်။\n\n"
        "📌 အသုံးပြုပုံ လမ်းညွှန်ချက် (FAQ):\n"
        "• VIP Channel ဝင်လိုပါက နှိပ်ပြီး ငွေလွဲကာ ပြေစာပုံ ပို့ပေးပါ။\n"
        "• Online Class တက်လိုပါက အချက်အလက်ကြည့်ပြီး ပြေစာပုံ ပို့ပေးပါ။\n"
        "• ကြော်ငြာထည့်လိုပါက ကြော်ငြာစုံစမ်းဆွေးနွေးရန် ကို နှိပ်နိုင်ပါသည်။\n\n"
        "အောက်ပါတို့အနက်မှ လိုအပ်ရာကို ရွေးချယ်နိုင်ပါတယ် -"
    )
    await message.answer(text=welcome_text, reply_markup=get_main_menu())

@dp.callback_query(F.data == "free_movies")
async def process_free_movies(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    text = (
        "🎬 Free Movie Channels များ:\n\n"
        "ကျွန်ုပ်တို့ရဲ့ အခမဲ့ ရုပ်ရှင်ချန်နယ်တွေထဲကို အောက်ပါလင့်ခ်ကနေ ဝင်ရောက်နိုင်ပါတယ် -\n"
        "👉 https://t.me/kasnreviews"
    )
    await callback.message.answer(text)
    await callback.answer()

@dp.callback_query(F.data == "online_class")
async def process_online_class(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserState.waiting_for_class_slip)
    class_text = (
        "မင်္ဂလာပါခင်ဗျာ။ စိတ်ဝင်စားပေးလို့ ကျေးဇူးပါဗျ။\n\n"
        "ဇာတ်ကားချန်နယ်တေ ထောင်ပီး အချိန်ပိုင်းဝင်ငွေ သိန်းဆယ်ချီ ရချင်တဲ့သူတေအတွက် သင့်တော်တဲ့သင်တန်းပါခင်ဗျာ\n\n"
        "သင်တန်းကြေးကတော့ ၃၅,၀၀၀ ကျပ် ဖြစ်ပြီး အချိန်အကန့်အသတ်မရှိ လေ့လာနိုင်ပါတယ်။\n\n"
        "🤩 Wave - 09448835260 (Kaung Si Thu)\n"
        "🤩 Kpay - 09752828949 (Aye Sandar Moe)\n\n"
        "📌 [Online Class အတွက် ရွေးချယ်ထားပါသည်]\n"
        "ငွေလွဲပြီးပါက ပြေစာပုံကို ယခု Chat ထဲသို့ တိုက်ရိုက် ပို့ပေးပါခင်ဗျာ။\n\n"
        "ဆက်သွယ်ရန် 👇\n"
        "@milimeterz"
    )
    await callback.message.answer(class_text)
    await callback.answer()

@dp.callback_query(F.data == "vip_channel")
async def process_vip_channel(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserState.waiting_for_vip_slip)
    vip_text = (
        "မန်ဘာဝင်ရတာပါအကို series တွေက ကျန်တာတွေက မလိုပါဘူးဗျ မန်ဘာကြေးကသတ်မှတ်ထားတာမရှိဘဲ...\n\n"
        "5000 က စလို့ စေတနာရှိသလောက် အက်မင်ကို Support ပေးလို့ရပါတယ်...\n\n"
        "🤩 Wave - 09448835260 (Kaung Si Thu)\n"
        "🤩 Kpay - 09752828949 (Aye Sandar Moe)\n\n"
        "📌 [VIP Channel အတွက် ရွေးချယ်ထားပါသည်]\n"
        "ငွေလွဲပြီး ပြေစာပုံ ပို့ထားပေးပါခင်ဗျာ ။"
    )
    await callback.message.answer(vip_text)
    await callback.answer()

@dp.callback_query(F.data == "contact_admin")
async def process_contact_admin(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    text = (
        "💬 Admin သို့ တိုက်ရိုက်ဆက်သွယ်ရန်:\n\n"
        "အဆင်မပြေတာလေးများရှိပါက Admin ကို တိုက်ရိုက်ဆက်သွယ်နိုင်ပါတယ် -\n"
        "👉 @milimeterz"
    )
    await callback.message.answer(text)
    await callback.answer()

@dp.callback_query(F.data == "ads_inquiry")
async def process_ads_inquiry(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    
    text = "📢 **ကြော်ငြာလက်ခံမည့် ချန်နယ်များ**\n\n"
    for ch in ADS_CHANNELS:
        text += f"{ch['name']}\n"
        
    text += "\n1 sub = 3.5 ကျပ်\n"
    text += "one day one post pin ပါ"
        
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➡ ကြော်ငြာဈေးနှုန်း ဆက်လက်ကြည့်ရှုရန်", callback_data="ads_view_menu")]
        ]
    )
    
    if len(text) > 4000:
        chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
        for chunk in chunks[:-1]:
            await callback.message.answer(chunk)
        await callback.message.answer(chunks[-1], reply_markup=keyboard)
    else:
        await callback.message.answer(text, reply_markup=keyboard)
        
    await callback.answer()

@dp.callback_query(F.data == "ads_view_menu")
async def process_ads_view_menu(callback: CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📋 တစ်ခုချင်းစီ ဈေးနှုန်းကြည့်ရန်", callback_data="ads_view_each")],
            [InlineKeyboardButton(text="💎 ချန်နယ်အားလုံးပေါင်း Total ဈေးကြည့်ရန်", callback_data="ads_view_total")]
        ]
    )
    text = (
        "📊 **ကြော်ငြာကြေး တွက်ချက်မှု ရွေးချယ်ရန်**\n\n"
        "• 1 sub = 3.5 ကျပ်\n"
        "• one day one post pin ပါ\n\n"
        "အောက်ပါတို့အနက်မှ လိုအပ်သည်ကို ရွေးချယ်ပါ -"
    )
    await callback.message.answer(text, reply_markup=keyboard)
    await callback.answer()

@dp.callback_query(F.data == "ads_view_each")
async def process_ads_view_each(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("⏳ ချန်နယ်များ၏ Subscriber အရေအတွက်များကို စစ်ဆေးနေပါပြီ ခဏစောင့်ပါ...")
    
    text = "📋 **ချန်နယ်တစ်ခုချင်းစီ၏ ကြော်ငြာကြေး (Sub × 3.5 ကျပ်)**\n\n"
    
    for idx, ch in enumerate(ADS_CHANNELS, 1):
        channel_identifier = ch["id"]
        subs = 0
        
        # အောက်ဆုံးရောက်သွားသော ID (-1002704169981) အတွက် Default Sub ကို သတ်မှတ်ပေးခြင်း
        if channel_identifier == -1002704169981:
            subs = 77460
        else:
            try:
                subs = await bot.get_chat_member_count(channel_identifier)
            except Exception as e:
                print(f"Error fetching subs for {ch['name']}: {e}")
                subs = 0
            
        price = subs * 3.5
        text += f"{idx}. {ch['name']} ({subs:,} Subs) - `{price:,.1f}` ကျပ်\n"
        
    text += f"\n📌 one day one post pin ပါ။\n"
    text += f"💬 ဆက်သွယ်ရန် - @milimeterz"
    
    if len(text) > 4000:
        chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
        for chunk in chunks:
            await callback.message.answer(chunk)
    else:
        await callback.message.answer(text)
        
    await callback.answer("✅ တစ်ခုချင်းစီ၏ ဈေးနှုန်းများကို စစ်ဆေးပြသပြီးပါပြီ။")

@dp.callback_query(F.data == "ads_view_total")
async def process_ads_view_total(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("⏳ ချန်နယ်အားလုံး၏ Subscriber စုစုပေါင်းကို တွက်ချက်နေပါပြီ ခဏစောင့်ပါ...")
    
    total_subs = 0
    for ch in ADS_CHANNELS:
        channel_identifier = ch["id"]
        subs = 0
        
        # အောက်ဆုံးရောက်သွားသော ID (-1002704169981) အတွက် Default Sub ကို သတ်မှတ်ပေးခြင်း
        if channel_identifier == -1002704169981:
            subs = 77460
        else:
            try:
                subs = await bot.get_chat_member_count(channel_identifier)
            except Exception as e:
                print(f"Error fetching subs for {ch['name']}: {e}")
                subs = 0
                
        total_subs += subs
            
    total_price = total_subs * 3.5
    
    text = (
        "💎 **ချန်နယ်အားလုံးပေါင်း စုစုပေါင်းကြော်ငြာကြေး**\n\n"
        f"📊 ချန်နယ်အားလုံးရဲ့ Subscriber စုစုပေါင်း: `{total_subs:,}` Subs\n"
        f"💰 အားလုံးပေါင်းရဲ့ ကြော်ငြာကြေး (Total Sub × 3.5): `{total_price:,.1f}` ကျပ်\n\n"
        "📌 one day one post pin ပါ။\n"
        "💬 ဆက်သွယ်ရန် - @milimeterz"
    )
    await callback.message.answer(text)
    await callback.answer("✅ စုစုပေါင်း ကြော်ငြာကြေးကို တွက်ချက်ပြသပြီးပါပြီ။")

@dp.message(F.photo)
async def handle_payment_screenshot(message: Message, state: FSMContext):
    user = message.from_user
    current_state = await state.get_state()
    
    if current_state == UserState.waiting_for_vip_slip.state:
        purpose = "💎 ဝယ်ယူသည့်အမျိုးအစား: VIP Channel"
    elif current_state == UserState.waiting_for_class_slip.state:
        purpose = "📚 ဝယ်ယူသည့်အမျိုးအစား: Online Class"
    else:
        purpose = "❓ ဝယ်ယူသည့်အမျိုးအစား: မသတ်မှတ်ရသေးပါ"

    user_info = f"📩 ငွေလွဲပြေစာ အသစ်ရောက်ရှိပါပြီ!\n\n" \
                f"{purpose}\n" \
                f"👤 အမည်: {user.full_name}\n" \
                f"🔗 Username: @{user.username if user.username else 'None'}\n" \
                f"🆔 User ID: {user.id}"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💎 VIP Channel သို့ ထည့်ရန်", callback_data=f"approve_vip_{user.id}")],
            [InlineKeyboardButton(text="📚 Online Class သို့ ထည့်ရန်", callback_data=f"approve_class_{user.id}")]
        ]
    )

    tracker_key = f"payment_{user.id}"
    admin_msg_tracker[tracker_key] = {}

    for admin_id in ADMIN_IDS:
        try:
            sent_msg = await bot.send_photo(
                chat_id=admin_id,
                photo=message.photo[-1].file_id,
                caption=user_info,
                reply_markup=keyboard
            )
            admin_msg_tracker[tracker_key][admin_id] = sent_msg.message_id
        except Exception as e:
            print(f"ERROR: Failed to send photo to admin {admin_id}: {e}")

    await message.answer("ကျေးဇူးတင်ပါတယ်ခင်ဗျာ 🙏 ငွေလွဲပြေစာကို Admin ထံသို့ ပို့ပေးလိုက်ပါပြီ။ Admin မှ စစ်ဆေးပြီးပါက ချန်နယ်လင့်ခ် ပို့ပေးပါမည်။")
    await state.clear()

@dp.callback_query(F.data.startswith("approve_vip_"))
async def process_approve_vip(callback: CallbackQuery):
    target_user_id = int(callback.data.split("_")[2])
    tracker_key = f"payment_{target_user_id}"

    try:
        invite_link = await bot.create_chat_invite_link(
            chat_id=VIP_CHANNEL_ID,
            creates_join_request=True
        )

        await bot.send_message(
            chat_id=target_user_id,
            text=f"🎉 သင်၏ VIP Channel ငွေလွဲပြေစာ အတည်ပြုပြီးပါပြီ!\n\n"
                 f"VIP Channel သို့ ဝင်ရောက်ရန် အောက်ပါလင့်ခ်ကို နှိပ်ပြီး Join Request တင်ပေးပါ -\n"
                 f"👉 {invite_link.invite_link}"
        )

        for admin_id in ADMIN_IDS:
            try:
                await bot.send_message(
                    chat_id=admin_id,
                    text=f"✅ **VIP Channel လင့်ခ် ပို့ပြီးပါပြီ** (ဆောင်ရွက်သူ: {callback.from_user.full_name})\n\n"
                         f"👤 User ID: `{target_user_id}`\n"
                         f"🔗 Link: {invite_link.invite_link}"
                )
            except:
                pass

        if tracker_key in admin_msg_tracker:
            for admin_id, msg_id in admin_msg_tracker[tracker_key].items():
                try:
                    await bot.edit_message_caption(
                        chat_id=admin_id,
                        message_id=msg_id,
                        caption=callback.message.caption + f"\n\n✅ [VIP Channel လင့်ခ် ပို့ပြီးပါပြီ ({callback.from_user.full_name})]",
                        reply_markup=None
                    )
                except:
                    pass
            del admin_msg_tracker[tracker_key]

        await callback.answer("✅ VIP လင့်ခ် ပို့ပြီးပါပြီ။")

    except Exception as e:
        print(f"ERROR: Failed to approve VIP for user {target_user_id}: {e}")
        await callback.answer(f"❌ အမှားဖြစ်ပေါ်နေပါသည်: {e}", show_alert=True)

@dp.callback_query(F.data.startswith("approve_class_"))
async def process_approve_class(callback: CallbackQuery):
    target_user_id = int(callback.data.split("_")[2])
    tracker_key = f"payment_{target_user_id}"

    try:
        invite_link = await bot.create_chat_invite_link(
            chat_id=ONLINE_CLASS_CHANNEL_ID,
            creates_join_request=True
        )

        await bot.send_message(
            chat_id=target_user_id,
            text=f"🎉 သင်၏ Online Class ငွေလွဲပြေစာ အတည်ပြုပြီးပါပြီ!\n\n"
                 f"Online Class ချန်နယ်သို့ ဝင်ရောက်ရန် အောက်ပါလင့်ခ်ကို နှိပ်ပြီး Join Request တင်ပေးပါ -\n"
                 f"👉 {invite_link.invite_link}"
        )

        for admin_id in ADMIN_IDS:
            try:
                await bot.send_message(
                    chat_id=admin_id,
                    text=f"✅ **Online Class လင့်ခ် ပို့ပြီးပါပြီ** (ဆောင်ရွက်သူ: {callback.from_user.full_name})\n\n"
                         f"👤 User ID: `{target_user_id}`\n"
                         f"🔗 Link: {invite_link.invite_link}"
                )
            except:
                pass

        if tracker_key in admin_msg_tracker:
            for admin_id, msg_id in admin_msg_tracker[tracker_key].items():
                try:
                    await bot.edit_message_caption(
                        chat_id=admin_id,
                        message_id=msg_id,
                        caption=callback.message.caption + f"\n\n✅ [Online Class လင့်ခ် ပို့ပြီးပါပြီ ({callback.from_user.full_name})]",
                        reply_markup=None
                    )
                except:
                    pass
            del admin_msg_tracker[tracker_key]

        await callback.answer("✅ Online Class လင့်ခ် ပို့ပြီးပါပြီ။")

    except Exception as e:
        print(f"ERROR: Failed to approve Online Class for user {target_user_id}: {e}")
        await callback.answer(f"❌ အမှားဖြစ်ပေါ်နေပါသည်: {e}", show_alert=True)

@dp.chat_join_request()
async def handle_chat_join_request(chat_join: ChatJoinRequest):
    user = chat_join.from_user
    chat_id = chat_join.chat.id
    
    if str(chat_id) == VIP_CHANNEL_ID:
        channel_name = "💎 VIP Channel"
    elif str(chat_id) == ONLINE_CLASS_CHANNEL_ID:
        channel_name = "📚 Online Class"
    else:
        return

    admin_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ လက်ခံမည် (Approve)", callback_data=f"man_approve_{chat_id}_{user.id}"),
                InlineKeyboardButton(text="❌ ပယ်ချမည် (Decline)", callback_data=f"man_decline_{chat_id}_{user.id}")
            ]
        ]
    )

    request_text = (
        "📥 **ချန်နယ် Join Request အသစ် ရောက်ရှိနေပါပြီ!**\n\n"
        f"📌 ချန်နယ်: {channel_name}\n"
        f"👤 အမည်: {user.full_name}\n"
        f"🔗 Username: @{user.username if user.username else 'None'}\n"
        f"🆔 User ID: `{user.id}`"
    )

    tracker_key = f"join_{chat_id}_{user.id}"
    admin_msg_tracker[tracker_key] = {}

    for admin_id in ADMIN_IDS:
        try:
            sent_msg = await bot.send_message(
                chat_id=admin_id,
                text=request_text,
                reply_markup=admin_keyboard
            )
            admin_msg_tracker[tracker_key][admin_id] = sent_msg.message_id
        except Exception as e:
            print(f"ERROR sending join request to admin {admin_id}: {e}")

@dp.callback_query(F.data.startswith("man_approve_"))
async def process_manual_approve(callback: CallbackQuery):
    parts = callback.data.split("_")
    chat_id = int(parts[2])
    target_user_id = int(parts[3])
    tracker_key = f"join_{chat_id}_{target_user_id}"

    try:
        await bot.approve_chat_join_request(chat_id=chat_id, user_id=target_user_id)

        if str(chat_id) == VIP_CHANNEL_ID:
            success_message = (
                "🎉 ဂုဏ်ယူပါတယ်ခင်ဗျာ!\n\n"
                "သင့်ကို **VIP Channel** ထဲသို့ အောင်မြင်စွာ ထည့်သွင်းပေးလိုက်ပါပြီ။ "
                "အောက်မှာပေးထားတဲ့ list ကိုနှိပ်ပီး မိမိကြိုက်နှစ်သက်ရာကို ရွေးချယ်ကြည့်ရှု့နိုင်ပါပီခင်ဗျာ 👇👇👇\n\n"
                "📌 **လက်ရှိတင်ထားပီးသား Series များ**\n"
                "https://t.me/kasnseries/711"
            )
        else:
            success_message = (
                "🎉 ဂုဏ်ယူပါတယ်ခင်ဗျာ!\n\n"
                "သင့်ကို **Online Class** ထဲသို့ အောင်မြင်စွာ ထည့်သွင်းပေးလိုက်ပါပြီ။ "
                "video တေကိုမကျော်ဘဲ တစ်ပုဒ်ချင်းစီသေချာကြည့်ပီးလေ့လာစေချင်ပါတယ်ခင်ဗျာ။ "
                "နားမလည်တာရှိရင်လည်း အချိန်မရွေး လာပီးမေးမြန်းနိုင်ပါတယ် ✅"
            )

        await bot.send_message(chat_id=target_user_id, text=success_message)

        if tracker_key in admin_msg_tracker:
            for admin_id, msg_id in admin_msg_tracker[tracker_key].items():
                try:
                    await bot.edit_message_text(
                        chat_id=admin_id,
                        message_id=msg_id,
                        text=callback.message.text + f"\n\n✅ **[အတည်ပြုပြီးပါပြီ - {callback.from_user.full_name}]**",
                        reply_markup=None
                    )
                except:
                    pass
            del admin_msg_tracker[tracker_key]

        await callback.answer("✅ User ကို ချန်နယ်ထဲသို့ အောင်မြင်စွာ ထည့်သွင်းပြီး စာပို့ပြီးပါပြီ။")

    except Exception as e:
        print(f"ERROR in manual approve: {e}")
        await callback.answer(f"❌ အမှားဖြစ်ပေါ်နေပါသည်: {e}", show_alert=True)

@dp.callback_query(F.data.startswith("man_decline_"))
async def process_manual_decline(callback: CallbackQuery):
    parts = callback.data.split("_")
    chat_id = int(parts[2])
    target_user_id = int(parts[3])
    tracker_key = f"join_{chat_id}_{target_user_id}"

    try:
        await bot.decline_chat_join_request(chat_id=chat_id, user_id=target_user_id)
        
        if tracker_key in admin_msg_tracker:
            for admin_id, msg_id in admin_msg_tracker[tracker_key].items():
                try:
                    await bot.edit_message_text(
                        chat_id=admin_id,
                        message_id=msg_id,
                        text=callback.message.text + f"\n\n❌ **[ပယ်ချလိုက်ပါပြီ - {callback.from_user.full_name}]**",
                        reply_markup=None
                    )
                except:
                    pass
            del admin_msg_tracker[tracker_key]

        await callback.answer("❌ Join Request ကို ပယ်ချလိုက်ပါပြီ။")
    except Exception as e:
        print(f"ERROR in manual decline: {e}")
        await callback.answer(f"❌ အမှားဖြစ်ပေါ်နေပါသည်: {e}", show_alert=True)

@dp.message(F.from_user.id.in_(ADMIN_IDS))
async def admin_reply_handler(message: Message):
    if message.reply_to_message and message.reply_to_message.caption:
        caption = message.reply_to_message.caption
        try:
            if "User ID:" in caption:
                lines = caption.split("\n")
                target_user_id = None
                for line in lines:
                    if "User ID:" in line:
                        target_user_id = line.split("User ID:")[1].strip()
                        break
                
                if target_user_id:
                    target_id = int(target_user_id)
                    
                    if message.photo:
                        await bot.send_photo(
                            chat_id=target_id,
                            photo=message.photo[-1].file_id,
                            caption=f"💬 Admin မှ ပေးပို့သော မက်ဆေ့ချ်:\n\n{message.caption}" if message.caption else "💬 Admin မှ ပေးပို့သော ပုံ:"
                        )
                    elif message.text:
                        await bot.send_message(
                            chat_id=target_id,
                            text=f"💬 Admin မှ ပြောကြားချက်:\n\n{message.text}"
                        )
                        
                    await message.reply("✅ User ထံသို့ အောင်မြင်စွာ ပို့ပြီးပါပြီ။")
                    return
        except Exception as e:
            print(f"ERROR: Admin reply failed: {e}")
            await message.reply(f"❌ ပို့၍မရပါ။ အမှားအယွင်းရှိနေပါသည်: {e}")
            return
            
    await message.reply("💡 User ဆီ စာပြန်လိုပါက ပုံကို Reply လုပ်၍ စာ/ပုံ ပို့ပါ။")

async def on_startup(bot: Bot):
    await bot.set_webhook(BASE_WEBHOOK_URL, allowed_updates=["message", "callback_query", "chat_join_request"])

async def main():
    logging.basicConfig(level=logging.INFO)
    
    app = web.Application()
    
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    
    setup_application(app, dp, bot=bot)
    
    dp.startup.register(on_startup)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    
    print(f"Webhook Bot started on port {port}...")
    
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
