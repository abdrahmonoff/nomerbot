# -*- coding: utf-8 -*-
import os
import json
import logging
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ContentType

# ========= CONFIG =========
# MUHIM: Quyidagi 3 ta joyni o'zgartiring!

# 1. TOKEN - BotFather dan olingan token
# Masalan: "6789012345:AAEabcDefGhIjKlMnOpQrStUvWxYz123456"
TOKEN = "6518211111:AAFGnUEBzp7H1-SK2DU3sSGxAjx_StBOpUc"

# 2. ADMIN_ID - @userinfobot dan olingan ID raqam
# Masalan: 987654321
ADMIN_ID = 817765302

# 3. ADMIN_USERNAME - Sizning Telegram username ingiz (@ belgisisiz)
# Masalan: "sarvar_dev"
ADMIN_USERNAME = "abdrahmonoff"

# 4. ISHCHI VAQT - Xizmat ko'rsatish vaqti
WORK_START_HOUR = 9   # 09:00 dan
WORK_END_HOUR = 23    # 23:00 gacha
# Ish vaqtidan tashqari - faqat ma'lumot ko'rish mumkin

PAYMENTS_FILE = "payments.jsonl"
SALES_FILE = "sales.jsonl"
PRICE = 30000

# Statistika yuborish vaqti (soat:daqiqa - 24-soatlik format)
DAILY_REPORT_TIME = "23:00"  # Har kuni soat 23:00 da
# ==========================

def is_working_hours():
    """Ishchi vaqtni tekshirish - 09:00 dan 23:00 gacha"""
    now = datetime.now()
    current_hour = now.hour
    return WORK_START_HOUR <= current_hour < WORK_END_HOUR

def log_payment_entry(entry: dict):
    try:
        with open(PAYMENTS_FILE, "a", encoding="utf-8") as f:
            json.dump(entry, f, ensure_ascii=False)
            f.write("\n")
    except Exception as e:
        logging.error(f"Payment log failed: {e}")

def log_sale_entry(user_id: int, phone: str):
    """Sotilgan raqamni log qilish - FAQAT kod yuborilganda"""
    try:
        entry = {
            "time": datetime.utcnow().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "user_id": user_id,
            "phone": phone,
            "price": PRICE
        }
        with open(SALES_FILE, "a", encoding="utf-8") as f:
            json.dump(entry, f, ensure_ascii=False)
            f.write("\n")
        logging.info(f"Sale logged: {user_id} - {phone}")
    except Exception as e:
        logging.error(f"Sale log failed: {e}")

