🎮 بوت تحديات Red Dead Online للديسكورد,
بوت تلقائي يرسل التحديات اليومية للعبة Red Dead Online إلى خادم Discord الخاص بك، يشتغل مجاناً ومدى الحياة عبر GitHub Actions!

✨ المميزات,
🔄 تلقائي تماماً: يشتغل كل يوم بدون تدخل منك,
🆓 مجاني مدى الحياة: يستخدم GitHub Actions المجاني,
🇸🇦 ترجمة عربية: جميع التحديات مترجمة بالعامية,
📱 تنسيق جميل: رسائل Discord منسقة مع ألوان وأيقونات,
⏰ توقيت مضبوط: يرسل التحديات في أوقات تجديدها الفعلية,

🕐 أوقات الإرسال,
6:00 صباحاً UTC: إرسال التحديات الجديدة (وقت التحديث في اللعبة),
6:00 مساءً UTC: إرسال تذكير بالتحديات,

🚀 طريقة التفعيل,
الخطوة 1: إنشاء Discord Webhook,
اذهب لخادم Discord الخاص بك,
اختر القناة اللي تبي البوت يرسل فيها,
اضغط على إعدادات القناة ⚙️,
اختر Integrations > Webhooks,
اضغط Create Webhook,
انسخ Webhook URL (احتفظ فيه، راح تحتاجه),

الخطوة 2: إعداد GitHub Repository,
Fork هذا المشروع أو انسخ الملفات لمشروع جديد,
اذهب لإعدادات المشروع في GitHub,
اختر Settings > Secrets and variables > Actions,
اضغط New repository secret,
اكتب الاسم: DISCORD_WEBHOOK_URL,
الصق الـ Webhook URL اللي نسختوه,
اضغط Add secret,

الخطوة 3: تفعيل GitHub Actions,
اذهب لتبويب Actions في مشروعك,
اضغط I understand my workflows, enable them,
البوت راح يشتغل تلقائياً!,

الخطوة 4: اختبار البوت (اختياري),
لتجربة البوت فوراً بدون انتظار:

اذهب لتبويب Actions,
اختر RDO Daily Challenges Bot,
اضغط Run workflow,
اضغط Run workflow الأخضر,
راح ترسل رسالة للديسكورد خلال دقايق!,

📋 ما يرسله البوت,
التحديات العامة 🎮,
التحديات المتاحة لجميع اللاعبين,
مترجمة بالعامية السعودية,
تظهر الهدف المطلوب (كم مرة),

تحديات الأدوار 👤,
🎯 صائد الجوائز: مهام صيد المطلوبين,
📦 التاجر: مهام التجارة والصيد,
💎 كولكتر: جمع المقتنيات والنوادر,
**🥃 مون,
