> جَ:
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import os
from datetime import datetime
import logging

# إعداد السجلات
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RDOChallengesBot:
    def __init__(self):
        self.api_url = "https://api.rdo.gg/challenges/index.json"

        # قاموس ترجمة التحديات بالعامية
        self.challenge_translations = {
            # تحديات صائد الجوائز
            'MPRC_BOUNTY_COMPLETED_POSSE_MEMBER': 'اكمل مهمة صائد جوائز مع الشلة',
            'MPRC_BOUNTY_LOCATION_LEMOYNE': 'اكمل مهمة صائد جوائز في ليموين',
            'MPRC_BOUNTY_TARGET_PHOTOGRAPHED_ALIVE': 'صور المطلوب وهو حي',

            # تحديات التاجر
            'MPRC_TRADER_SUPPLIES_DONATED': 'تبرع بأشياء للتاجر',
            'MPRC_TRADER_SOLD_CARCASS_TIMED': 'بع جثث حيوانات للتاجر',
            'MPRC_TRADER_STEW_EATEN': 'كل شوربة من مخيم التاجر',

            # تحديات الكولكتر
            'MPRC_COLLECTOR_ANTIQUE_BOTTLES_FOUND': 'لاقي قزايز قديمة',
            'MPRC_COLLECTOR_FAMILY_HEIRLOOMS_FOUND': 'لاقي تحف عائلية',
            'MPRC_COLLECTOR_WILD_FLOWERS_FOUND': 'لاقي ورود برية',

            # تحديات المونشاين
            'MPRC_MOONSHINER_BAR_CHANGED_DECOR': 'غير ديكور البار',
            'MPRC_MOONSHINER_MARKETING_MISSION_COMPLETED': 'اكمل مهمة دعاية للمقطر',
            'MPRC_MOONSHINER_MOONSHINE_SERVED_BAR': 'قدم خمرة في البار',
            'MPRC_MOONSHINER_MOONSHINE_DRANK_EASY': 'اشرب خمرة في البار',

            # تحديات عالم الطبيعة
            'MPRC_NATURALIST_CRAFTED_COOKED_WILDERNESS_CAMP': 'اطبخ في مخيم البرية',
            'MPRC_NATURALIST_USED_HARDY_TONIC': 'استعمل منشط القوة',
            'MPRC_NATURALIST_USED_LEGENDARY_BAIT': 'استعمل طعم أسطوري',
            'MPRC_NATURALIST_DONT_KILL_ANIMALS_EASY': 'ما تقتل حيوانات (استعمل المخدر)',
            'MPRC_NATURALIST_CRAFTED_BLENDING_TONIC': 'اصنع منشط التخفي',
            'MPRC_NATURALIST_PHOTO_ANIMAL_LEGENDARY': 'صور حيوان أسطوري',

            # التحديات العامة
            'MPGC_ARMADILLO_SKINNED': 'اسلخ مدرع',
            'MPGC_SHEEP_SKINNED': 'اسلخ خروف',
            'MPGC_CRAFT_FOOD': 'اصنع أكل',
            'MPGC_FME_WINS': 'اربح في الأحداث الحرة',
            'MPGC_OREGANO_PICKED': 'اجمع أوريجانو',
            'MPGC_PLAYERS_KILLED_PV_TIMER': 'اقتل لاعبين في معارك الشلل',
            'MPGC_RACE_WINS': 'اربح سباق',
            'MPGC_LEGENDARY_ANIMALS_SKINNED': 'اسلخ حيوانات أسطورية',
            'MPGC_COLLECTIBLES_FOUND': 'لاقي أشياء نادرة',
            'MPGC_FISH_CAUGHT': 'اصطاد سمك',
            'MPGC_HERBS_PICKED': 'اجمع أعشاب',
            'MPGC_BIRDS_SHOT': 'اقتل طيور',
            'MPGC_DISTANCE_TRAVELLED_HORSE': 'اطلع مسافة على الحصان',
            'MPGC_CAMP_CRAFTING': 'اصنع شي في المخيم',
            'MPGC_EMOTES_USED': 'استعمل حركات'
        }

    def get_challenges(self):
        """جلب جميع التحديات من API"""
        try:
            logger.info("جاري جلب التحديات من RDO API...")
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            data = response.json()

            general_count = len(data.get('general', []))
            easy_count = sum(len(v) for v in data.get('easy', {}).values())
            logger.info(f"تم جلب {general_count} تحدي عام و {easy_count} تحدي للأدوار")
            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"خطأ في جلب البيانات: {e}")
            return None
        except Exception as e:
            logger.error(f"خطأ غير متوقع: {e}")
            return None

    def translate_challenge(self, challenge):
        """ترجمة تحدي واحد"""
        title_code = challenge.get('title', '')
        goal = challenge.get('goal', 1)

        # استخدام الترجمة المحفوظة
        if title_code in self.challenge_translations:
            arabic_title = self.challenge_translations[title_code]
        else:
            # إذا ما كان في القاموس، استخدم اسم بسيط
            arabic_title = f"تحدي: {title_code.