def get_statistics(days: int = 1):
    """Statistika olish"""
    try:
        from datetime import timedelta
        
        today = datetime.now().date()
        start_date = today - timedelta(days=days-1)
        
        sales = []
        if os.path.exists(SALES_FILE):
            with open(SALES_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        sale_date = datetime.fromisoformat(entry["time"]).date()
                        if start_date <= sale_date <= today:
                            sales.append(entry)
                    except:
                        continue
        
        total_sales = len(sales)
        total_profit = total_sales * PRICE
        
        return {
            "sales": total_sales,
            "profit": total_profit,
            "period_days": days
        }
    except Exception as e:
        logging.error(f"Statistics error: {e}")
        return {"sales": 0, "profit": 0, "period_days": days}

async def send_daily_report():
    """Kunlik hisobot yuborish - faqat bugungi ma'lumotlar"""
    try:
        today_stats = get_statistics(1)
        
        report = (
            "📊 *KUNLIK HISOBOT*\n"
            f"📅 Sana: {datetime.now().strftime('%d.%m.%Y')}\n\n"
            
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"📱 Sotilgan raqamlar: *{today_stats['sales']} ta*\n"
            f"💰 Foyda: *{today_stats['profit']:,} so'm*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "✅ Kunlik hisobot"
        )
        
        await bot.send_message(ADMIN_ID, report, parse_mode="Markdown")
        logging.info("Daily report sent successfully")
        
    except Exception as e:
        logging.error(f"Daily report failed: {e}")

async def send_monthly_report():
    """Oylik hisobot - o'tgan oyning to'liq statistikasi"""
    try:
        from datetime import timedelta
        
        # O'tgan oyni hisoblash
        today = datetime.now()
        first_day_current_month = today.replace(day=1)
        last_day_prev_month = first_day_current_month - timedelta(days=1)
        first_day_prev_month = last_day_prev_month.replace(day=1)
        
        # O'tgan oy nomi
        months = [
            "Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun",
            "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"
        ]
        prev_month_name = months[last_day_prev_month.month - 1]
        prev_year = last_day_prev_month.year
        
        # O'tgan oyning kunlari soni
        days_in_month = (first_day_current_month - first_day_prev_month).days
        
        # O'tgan oy statistikasini olish
        stats = get_statistics(days_in_month)
        
        # O'rtacha kunlik
        avg_daily = stats['sales'] // days_in_month if stats['sales'] > 0 else 0
        
        report = (
            "📊 *OYLIK HISOBOT*\n"
            f"📅 {prev_month_name} {prev_year}\n\n"
            
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"📱 Jami sotilgan: *{stats['sales']} ta*\n"
            f"💰 Jami foyda: *{stats['profit']:,} so'm*\n"
            f"📉 O'rtacha kunlik: *{avg_daily} ta*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"✅ {prev_month_name} oyi yakunlandi"
        )
        
        await bot.send_message(ADMIN_ID, report, parse_mode="Markdown")
        logging.info(f"Monthly report sent for {prev_month_name} {prev_year}")
        
    except Exception as e:
        logging.error(f"Monthly report failed: {e}")

async def schedule_daily_reports():
    """Har kuni statistika yuborish - soat 23:00 da"""
    while True:
        try:
            now = datetime.now()
            report_hour, report_minute = map(int, DAILY_REPORT_TIME.split(":"))
            today_report = now.replace(hour=report_hour, minute=report_minute, second=0, microsecond=0)
            
            if now >= today_report:
                from datetime import timedelta
                today_report += timedelta(days=1)
            
            wait_seconds = (today_report - now).total_seconds()
            logging.info(f"Next daily report in {wait_seconds/3600:.1f} hours at {today_report.strftime('%d.%m.%Y %H:%M')}")
            
            await asyncio.sleep(wait_seconds)
            await send_daily_report()
            await asyncio.sleep(60)
            
        except Exception as e:
            logging.error(f"Daily schedule error: {e}")
            await asyncio.sleep(3600)

async def schedule_monthly_reports():
    """Har oyning 1-sanasida o'tgan oy hisobotini yuborish - soat 09:00 da"""
    while True:
        try:
            from datetime import timedelta
            
            now = datetime.now()
            
            # Keyingi 1-sana, soat 09:00
            if now.day == 1 and now.hour < 9:
                # Bugun 1-sana va soat 9 dan oldin
                next_report = now.replace(hour=9, minute=0, second=0, microsecond=0)
            else:
                # Keyingi oyning 1-sanasi
                if now.month == 12:
                    next_month = now.replace(year=now.year + 1, month=1, day=1, hour=9, minute=0, second=0, microsecond=0)
                else:
                    next_month = now.replace(month=now.month + 1, day=1, hour=9, minute=0, second=0, microsecond=0)
                next_report = next_month
            
            wait_seconds = (next_report - now).total_seconds()
            logging.info(f"Next monthly report in {wait_seconds/86400:.1f} days at {next_report.strftime('%d.%m.%Y %H:%M')}")
            
            await asyncio.sleep(wait_seconds)
            await send_monthly_report()
            await asyncio.sleep(3600)  # 1 soat kutish
            
        except Exception as e:
            logging.error(f"Monthly schedule error: {e}")
            await asyncio.sleep(3600)

AWAITING_CHECK = set()
USED_CHECK_PHOTOS = {}
PENDING_NUMBERS = {}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def number_expire_timer(user_id: int):
    """20 daqiqa timer - vaqt tugaganda xabar yuborish"""
    await asyncio.sleep(20 * 60)  # 20 daqiqa
    
    try:
        # Foydalanuvchiga xabar
        await bot.send_message(
            user_id,
            "⏰ Raqam muddati tugadi\n\n"
            "Afsuski, 20 daqiqalik muddat tugadi.\n\n"
            "💬 Agar muammo bo'lgan bo'lsa:\n"
            "👉 Admin bilan bog'laning: @{}\n"
            "Vaziyatni tushuntirib bering, yordam beramiz!".format(ADMIN_USERNAME),
            reply_markup=get_main_menu()
        )
        logging.info(f"⏰ Timer expired for user {user_id}")
        
        # Admin ga xabar
        await bot.send_message(
            ADMIN_ID,
            f"⏰ Vaqt tugadi\n\n"
            f"👤 User ID: `{user_id}`\n"
            f"⏱ 20 daqiqa o'tdi\n\n"
            f"Tekshiring: Kod yuborgan bo'lsangizmi?",
            parse_mode="Markdown"
        )
        
    except Exception as e:
        logging.error(f"Timer notification failed for {user_id}: {e}")

def get_main_menu():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📲 Raqam olish"), KeyboardButton(text="💰 Narxlar")],
            [KeyboardButton(text="✅ Qanday ishlaydi?")],
            [KeyboardButton(text="🛠 Yordam"), KeyboardButton(text="👤 Admin bilan aloqa")]
        ],
        resize_keyboard=True
    )
    return kb

