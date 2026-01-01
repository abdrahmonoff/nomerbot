# YOUTUBE VERIFICATION BOT - COMPLETE PACKAGE

Version: 2.0 FINAL
Date: 15.12.2025

## FILES IN THIS PACKAGE:

telegram_bot/
├── bot.py              <- Main bot file
├── start.bat          <- Start bot
├── install.bat        <- Install dependencies
├── stop.bat           <- Stop bot
└── README.txt         <- This file

---

## QUICK START - 3 STEPS:

### STEP 1: GET TOKEN & ID (2 minutes)

**Telegram:**
1. @BotFather -> /newbot -> Copy TOKEN
2. @userinfobot -> /start -> Copy ID

---

### STEP 2: EDIT bot.py (2 minutes)

Open bot.py with Notepad

**Change 3 lines:**

Line 14:
TOKEN = "YOUR_TOKEN_FROM_BOTFATHER"

Line 18:
ADMIN_ID = YOUR_ID_NUMBER

Line 22:
ADMIN_USERNAME = "your_username"

**Save:** Ctrl + S

---

### STEP 3: RUN (1 minute)

1. install.bat -> Double click (first time only)
2. start.bat -> Double click (every time)

**DONE!** Bot is running!

---

## FEATURES:

### For Users:
- Buy USA phone numbers for YouTube verification
- 30,000 som per number
- 20 minute validity
- Beautiful interface with emojis
- Step-by-step guide

### For Admin:
- Send numbers: /num USER_ID +1234567890
- Send codes: /code USER_ID 123456
- View statistics: /stats
- Daily auto-report at 23:00
- Payment tracking
- Duplicate check

### Statistics:
- Daily report (auto at 23:00)
- Manual check anytime: /stats
- Weekly stats: /stats week
- Monthly stats: /stats month
- Sales only counted when CODE is sent!

---

## ADMIN COMMANDS:

/admin - Show admin guide
/num USER_ID PHONE - Send number to user
/code USER_ID CODE - Send code (counts as sale!)
/stats - View all statistics
/stats today - Today only
/stats week - Last 7 days
/stats month - Last 30 days

---

## HOW IT WORKS:

### User Flow:
1. User: /start -> Sees menu
2. User: "Raqam olish" -> Payment info
3. User: Sends payment screenshot
4. Admin: Gets notification

### Admin Flow:
1. Admin: /num USER_ID +1234567890 -> Number sent
2. User: Gets number, uses it on YouTube
3. User: Clicks "Kod yubordim"
4. Admin: /code USER_ID 123456 -> Code sent
5. System: Sale logged! Statistics updated!

---

## STATISTICS:

### Daily Auto Report (23:00):
```
📊 KUNLIK HISOBOT
📅 Sana: 15.12.2025

━━━━━━━━━━━━━━━━━━━━
📈 BUGUN:
📱 Sotilgan raqamlar: 5 ta
💰 Foyda: 150,000 so'm

━━━━━━━━━━━━━━━━━━━━
📊 7 KUN:
📱 Sotilgan: 28 ta
💵 Foyda: 840,000 so'm

━━━━━━━━━━━━━━━━━━━━
📈 30 KUN:
📱 Sotilgan: 95 ta
💸 Foyda: 2,850,000 so'm
```

### Manual Check:
```
/stats
```

Shows today, 7 days, and 30 days stats!

---

## IMPORTANT NOTES:

### Sales Counting:
- ❌ /start pressed -> NOT counted
- ❌ Payment sent -> NOT counted
- ❌ Number sent -> NOT counted
- ✅ CODE sent -> COUNTED AS SALE!

**Why?**
Sale = Code sent = Service completed = Money earned!

### Files Created:
- payments.jsonl - Payment screenshots log
- sales.jsonl - Completed sales log

---

## CONFIGURATION:

### Change Daily Report Time:

Open bot.py, Line 30:
```python
DAILY_REPORT_TIME = "23:00"
```

Change to:
```python
DAILY_REPORT_TIME = "20:00"  # 8 PM
DAILY_REPORT_TIME = "09:00"  # 9 AM
```

### Change Price:

Open bot.py, Line 29:
```python
PRICE = 30000
```

---

## TESTING:

### 1. Start bot:
```
start.bat
```

Terminal shows:
```
✅ BOT ISHGA TUSHMOQDA...
================================================

👤 Admin ID: 987654321
💰 Narx: 30,000 so'm
🌐 Davlat: Amerika Qo'shma Shtatlari 🇺🇸
📊 Kunlik hisobot: 23:00

Bot ishlayapti! To'xtatish uchun Ctrl+C bosing.
```

### 2. Test in Telegram:
```
/start - Shows menu
/admin - Shows admin commands
/stats - Shows statistics (0 at first)
```

### 3. Test sale:
```
/num 123456789 +12025551234
```

Check stats:
```
/stats
```

Result: Still 0 sales (number sent, code not sent yet)

Send code:
```
/code 123456789 123456
```

Bot replies:
```
✅ Kod foydalanuvchi 123456789 ga yuborildi.
💰 Sotuv hisobga olindi!
```

Check stats again:
```
/stats
```

Result: 1 sale, 30,000 so'm profit!

---

## TROUBLESHOOTING:

### "TOKEN is invalid"
Fix: Check line 14 in bot.py

### "python is not recognized"
Fix: Install Python from python.org

### "No module named 'aiogram'"
Fix: Run install.bat

### Admin commands not working
Fix: Check ADMIN_ID in line 18

### Statistics showing 0
- Make sure you sent /code command
- /num alone doesn't count as sale
- Check sales.jsonl file exists

---

## FILE STRUCTURE:

All files must be in same folder:

```
C:\telegram_bot\
├── bot.py         <- Main (edit this)
├── start.bat      <- Run this
├── install.bat    <- First time only
└── stop.bat       <- Stop bot
```

After running, these appear:
```
├── payments.jsonl <- Payment logs
└── sales.jsonl    <- Sales logs
```

---

## TIPS:

### 1. Auto-start on Windows boot:
- Win + R
- Type: shell:startup
- Copy start.bat there

### 2. View sales.jsonl in Excel:
- Open Excel
- Import JSON
- Analyze data

### 3. Backup important files:
- sales.jsonl - All sales
- payments.jsonl - All payments

### 4. 24/7 running:
Use VPS server (DigitalOcean, AWS, etc)

---

## SUPPORT:

Check admin Telegram: @YOUR_USERNAME

---

## CHANGELOG:

### Version 2.0 (FINAL):
- ✅ Amerika -> Amerika Qo'shma Shtatlari
- ✅ Sales counted only when code sent
- ✅ Daily auto-report at 23:00
- ✅ Manual statistics: /stats
- ✅ Clean code, no invisible characters
- ✅ Complete English bat files
- ✅ Professional interface

---

## SUMMARY:

**What you get:**
- Professional YouTube verification bot
- USA phone numbers
- Automatic daily reports
- Real-time statistics
- Payment tracking
- Duplicate detection
- 20-minute timer
- Beautiful interface

**What you need:**
- Windows PC
- Python installed
- Telegram bot token
- 5 minutes setup time

**Result:**
- Automated business
- Daily income reports
- Professional service
- Happy customers

---

GOOD LUCK WITH YOUR BUSINESS! 💰🚀

---

Last updated: 15.12.2025
