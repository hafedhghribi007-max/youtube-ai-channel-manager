#!/usr/bin/env python3
"""
README - YouTube AI Channel Manager
دليل استخدام مدير القناة الذكي
"""

# YouTube AI Channel Manager
# مدير قناة يوتيوب بالذكاء الاصطناعي

## 📺 نظرة عامة
تطبيق شامل لإدارة قنوات YouTube باستخدام الذكاء الاصطناعي، مع واجهة ويب وبوتات تفاعلية.

## ✨ المميزات الرئيسية

### 1. 💻 لوحة التحكم الويب
- واجهة تفاعلية جميلة
- إحصائيات فورية للقناة
- توليد محتوى ذكي
- جدولة التحميلات

### 2. 🤖 بوت Discord
- إدارة القناة عبر Discord
- أوامر سهلة الاستخدام
- إحصائيات فورية
- توليد أفكار فيديو

### 3. 📱 بوت Telegram
- إدارة القناة عبر Telegram
- واجهة بسيطة وسهلة
- إشعارات فورية
- دعم اللغة العربية

## 🚀 البدء السريع

### المتطلبات
```bash
Python 3.8+
Flask
discord.py (اختياري)
python-telegram-bot (اختياري)
```

### التثبيت
```bash
# استنساخ المستودع
git clone https://github.com/hafedhghribi007-max/youtube-ai-channel-manager.git
cd youtube-ai-channel-manager

# إنشاء بيئة افتراضية
python -m venv venv

# تفعيل البيئة الافتراضية
# على Windows:
venv\Scripts\activate
# على Linux/Mac:
source venv/bin/activate

# تثبيت المتطلبات
pip install -r requirements.txt
```

### التكوين
إنشاء ملف `.env`:
```
DISCORD_BOT_TOKEN=your_discord_token
DISCORD_GUILD_ID=your_guild_id
DISCORD_CHANNEL_ID=your_channel_id
TELEGRAM_BOT_TOKEN=your_telegram_token
DATABASE_URL=sqlite:///app.db
```

### التشغيل
```bash
python app_launcher.py
```

الآن يمكنك الوصول إلى:
- 💻 لوحة التحكم: http://localhost:5000
- 🤖 Discord Bot: (عند تفعيله)
- 📱 Telegram Bot: (عند تفعيله)

## 📁 هيكل المشروع
```
youtube-ai-channel-manager/
├── dashboard.py           # لوحة التحكم الويب
├── discord_bot.py         # بوت Discord
├── telegram_bot.py        # بوت Telegram
├── app_launcher.py        # مشغل التطبيق
├── modules/              # وحدات إضافية
├── config.py             # ملف التكوين
├── requirements.txt      # المتطلبات
└── README.md            # هذا الملف
```

## 🎮 أوامر Discord

```
!generate [topic]  - توليد فكرة فيديو جديدة
!stats             - عرض إحصائيات القناة
!help              - عرض المساعدة
```

## 🎮 أوامر Telegram

```
/start             - البدء مع البوت
/generate          - توليد فكرة فيديو
/stats             - عرض الإحصائيات
/upload            - جدولة التحميل
/help              - عرض المساعدة
```

## 📊 الإحصائيات

يتم جمع وعرض:
- 📺 عدد المشاهدات
- 👍 عدد الإعجابات
- 💬 عدد التعليقات
- 👥 عدد المشتركين
- 💰 الأرباح الشهرية
- 🔥 معدل النمو

## 🔒 الأمان
- جميع البيانات محمية
- استخدام متغيرات البيئة للرموز السرية
- عدم حفظ البيانات الحساسة في الكود

## 📝 المساهمة
نرحب بالمساهمات! يرجى:
1. عمل Fork للمستودع
2. إنشاء فرع للميزة الجديدة
3. إرسال Pull Request

## 📄 الترخيص
هذا المشروع مرخص تحت MIT License

## 📞 التواصل
- البريد الإلكتروني: hafedhghribi007@yahoo.fr
- GitHub: [@hafedhghribi007-max](https://github.com/hafedhghribi007-max)

## 🙏 شكر خاص
شكراً لاستخدامك YouTube AI Channel Manager!

---

**ملاحظة:** هذا المشروع لا يزال في مرحلة التطوير. قد تحدث تغييرات كبيرة.

---

آخر تحديث: 2026-09-08
الإصدار: 1.0.0