async def start(message: Message):
    text = (
        "👋 Assalomu alaykum!\n\n"
        "🎥 YouTube kanalini tasdiqlash uchun Indonesia raqami xizmati.\n\n"
        "✅ Nimalar olasiz:\n"
        "  • 🇮🇩 Indonesia raqami\n"
        "  • 🔐 Tasdiqlash kodi\n"
        "  • ⏱ 20 daqiqa muddat\n"
        "  • 💬 Yordam va qo'llab-quvvatlash\n\n"
        "💰 Narx: 30,000 so'm\n\n"
        "🕐 Ishchi vaqt: 09:00 - 23:00\n"
        "(Xizmat faqat ish vaqtida ko'rsatiladi)\n\n"
        "⚠️ Muhim: Bu raqam faqat YouTube kanal verifikatsiyasi uchun.\n"
        "Google account ochish uchun ishlamaydi.\n\n"
        "Quyidagi menyudan kerakli bo'limni tanlang 👇"
    )
    await message.answer(text, reply_markup=get_main_menu())

async def menu_buy(message: Message):
    # Ishchi vaqtni tekshirish
    if not is_working_hours():
        now = datetime.now()
        await message.answer(
            f"🕐 ISHCHI VAQT: 09:00 - 23:00\n\n"
            f"⏰ Hozirgi vaqt: {now.strftime('%H:%M')}\n\n"
            f"Afsuski, hozir ish vaqti emas.\n"
            f"Iltimos, bugun 09:00 dan 23:00 gacha bo'lgan vaqtda qayta urinib ko'ring.\n\n"
            f"📋 Ish vaqtida siz:\n"
            f"  • Raqam sotib olishingiz\n"
            f"  • To'lov qilishingiz\n"
            f"  • Xizmat olishingiz mumkin\n\n"
            f"💬 Savol bo'lsa: @{ADMIN_USERNAME}\n\n"
            f"Tushunganingiz uchun rahmat! 😊",
            reply_markup=get_main_menu()
        )
        return
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📲 Sotib olish", callback_data="buy")]
    ])
    
    await message.answer(
        "💳 To'lov: *30,000 so'm*\n\n"
        "🎥 YouTube kanalini tasdiqlash uchun *Indonesia* 🇮🇩 raqami olib beraman.\n\n"
        "⚠️ *Diqqat:* Bu raqam *faqat YouTube kanal verifikatsiyasi* uchun!\n"
        "Google account/Gmail ochish uchun ishlatib bo'lmaydi.\n\n"
        "Davom etish uchun pastdagi tugmani bosing 👇",
        reply_markup=kb,
        parse_mode="Markdown"
    )

async def menu_prices(message: Message):
    await message.answer(
        "💰 *Xizmat narxi:*\n\n"
        "📱 YouTube tasdiqlash uchun raqam – *30,000 so'm*\n\n"
        "🌎 Davlat: *Indonesia* 🇮🇩\n"
        "⏱ Har bir raqam 20 daqiqa amal qiladi.\n"
        "🔐 Raqamlar faqat YouTube tasdiqlash uchun mo'ljallangan.",
        parse_mode="Markdown",
        reply_markup=get_main_menu()
    )

