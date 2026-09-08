# YouTube AI Channel Manager

## 📺 نظام إدارة قناة يوتيوب بالذكاء الاصطناعي

### 🎯 الميزات الرئيسية

- **AI Content Generation**: توليد أفكار ومحتوى فيديو باستخدام OpenAI
- **Automated Video Upload**: تحميل تلقائي للفيديوهات على يوتيوب
- **Video Processing**: معالجة وتحرير الفيديوهات
- **Channel Analytics**: تحليلات شاملة لأداء القناة
- **Database Management**: إدارة قاعدة بيانات المحتوى
- **Schedule Management**: جدولة تحميل الفيديوهات

### 🚀 البدء السريع

#### المتطلبات

```bash
Python 3.8+
FFmpeg (لمعالجة الفيديو)
PostgreSQL أو SQLite
```

#### التثبيت

1. **استنسخ المستودع**

```bash
git clone https://github.com/hafedhghribi007-max/youtube-ai-channel-manager.git
cd youtube-ai-channel-manager
```

2. **ثبت المتطلبات**

```bash
pip install -r requirements.txt
```

3. **إعداد متغيرات البيئة**

```bash
cp .env.example .env
# ثم عدّل .env بمفاتيحك
```

4. **احصل على مفاتيح API**

#### YouTube API

1. اذهب إلى [Google Cloud Console](https://console.cloud.google.com/)
2. أنشئ مشروعاً جديداً
3. فعّل YouTube Data API v3
4. أنشئ OAuth 2.0 credentials (Desktop application)
5. حمّل الملف JSON وسمّه `credentials.json`

#### OpenAI API

1. اذهب إلى [OpenAI Platform](https://platform.openai.com/)
2. أنشئ API key جديد
3. أضفه إلى ملف `.env`

### 📝 أمثلة الاستخدام

#### 1. توليد فكرة فيديو

```python
from modules.ai_content_generator import AIContentGenerator
from config import DevelopmentConfig

config = DevelopmentConfig()
ai_gen = AIContentGenerator(config)

# توليد فكرة عشوائية
idea = ai_gen.generate_video_idea()
print(idea)

# توليد فكرة حول موضوع معين
idea = ai_gen.generate_video_idea(topic="الرياضيات للأطفال")
print(idea)
```

#### 2. توليد سكريبت

```python
video_idea = {
    'content': 'فكرة حول تعليم الأطفال الأرقام'
}

script = ai_gen.generate_script(video_idea)
print(script)
```

#### 3. تحميل فيديو على يوتيوب

```python
from modules.youtube_uploader import YouTubeUploader

config = DevelopmentConfig()
uploader = YouTubeUploader(config)

result = uploader.upload_video(
    video_file='path/to/video.mp4',
    title='تعليم الأطفال الأرقام',
    description='فيديو تعليمي ممتع للأطفال',
    tags=['تعليم', 'أطفال', 'أرقام'],
    category_id='23'  # Shorts
)

print(result)
```

#### 4. معالجة الفيديو

```python
from modules.video_processor import VideoProcessor

config = DevelopmentConfig()
processor = VideoProcessor(config)

# توليد صورة غلاف
thumbnail = processor.generate_thumbnail(
    title='تعليم الأطفال',
    description='فيديو ممتع',
    output_file='thumbnail.png'
)

# تحويل جودة الفيديو
converted = processor.convert_video_format(
    input_file='input.mp4',
    output_file='output.mp4',
    quality='720p'
)
```

#### 5. الحصول على تحليلات القناة

```python
from modules.analytics import AnalyticsManager

config = DevelopmentConfig()
analytics = AnalyticsManager(config)

# احصل على إحصائيات القناة
stats = analytics.get_channel_stats()
print(stats)

# احصل على تحليلات فيديو معين
video_stats = analytics.get_video_analytics('VIDEO_ID')
print(video_stats)
```

#### 6. إدارة قاعدة البيانات

```python
from modules.database import Database

db = Database('postgresql://user:password@localhost/youtube_channel')

# إضافة محتوى جديد
result = db.add_video_content(
    title='تعليم الأطفال',
    description='فيديو تعليمي',
    script='السكريبت هنا',
    topic='التعليم'
)

# الحصول على محتوى
video = db.get_video_by_id(1)
print(video)
```

### 🔄 سير العمل الكامل

```
1. توليد فكرة (AI Content Generator)
   ↓
2. توليد سكريبت (AI Content Generator)
   ↓
3. معالجة الفيديو (Video Processor)
   ↓
4. توليد صورة الغلاف (Video Processor)
   ↓
5. حفظ البيانات في قاعدة البيانات (Database)
   ↓
6. تحميل على يوتيوب (YouTube Uploader)
   ↓
7. تحليل الأداء (Analytics Manager)
```

### 📊 هيكل المشروع

```
youtube-ai-channel-manager/
├── main.py                 # التطبيق الرئيسي
├── config.py               # الإعدادات
├── requirements.txt        # المتطلبات
├── .env.example           # متغيرات البيئة
├── modules/
│   ├── ai_content_generator.py
│   ├── youtube_uploader.py
│   ├── video_processor.py
│   ├── analytics.py
│   ├── database.py
│   └── __init__.py
├── output_videos/         # مجلد الفيديوهات
├── README.md
└── LICENSE
```

### 🔒 الأمان

- لا تشارك مفاتيح API الخاصة بك
- استخدم ملف `.env` لتخزين المفاتيح
- لا تضف `.env` إلى git

### 📜 الترخيص

MIT License - انظر ملف LICENSE

### 🤝 المساهمة

المساهمات مرحب بها! يرجى:

1. Fork المستودع
2. أنشئ فرع للميزة الجديدة
3. أرسل Pull Request

### 📧 الاتصال

للمساعدة والاستفسارات: hafedhghribi007@yahoo.fr

### ⚠️ تنويهات مهمة

1. **محتوى الأطفال**: تأكد من أن جميع المحتوى آمن وملائم للأطفال
2. **الامتثال للقانون**: التزم بسياسات يوتيوب والقوانين المحلية
3. **الخصوصية**: لا تجمع بيانات شخصية الأطفال بدون موافقة الأهل
4. **الجودة**: تأكد من جودة المحتوى قبل النشر

### 🎓 الموارد المفيدة

- [YouTube API Documentation](https://developers.google.com/youtube/v3)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

---

**تم إنشاه هذا المشروع لمساعدتك في إطلاق قناة يوتيوب ناجحة للأطفال! 🚀**