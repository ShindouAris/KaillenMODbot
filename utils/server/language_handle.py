import os, json
from colorama import Fore, Style

class LocalizationManager():
    def __init__(self, locale_dir='language'):
        self.locale_dir = locale_dir
        self.localizations = {}

    def load_localizations(self):
        for root, dirs, files in os.walk(self.locale_dir):
            for filename in files:
                if filename.endswith('.json'):
                    locale = os.path.basename(root)  # Lấy tên thư mục cha làm key (vd: 'en-US', 'vi-VN')
                    with open(os.path.join(root, filename), 'r', encoding='utf-8') as f:
                        self.localizations[locale] = json.load(f)
                        print(Fore.GREEN + f"| [ ✅ ] Tải bộ ngôn ngữ {locale} thành công" + Style.RESET_ALL)
                           

    def get(self, locale, key) -> str:
        return self.localizations.get(locale, {}).get(key, key)