async def menu_how_it_works(message: Message):
    text = (
        "✅ QANDAY ISHLAYDI?\n\n"
        "1️⃣ 📲 Raqam olish tugmasini bosing\n"
        "2️⃣ To'lov qiling va chekni yuboring\n"
        "3️⃣ Admin sizga Indonesia raqamini yuboradi\n"
        "4️⃣ YouTube'da raqamni kiriting\n"
        "5️⃣ Kod kelgach, botda 'Kod yubordim' bosing\n"
        "6️⃣ Admin tasdiqlash kodini yuboradi\n"
        "7️⃣ Kodni YouTube'ga kiriting - tayyor! ✅\n\n"
        "⏱ Raqam 20 daqiqa amal qiladi.\n"
        "Odatda jarayon 5-10 daqiqa davom etadi.\n\n"
        "💬 Savol yoki muammo bo'lsa:\n"
        "👉 Admin: @{}\n"
        "Yordam beramiz!".format(ADMIN_USERNAME)
    )
    await message.answer(text, reply_markup=get_main_menu())

async def menu_help(message: Message):
    text = (
        "🛠 YORDAM BO'LIMI\n\n"
        "Agar botdan foydalanishda qiyinchilik bo'lsa yoki biror joy tushunarsiz bo'lsa, "
        "admin bilan bog'laning.\n\n"
        f"👤 Admin: @{ADMIN_USERNAME}"
    )
    await message.answer(text, reply_markup=get_main_menu())

async def menu_contact_admin(message: Message):
    text = (
        "👤 ADMIN BILAN ALOQA\n\n"
        f"Telegram: @{ADMIN_USERNAME}\n\n"
        "Savollaringiz, takliflaringiz yoki muammolar bo'lsa, bemalol yozib qoldiring."
    )
    await message.answer(text, reply_markup=get_main_menu())

async def cmd_help(message: Message):
    text = (
        "🛠 YORDAM\n\n"
        "Bot yordamida YouTube tasdiqlash uchun raqam olasiz.\n\n"
        "Asosiy qadamlar:\n"
        "1️⃣ 📲 Raqam olish - to'lov qiling\n"
        "2️⃣ To'lov chekini skrinshot qilib yuboring\n"
        "3️⃣ Admin sizga raqam yuboradi\n"
        "4️⃣ YouTube'da raqamni kiriting, kodni oling\n"
        "5️⃣🔐 Kod yubordim tugmasini bosing\n"
        "6️⃣ Admin sizga tasdiqlash kodini yuboradi\n\n"
        "Muammo bo'lsa 👤 Admin bilan aloqa bo'limidan foydalaning."
    )
    await message.answer(text, reply_markup=get_main_menu())

async def cmd_info(message: Message):
    text = (
        "ℹ️ XIZMAT HAQIDA\n\n"
        "📺 Xizmat turi: YouTube kanalini tasdiqlash uchun raqam\n"
        "🌍 Davlat: Indonesia 🇮🇩\n"
        "⏱ Amal qilish: 20 daqiqa\n\n"
        "💰 Narx: 30,000 so'm\n\n"
        "⚠️ MUHIM:\n"
        "Bu raqam faqat YouTube kanal verifikatsiyasi uchun.\n"
        "Google account, Gmail yoki boshqa xizmatlar uchun ishlamaydi."
    )
    await message.answer(text, reply_markup=get_main_menu())

async def cmd_about(message: Message):
    text = (
        "🤖 BOT HAQIDA\n\n"
        "Ushbu bot YouTube kanalingizni tasdiqlash uchun maxsus raqamlarni taqdim etadi.\n"
        "Tezkor, ishonchli va qulay xizmat ko'rsatishga harakat qilamiz.\n\n"
        f"👤 Admin: @{ADMIN_USERNAME}"
    )
    await message.answer(text, reply_markup=get_main_menu())

