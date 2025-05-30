#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import os
from datetime import datetime
import logging

# ุฅุนุฏุงุฏ ุงูุณุฌูุงุช
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RDOChallengesBot:
    def __init__(self):
        self.api_url = "https://api.rdo.gg/challenges/index.json"

        # ูุงู…ูุณ ุชุฑุฌู…ุฉ ุงูุชุญุฏูุงุช ุจุงูุนุงู…ูุฉ
        self.challenge_translations = {
            # ุชุญุฏูุงุช ุตุงุฆุฏ ุงูุฌูุงุฆุฒ
            'MPRC_BOUNTY_COMPLETED_POSSE_MEMBER': 'ุงูู…ู ู…ูู…ุฉ ุตุงุฆุฏ ุฌูุงุฆุฒ ู…ุน ุงูุดูุฉ',
            'MPRC_BOUNTY_LOCATION_LEMOYNE': 'ุงูู…ู ู…ูู…ุฉ ุตุงุฆุฏ ุฌูุงุฆุฒ ูู ููู…ููู',
            'MPRC_BOUNTY_TARGET_PHOTOGRAPHED_ALIVE': 'ุตูุฑ ุงูู…ุทููุจ ููู ุญู',

            # ุชุญุฏูุงุช ุงูุชุงุฌุฑ
            'MPRC_TRADER_SUPPLIES_DONATED': 'ุชุจุฑุน ุจุฃุดูุงุก ููุชุงุฌุฑ',
            'MPRC_TRADER_SOLD_CARCASS_TIMED': 'ุจุน ุฌุซุซ ุญููุงูุงุช ููุชุงุฌุฑ',
            'MPRC_TRADER_STEW_EATEN': 'ูู ุดูุฑุจุฉ ู…ู ู…ุฎูู… ุงูุชุงุฌุฑ',

            # ุชุญุฏูุงุช ุงูููููุชุฑ
            'MPRC_COLLECTOR_ANTIQUE_BOTTLES_FOUND': 'ูุงูู ูุฒุงูุฒ ูุฏูู…ุฉ',
            'MPRC_COLLECTOR_FAMILY_HEIRLOOMS_FOUND': 'ูุงูู ุชุญู ุนุงุฆููุฉ',
            'MPRC_COLLECTOR_WILD_FLOWERS_FOUND': 'ูุงูู ูุฑูุฏ ุจุฑูุฉ',

            # ุชุญุฏูุงุช ุงูู…ููุดุงูู
            'MPRC_MOONSHINER_BAR_CHANGED_DECOR': 'ุบูุฑ ุฏูููุฑ ุงูุจุงุฑ',
            'MPRC_MOONSHINER_MARKETING_MISSION_COMPLETED': 'ุงูู…ู ู…ูู…ุฉ ุฏุนุงูุฉ ููู…ูุทุฑ',
            'MPRC_MOONSHINER_MOONSHINE_SERVED_BAR': 'ูุฏู… ุฎู…ุฑุฉ ูู ุงูุจุงุฑ',
            'MPRC_MOONSHINER_MOONSHINE_DRANK_EASY': 'ุงุดุฑุจ ุฎู…ุฑุฉ ูู ุงูุจุงุฑ',

            # ุชุญุฏูุงุช ุนุงูู… ุงูุทุจูุนุฉ
            'MPRC_NATURALIST_CRAFTED_COOKED_WILDERNESS_CAMP': 'ุงุทุจุฎ ูู ู…ุฎูู… ุงูุจุฑูุฉ',
            'MPRC_NATURALIST_USED_HARDY_TONIC': 'ุงุณุชุนู…ู ู…ูุดุท ุงูููุฉ',
            'MPRC_NATURALIST_USED_LEGENDARY_BAIT': 'ุงุณุชุนู…ู ุทุนู… ุฃุณุทูุฑู',
            'MPRC_NATURALIST_DONT_KILL_ANIMALS_EASY': 'ู…ุง ุชูุชู ุญููุงูุงุช (ุงุณุชุนู…ู ุงูู…ุฎุฏุฑ)',
            'MPRC_NATURALIST_CRAFTED_BLENDING_TONIC': 'ุงุตูุน ู…ูุดุท ุงูุชุฎูู',
            'MPRC_NATURALIST_PHOTO_ANIMAL_LEGENDARY': 'ุตูุฑ ุญููุงู ุฃุณุทูุฑู',

            # ุงูุชุญุฏูุงุช ุงูุนุงู…ุฉ
            'MPGC_ARMADILLO_SKINNED': 'ุงุณูุฎ ู…ุฏุฑุน',
            'MPGC_SHEEP_SKINNED': 'ุงุณูุฎ ุฎุฑูู',
            'MPGC_CRAFT_FOOD': 'ุงุตูุน ุฃูู',
            'MPGC_FME_WINS': 'ุงุฑุจุญ ูู ุงูุฃุญุฏุงุซ ุงูุญุฑุฉ',
            'MPGC_OREGANO_PICKED': 'ุงุฌู…ุน ุฃูุฑูุฌุงูู',
            'MPGC_PLAYERS_KILLED_PV_TIMER': 'ุงูุชู ูุงุนุจูู ูู ู…ุนุงุฑู ุงูุดูู',
            'MPGC_RACE_WINS': 'ุงุฑุจุญ ุณุจุงู',
            'MPGC_LEGENDARY_ANIMALS_SKINNED': 'ุงุณูุฎ ุญููุงูุงุช ุฃุณุทูุฑูุฉ',
            'MPGC_COLLECTIBLES_FOUND': 'ูุงูู ุฃุดูุงุก ูุงุฏุฑุฉ',
            'MPGC_FISH_CAUGHT': 'ุงุตุทุงุฏ ุณู…ู',
            'MPGC_HERBS_PICKED': 'ุงุฌู…ุน ุฃุนุดุงุจ',
            'MPGC_BIRDS_SHOT': 'ุงูุชู ุทููุฑ',
            'MPGC_DISTANCE_TRAVELLED_HORSE': 'ุงุทูุน ู…ุณุงูุฉ ุนูู ุงูุญุตุงู',
            'MPGC_CAMP_CRAFTING': 'ุงุตูุน ุดู ูู ุงูู…ุฎูู…',
            'MPGC_EMOTES_USED': 'ุงุณุชุนู…ู ุญุฑูุงุช'
        }

    def get_challenges(self):
        """ุฌูุจ ุฌู…ูุน ุงูุชุญุฏูุงุช ู…ู API"""
        try:
            logger.info("ุฌุงุฑู ุฌูุจ ุงูุชุญุฏูุงุช ู…ู RDO API...")
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            data = response.json()

            general_count = len(data.get('general', []))
            easy_count = sum(len(v) for v in data.get('easy', {}).values())
            logger.info(f"ุชู… ุฌูุจ {general_count} ุชุญุฏู ุนุงู… ู {easy_count} ุชุญุฏู ููุฃุฏูุงุฑ")
            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"ุฎุทุฃ ูู ุฌูุจ ุงูุจูุงูุงุช: {e}")
            return None
        except Exception as e:
            logger.error(f"ุฎุทุฃ ุบูุฑ ู…ุชููุน: {e}")
            return None

    def translate_challenge(self, challenge):
        """ุชุฑุฌู…ุฉ ุชุญุฏู ูุงุญุฏ"""
        title_code = challenge.get('title', '')
        goal = challenge.get('goal', 1)

        # ุงุณุชุฎุฏุงู… ุงูุชุฑุฌู…ุฉ ุงูู…ุญููุธุฉ
        if title_code in self.challenge_translations:
            arabic_title = self.challenge_translations[title_code]
        else:
            # ุฅุฐุง ู…ุง ูุงู ูู ุงููุงู…ูุณุ ุงุณุชุฎุฏู… ุงุณู… ุจุณูุท
            arabic_title = f"ุชุญุฏู: {title_code.replace('MPGC_', '').replace('MPRC_', '').replace('_', ' ')}"

        # ุฅุถุงูุฉ ุงููุฏู
        if goal > 1:
            description = f"ุงููุฏู: {goal} ู…ุฑุงุช"
        else:
            description = "ุงููุฏู: ู…ุฑุฉ ูุงุญุฏุฉ"

        return {
            'title': arabic_title,
            'description': description,
            'goal': goal,
            'original': title_code
        }

    def create_discord_message(self, all_challenges_data):
        """ุฅูุดุงุก ุฑุณุงูุฉ Discord ู…ุน ุฌู…ูุน ุงูุชุญุฏูุงุช"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Embed ููุชุญุฏูุงุช ุงูุนุงู…ุฉ
        general_embed = {
            "title": "๐ฎ ุงูุชุญุฏูุงุช ุงูุนุงู…ุฉ",
            "description": f"ุชุญุฏูุงุช ุนุงู…ุฉ ูุฌู…ูุน ุงููุงุนุจูู\n๐“… {current_time}",
            "color": 0x6c757d,  # ุฑู…ุงุฏู
            "fields": []
        }

        # ุงูุชุญุฏูุงุช ุงูุนุงู…ุฉ
        general_challenges = all_challenges_data.get('general', [])
        for i, challenge in enumerate(general_challenges[:5], 1):
            translated = self.translate_challenge(challenge)
            general_embed["fields"].append({
                "name": f"#{i} {translated['title']}",
                "value": f"{translated['description']}",
                "inline": True
            })

        # Embed ูุชุญุฏูุงุช ุงูุฃุฏูุงุฑ
        roles_embed = {
            "title": "๐‘ค ุชุญุฏูุงุช ุงูุฃุฏูุงุฑ",
            "description": "ุชุญุฏูุงุช ุฎุงุตุฉ ุจูู ุฏูุฑ",
            "color": 0xD2691E,  # ุจูู
            "fields": []
        }

        # ุฃุณู…ุงุก ุงูุฃุฏูุงุฑ ุจุงูุนุฑุจูุฉ
        role_names = {
            'bounty_hunter': '๐ฏ ุตุงุฆุฏ ุงูุฌูุงุฆุฒ',
            'trader': '๐“ฆ ุงูุชุงุฌุฑ',
            'collector': '๐’ ููููุชุฑ',
            'moonshiner': '๐ฅ ู…ููุดุงูู',
            'naturalist': '๐ฟ ุนุงูู… ุงูุทุจูุนุฉ'
        }

        # ุฅุถุงูุฉ ุชุญุฏูุงุช ูู ุฏูุฑ
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
                    "value": challenges_text if challenges_text else "ูุง ุชูุฌุฏ ุชุญุฏูุงุช",
                    "inline": True
                })

        return {"embeds": [general_embed, roles_embed]}

    def send_to_discord(self, webhook_url, message_data):
        """ุฅุฑุณุงู ุงูุฑุณุงูุฉ ุฅูู Discord"""
        try:
            logger.info("ุฌุงุฑู ุฅุฑุณุงู ุงูุฑุณุงูุฉ ุฅูู Discord...")
            response = requests.post(webhook_url, json=message_data)
            response.raise_for_status()
            logger.info("โ… ุชู… ุฅุฑุณุงู ุงูุฑุณุงูุฉ ุจูุฌุงุญ!")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"ุฎุทุฃ ูู ุฅุฑุณุงู ุงูุฑุณุงูุฉ: {e}")
            return False

    def send_daily_challenges(self, webhook_url):
        """ุฅุฑุณุงู ุงูุชุญุฏูุงุช ุงูููู…ูุฉ"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{current_time}] ๐” ุจุฏุก ุฅุฑุณุงู ุงูุชุญุฏูุงุช ุงูููู…ูุฉ...")

        # ุฌูุจ ุฌู…ูุน ุงูุชุญุฏูุงุช
        all_challenges_data = self.get_challenges()
        if not all_challenges_data:
            print("โ ูุดู ูู ุฌูุจ ุงูุชุญุฏูุงุช")
            return False

        # ุฅูุดุงุก ุฑุณุงูุฉ Discord ู…ุน ุฌู…ูุน ุงูุชุญุฏูุงุช
        discord_message = self.create_discord_message(all_challenges_data)

        # ุฅุฑุณุงู ุฅูู Discord
        success = self.send_to_discord(webhook_url, discord_message)

        if success:
            print(f"โ… ุชู… ุฅุฑุณุงู ุฌู…ูุน ุงูุชุญุฏูุงุช ุจูุฌุงุญ ูู {current_time}")
            return True
        else:
            print(f"โ ูุดู ูู ุฅุฑุณุงู ุงูุชุญุฏูุงุช ูู {current_time}")
            return False

