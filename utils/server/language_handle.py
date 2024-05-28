import os, json
from colorama import Fore, Style
import logging

FORMAT = '%(asctime)s || [%(levelname)s] [%(funcName)s]: %(message)s'
logger = logging.getLogger(__name__)
class LocalizationManager():
    def __init__(self, locale_dir='language'):
        self.locale_dir = locale_dir
        self.localizations = {}
        
    

    def load_localizations(self, silent: bool = False):
        """Tải các dữ liệu bản dịch vào ram"""
        logging.basicConfig(level=logging.INFO, format=FORMAT)
        for root, dirs, files in os.walk(self.locale_dir):
            for filename in files:
                if filename.endswith('.json'):
                    locale = os.path.basename(root)  # Lấy tên thư mục cha làm key (vd: 'en-US', 'vi-VN')
                    with open(os.path.join(root, filename), 'r', encoding='utf-8') as f:
                        self.localizations[locale] = json.load(f)
                        if not silent:
                            logging.info(Fore.GREEN + f"| [ ✅ ] Tải bộ ngôn ngữ {locale} thành công" + Style.RESET_ALL)
                        else: pass
                           

    def get(self, locale, key) -> str:
        """Lấy dữ liệu dịch
        
        
        
        USAGE: get(language, 'some_key')
        """
        return self.localizations.get(locale, {}).get(key, key)