@dp.message(Command("admin"))
async def admin_help(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    
    text = (
        "👑 *Admin qo'llanma*\n\n"
        "📱 Raqam yuborish:\n"
        "`/num USER_ID NOMER`\n"
        "Misol: `/num 7273500546 628123456789`\n\n"
        "🔐 Kod yuborish:\n"
        "`/code USER_ID KOD`\n"
        "Misol: `/code 7273500546 734822`\n\n"
        "📊 Statistika:\n"
        "`/stats` - Kunlik/Haftalik/Oylik\n"
        "`/stats today` - Bugun\n"
        "`/stats week` - 7 kun\n"
        "`/stats month` - 30 kun\n\n"
        "⚠️ Sotuv faqat /code yuborilganda hisoblanadi!"
    )
    await message.answer(text, parse_mode="Markdown")

@dp.message(Command("stats"))
async def cmd_stats(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        args = message.text.split()
        period = args[1] if len(args) > 1 else "all"
        
        if period == "today":
            days = 1
            title = "BUGUNGI STATISTIKA"
        elif period == "week":
            days = 7
            title = "HAFTALIK STATISTIKA (7 kun)"
        elif period == "month":
            days = 30
            title = "OYLIK STATISTIKA (30 kun)"
        else:
            today_stats = get_statistics(1)
            week_stats = get_statistics(7)
            month_stats = get_statistics(30)
            
            report = (
                "📊 *TO'LIQ STATISTIKA*\n"
                f"📅 Sana: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
                
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📈 *BUGUN:*\n"
                f"📱 Sotilgan: *{today_stats['sales']} ta*\n"
                f"💰 Foyda: *{today_stats['profit']:,} so'm*\n\n"
                
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📊 *7 KUN:*\n"
                f"📱 Sotilgan: *{week_stats['sales']} ta*\n"
                f"💵 Foyda: *{week_stats['profit']:,} so'm*\n"
                f"📉 O'rtacha: *{week_stats['sales']//7 if week_stats['sales'] > 0 else 0} ta/kun*\n\n"
                
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📈 *30 KUN:*\n"
                f"📱 Sotilgan: *{month_stats['sales']} ta*\n"
                f"💸 Foyda: *{month_stats['profit']:,} so'm*\n"
                f"📉 O'rtacha: *{month_stats['sales']//30 if month_stats['sales'] > 0 else 0} ta/kun*\n\n"
                
                "━━━━━━━━━━━━━━━━━━━━"
            )
            
            await message.answer(report, parse_mode="Markdown")
            return
        
        stats = get_statistics(days)
        
        report = (
            f"📊 *{title}*\n"
            f"📅 Sana: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
            
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"📱 Sotilgan raqamlar: *{stats['sales']} ta*\n"
            f"💰 Umumiy foyda: *{stats['profit']:,} so'm*\n"
        )
        
        if days > 1:
            avg = stats['sales'] // days if stats['sales'] > 0 else 0
            report += f"📉 O'rtacha: *{avg} ta/kun*\n"
        
        report += "\n━━━━━━━━━━━━━━━━━━━━"
        
        await message.answer(report, parse_mode="Markdown")
        
    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}")

@dp.callback_query(F.data == "buy")
async def buy(callback: CallbackQuery):
    # Ishchi vaqtni tekshirish
    if not is_working_hours():
        now = datetime.now()
        await callback.message.answer(
            f"🕐 ISHCHI VAQT: 09:00 - 23:00\n\n"
            f"⏰ Hozirgi vaqt: {now.strftime('%H:%M')}\n\n"
            f"Afsuski, hozir ish vaqti emas.\n"
            f"To'lov faqat ish vaqtida qabul qilinadi.\n\n"
            f"Iltimos, bugun 09:00 dan 23:00 gacha qayta urinib ko'ring.\n\n"
            f"💬 Savol: @{ADMIN_USERNAME}",
            reply_markup=get_main_menu()
        )
        await callback.answer()
        return
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Chek yubordim", callback_data="sent")]
    ])
    
    await callback.message.answer(
        "💳 To'lov: *30,000 so'm*\n\n"
        "💰 Karta: `9860 3501 4386 4253`\n"
        "👤 Ism: *SARVAR ABDRAHMONOV*\n\n"
        "📌 Karta raqamini ustiga bosib osongina nusxa olishingiz mumkin.\n\n"
        "✅ To'lovdan keyin pastdagi tugmani bosing:",
        reply_markup=kb,
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "sent")
async def sent(callback: CallbackQuery):
    user = callback.from_user
    user_id = user.id
    
    AWAITING_CHECK.add(user_id)
    
    await bot.send_message(
        ADMIN_ID,
        "💰 *Foydalanuvchi to'lov qilganini bildirdi!*\n\n"
        f"👤 Foydalanuvchi: {user.full_name}\n"
        f"🆔 ID: `{user.id}`\n"
        f"Username: @{user.username or 'yoq'}\n\n"
        "📷 Endi u chek skrinshotini yuborishi kerak.",
        parse_mode="Markdown"
    )
    
    await callback.message.answer(
        "📷 Iltimos, to'lov chek skrinshotini *rasm (photo)* sifatida yuboring.\n\n"
        "Diqqat: faqat rasm qabul qilinadi, fayl yoki video emas.",
        parse_mode="Markdown",
        reply_markup=get_main_menu()
    )
    await callback.answer()

