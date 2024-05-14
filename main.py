from utils.ClientUser import LoadBot
from colorama import Fore, Style

print(f""" 
      {Fore.RED}       ____  _   _ ___ _   _ ____   ___  _   _       ____  _______     __
      {Fore.GREEN}      / ___|| | | |_ _| \ | |  _ \ / _ \| | | |     |  _ \| ____\ \   / /
      {Fore.YELLOW}      \___ \| |_| || ||  \| | | | | | | | | | |     | | | |  _|  \ \ / / 
      {Fore.GREEN}       ___) |  _  || || |\  | |_| | |_| | |_| |  _  | |_| | |___  \ V /  
      {Fore.CYAN}      |____/|_| |_|___|_| \_|____/ \___/ \___/  (_) |____/|_____|  \_/  {Style.RESET_ALL}""")

bot = LoadBot()

bot.load()