> جَ:
replace('MPGC_', '').replace('MPRC_', '').replace('_', ' ')}"

        # إضافة الهدف
        if goal > 1:
            description = f"الهدف: {goal} مرات"
        else:
            description = "الهدف: مرة واحدة"

        return {
            'title': arabic_title,
            'description': description,
            'goal': goal,
            'original': title_code
        }

    def create_discord_message(self, all_challenges_data):
        """إنشاء رسالة Discord مع جميع التحديات"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Embed للتحديات العامة
        general_embed = {
            "title": "🎮 التحديات العامة",
            "description": f"تحديات عامة لجميع اللاعبين\n📅 {current_time}",
            "color": 0x6c757d,  # رمادي
            "fields": []
        }

        # التحديات العامة
        general_challenges = all_challenges_data.get('general', [])
        for i, challenge in enumerate(general_challenges[:5], 1):
            translated = self.translate_challenge(challenge)
            general_embed["fields"].append({
                "name": f"#{i} {translated['title']}",
                "value": f"{translated['description']}",
                "inline": True
            })

        # Embed لتحديات الأدوار
        roles_embed = {
            "title": "👤 تحديات الأدوار",
            "description": "تحديات خاصة بكل دور",
            "color": 0xD2691E,  # بني
            "fields": []
        }

        # أسماء الأدوار بالعربية
        role_names = {
            'bounty_hunter': '🎯 صائد الجوائز',
            'trader': '📦 التاجر',
            'collector': '💎 كولكتر',
            'moonshiner': '🥃 مونشاين',
            'naturalist': '🌿 عالم الطبيعة'
        }

        # إضافة تحديات كل دور
        easy_challenges = all_challenges_data.get('easy', {})
        for role_key, role_name in role_names.items():
            role_challenges = easy_challenges.get(role_key, [])
            if role_challenges:
                challenges_text = ""
                for i, challenge in enumerate(role_challenges[:3], 1):
                    translated = self.translate_challenge(challenge)
                    challenges_text += f"{i}. {translated['title']}\n"

                roles_embed["fields"].append({
                    "name": role_name,
                    "value": challenges_text if challenges_text else "لا توجد تحديات",
                    "inline": True
                })

        return {"embeds": [general_embed, roles_embed]}

    def send_to_discord(self, webhook_url, message_data):
        """إرسال الرسالة إلى Discord"""
        try:
            logger.info("جاري إرسال الرسالة إلى Discord...")
            response = requests.post(webhook_url, json=message_data)
            response.raise_for_status()
            logger.info("✅ تم إرسال الرسالة بنجاح!")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"خطأ في إرسال الرسالة: {e}")
            return False

    def send_daily_challenges(self, webhook_url):
        """إرسال التحديات اليومية"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{current_time}] 🔄 بدء إرسال التحديات اليومية...")

        # جلب جميع التحديات
        all_challenges_data = self.get_challenges()
        if not all_challenges_data:
            print("❌ فشل في جلب التحديات")
            return False

        # إنشاء رسالة Discord مع جميع التحديات
        discord_message = self.create_discord_message(all_challenges_data)

        # إرسال إلى Discord
        success = self.send_to_discord(webhook_url, discord_message)

        if success:
            print(f"✅ تم إرسال جميع التحديات بنجاح في {current_time}")
            return True
        else:
            print(f"❌ فشل في إرسال التحديات في {current_time}")
            return False

def main():
    """الدالة الرئيسية للتشغيل في GitHub Actions"""
    print("🚀 بدء تشغيل بوت تحديات Red Dead Online")
    print("🔗 يشتغل عبر GitHub Actions")
    print("=" * 60)

    # جلب Discord webhook URL من environment variables