@dp.message(F.content_type == ContentType.PHOTO)
async def handle_check_photo(message: Message):
    user = message.from_user
    user_id = user.id
    file_id = message.photo[-1].file_id
    caption = message.caption or ""
    
    expected = user_id in AWAITING_CHECK
    duplicate = file_id in USED_CHECK_PHOTOS and USED_CHECK_PHOTOS[file_id] != user_id
    
    entry = {
        "time": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "username": user.username,
        "full_name": user.full_name,
        "file_id": file_id,
        "caption": caption,
        "expected": expected,
        "duplicate": duplicate,
    }
    log_payment_entry(entry)
    
    USED_CHECK_PHOTOS[file_id] = user_id
    
    if not expected:
        await message.reply(
            "⚠️ Iltimos, avval botdagi *\"📲 Raqam olish\" → \"📲 Sotib olish\" → \"✅ Chek yubordim\"* "
            "tugmalari orqali boshlang, so'ng chek rasmini yuboring.",
            parse_mode="Markdown",
            reply_markup=get_main_menu()
        )
    else:
        AWAITING_CHECK.discard(user_id)
    
    admin_caption = (
        "📥 *Yangi chek skrinshoti!*\n\n"
        f"👤 Ism: {user.full_name}\n"
        f"🆔 ID: `{user_id}`\n"
        f"Username: @{user.username or 'yoq'}\n"
        f"💰 Summa: 30,000 so'm\n\n"
    )
    
    if duplicate:
        admin_caption += "⚠️ *DIQQAT!* Bu rasm avval boshqa hisobdan ham yuborilgan. Shubhali!\n\n"
    
    admin_caption += (
        "📌 Raqam yuborish uchun:\n"
        f"`/num {user_id} XXXXXXXXXXX`\n\n"
        "Chek izohi: " + (caption if caption else "—")
    )
    
    try:
        await bot.send_photo(
            ADMIN_ID,
            file_id,
            caption=admin_caption,
            parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"Failed to send check to admin: {e}")
    
    if duplicate:
        await message.reply(
            "✅ Chek qabul qilindi.\n"
            "⚠️ Diqqat: bu chek qo'shimcha tekshiruvdan o'tadi. Iltimos, admingiz javobini kuting.",
            reply_markup=get_main_menu()
        )
    else:
        await message.reply(
            "✅ Chek skrinshoti qabul qilindi.\n"
            "Tez orada raqam yuboraman, iltimos kuting.",
            reply_markup=get_main_menu()
        )

@dp.message(Command("num"))
async def send_number(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split(maxsplit=2)
        if len(parts) != 3:
            raise ValueError("Invalid format")
        
        _, user_id_str, phone = parts
        user_id = int(user_id_str)
    except Exception:
        await message.answer(
            "❌ To'g'ri format:\n"
            "`/num USER_ID NOMER`\n\n"
            "Misol:\n"
            "`/num 7273500546 628123456789`",
            parse_mode="Markdown"
        )
        return
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔐 Kod yubordim", callback_data="wait_code")]
    ])
    
    try:
        await bot.send_message(
            user_id,
            f"📱 Sizning Indonesia raqamingiz:\n`{phone}`\n\n"
            "✅ Keyingi qadamlar:\n"
            "1️⃣ YouTube'da Indonesia davlatini tanlang\n"
            "2️⃣ Shu raqamni kiriting\n"
            "3️⃣ Kod kelgach, pastdagi tugmani bosing\n\n"
            "⏱ Raqam 20 daqiqa amal qiladi.\n"
            "Odatda 5-10 daqiqa yetadi ✅\n\n"
            "Tayyor bo'lganingizda:",
            parse_mode="Markdown",
            reply_markup=kb
        )
        
        PENDING_NUMBERS[user_id] = phone
        
        await message.answer(f"✅ Raqam foydalanuvchi {user_id} ga yuborildi.")
        asyncio.create_task(number_expire_timer(user_id))
        
    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}")