def main():
    """ุงูุฏุงูุฉ ุงูุฑุฆูุณูุฉ ููุชุดุบูู ูู GitHub Actions"""
    print("๐€ ุจุฏุก ุชุดุบูู ุจูุช ุชุญุฏูุงุช Red Dead Online")
    print("๐”— ูุดุชุบู ุนุจุฑ GitHub Actions")
    print("=" * 60)
    
    # ุฌูุจ Discord webhook URL ู…ู environment variables
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    
    if not webhook_url:
        print("โ ุฎุทุฃ: DISCORD_WEBHOOK_URL ุบูุฑ ู…ูุฌูุฏ ูู ุงูู…ุชุบูุฑุงุช")
        print("ุชุฃูุฏ ู…ู ุฅุถุงูุฉ Discord webhook URL ูู GitHub Secrets")
        return False
    
    # ุฅูุดุงุก ุงูุจูุช ูุฅุฑุณุงู ุงูุชุญุฏูุงุช
    bot = RDOChallengesBot()
    success = bot.send_daily_challenges(webhook_url)
    
    if success:
        print("๐ ุชู… ุชุดุบูู ุงูุจูุช ุจูุฌุงุญ!")
        return True
    else:
        print("๐’ฅ ูุดู ูู ุชุดุบูู ุงูุจูุช")
        return False

if __name__ == "__main__":
    main()