@dp.callback_query(F.data == "wait_code")
async def wait_code(callback: CallbackQuery):
    user = callback.from_user
    
    await callback.message.answer(
        "⌛ Tasdiqlash kodi olinmoqda, hozir sizga yuboraman.",
        reply_markup=get_main_menu()
    )
    
    await bot.send_message(
        ADMIN_ID,
        "🔔 *\"Kod yubordim\" tugmasi bosildi!*\n"
        f"👤 Ism: {user.full_name}\n"
        f"🆔 ID: `{user.id}`\n"
        f"Username: @{user.username or 'yoq'}\n\n"
        f"Tasdiqlash kodi kelgach, quyidagicha yuboring:\n"
        f"`/code {user.id} XXXXXX`",
        parse_mode="Markdown"
    )
    
    await callback.answer()

@dp.message(Command("code"))
async def send_code(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = message.text.split(maxsplit=2)
        if len(parts) != 3:
            raise ValueError("Invalid format")
        
        _, user_id_str, code = parts
        user_id = int(user_id_str)
    except Exception:
        await message.answer(
            "❌ To'g'ri format:\n"
            "`/code USER_ID KOD`\n\n"
            "Misol:\n"
            "`/code 7273500546 734822`",
            parse_mode="Markdown"
        )
        return
    
    try:
        await bot.send_message(
            user_id,
            f"🔐 *Sizning YouTube tasdiqlash kodingiz:* `{code}`",
            parse_mode="Markdown"
        )
        
        await bot.send_message(
            user_id,
            "✅ *Kodingiz muvaffaqiyatli yuborildi!*\n\n"
            "🔔 Iltimos, kodingizni YouTube'ga kiriting va kanalingizni tasdiqlab oling.\n\n"
            "🎉 Bizning xizmatimizdan foydalanganingiz uchun katta rahmat!\n"
            "🚀 YouTube faoliyatingizga omad tilaymiz!\n\n"
            "🤝 Yana sizni kutamiz!",
            parse_mode="Markdown"
        )
        
        if user_id in PENDING_NUMBERS:
            phone = PENDING_NUMBERS[user_id]
            log_sale_entry(user_id, phone)
            del PENDING_NUMBERS[user_id]
            logging.info(f"✅ SOTUV YAKUNLANDI: {user_id} - {phone}")
        else:
            log_sale_entry(user_id, "UNKNOWN")
            logging.warning(f"⚠️ Raqam topilmadi, lekin kod yuborildi: {user_id}")
        
        await message.answer(f"✅ Kod foydalanuvchi {user_id} ga yuborildi.\n💰 Sotuv hisobga olindi!")
        
    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}")

@dp.message()
async def handle_all_messages(message: Message):
    """BITTA handler - hamma narsani boshqaradi"""
    text = message.text or ""
    
    # Debug
    logging.info(f"📨 Xabar keldi: [{text}]")
    
    # Commands
    if text.startswith("/start"):
        await start(message)
        return
    
    if text.startswith("/help"):
        await cmd_help(message)
        return
    
    if text.startswith("/info"):
        await cmd_info(message)
        return
    
    if text.startswith("/about"):
        await cmd_about(message)
        return
    
    if text.startswith("/admin"):
        if message.from_user.id == ADMIN_ID:
            await admin_help(message)
        return
    
    if text.startswith("/stats"):
        if message.from_user.id == ADMIN_ID:
            await cmd_stats(message)
        return
    
    if text.startswith("/num"):
        if message.from_user.id == ADMIN_ID:
            await send_number(message)
        return
    
    if text.startswith("/code"):
        if message.from_user.id == ADMIN_ID:
            await send_code(message)
        return
    
    if text.startswith("/"):
        await message.reply(
            "❌ Bu komanda mavjud emas.\n\n"
            "/start ni bosing yoki menyudagi tugmalardan foydalaning.",
            reply_markup=get_main_menu()
        )
        return
    
    # Button handlers
    logging.info(f"📨 KELDI: [{text}]")
    
    # Emoji'larni olib tashlash
    text_clean = text.replace("🛠", "").replace("👤", "").replace("📲", "").replace("💰", "").replace("✅", "").strip()
    logging.info(f"🧹 Tozalangan: [{text_clean}]")
    
    # YORDAM
    if text_clean == "Yordam":
        logging.info("🎯 YORDAM ISHLADI!")
        await menu_help(message)
        return
    
    # ADMIN
    if text_clean == "Admin bilan aloqa":
        logging.info("🎯 ADMIN ISHLADI!")
        await menu_contact_admin(message)
        return
    
    # Boshqa tugmalar
    if "Raqam" in text:
        logging.info("✅ Raqam olish")
        await menu_buy(message)
        return
    
    if "Narx" in text:
        logging.info("✅ Narxlar")
        await menu_prices(message)
        return
    
    if "Qanday" in text:
        logging.info("✅ Qanday ishlaydi")
        await menu_how_it_works(message)
        return
    
    # Unknown
    logging.warning(f"❓ Noma'lum xabar: [{text}]")
    await message.reply(
        "🤔 Kechirasiz, tushunmadim.\n\n"
        "Iltimos, /start bosing va menyudagi tugmalardan foydalaning:",
        reply_markup=get_main_menu()
    )

# Keep the original handlers but they won't be called since catch-all is first

# ========= HTTP SERVER (RENDER UCHUN) =========
from aiohttp import web

async def health_check(request):
    """HTTP health check endpoint - Render uchun"""
    return web.Response(text="✅ Bot ishlayapti!")

async def start_http_server():
    """HTTP server ishga tushirish - Render 'Web Service' uchun kerak"""
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv('PORT', 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"✅ HTTP server started on port {port}")

async def main():
    if TOKEN == "BURGA_BOTFATHER_DAN_OLINGAN_TOKEN_NI_JOYLANG" or len(TOKEN) < 20:
        print("=" * 60)
        print("❌ XATOLIK: BOT TOKEN O'RNATILMAGAN!")
        print("=" * 60)
        print()
        print("Iltimos, bot.py faylini oching va 14-qatorni o'zgartiring:")
        print('TOKEN = "SIZNING_HAQIQIY_TOKENINGIZ"')
        print()
        print("Token olish:")
        print("1. Telegram'da @BotFather ga boring")
        print("2. /newbot yoki /mybots yuboring")
        print("3. Token ni nusxalang")
        print("=" * 60)
        input("\nPress Enter to exit...")
        return
    
    if ADMIN_ID == 123456789:
        print("=" * 60)
        print("⚠️ OGOHLANTIRISH: ADMIN_ID O'ZGARTIRILMAGAN!")
        print("=" * 60)
        print()
        print("Iltimos, bot.py faylini oching va 18-qatorni o'zgartiring:")
        print("ADMIN_ID = SIZNING_ID_RAQAMINGIZ")
        print()
        print("ID olish:")
        print("1. Telegram'da @userinfobot ga boring")
        print("2. /start bosing")
        print("3. ID raqamni nusxalang")
        print("=" * 60)
        print()
        print("Davom etish uchun Enter bosing (test rejimida)...")
        input()
    
    print("=" * 60)
    print("✅ BOT ISHGA TUSHMOQDA...")
    print("=" * 60)
    print()
    print(f"👤 Admin ID: {ADMIN_ID}")
    print(f"💰 Narx: {PRICE:,} so'm")
    print(f"🌐 Davlat: Indonesia 🇮🇩")
    print(f"📝 Admin: @{ADMIN_USERNAME}")
    print(f"📊 Kunlik hisobot: {DAILY_REPORT_TIME}")
    print()
    print("Bot ishlayapti! To'xtatish uchun Ctrl+C bosing.")
    print("=" * 60)
    print()
    
    # HTTP server ishga tushirish (Render uchun)
    asyncio.create_task(start_http_server())
    
    # Hisobotlarni ishga tushirish
    asyncio.create_task(schedule_daily_reports())
    asyncio.create_task(schedule_monthly_reports())
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n✅ Bot to'xtatildi.")
    except Exception as e:
        print(f"\n\n❌ Xatolik: {e}")
        input("\nPress Enter to exit...")
