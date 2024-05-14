import disnake
from disnake.ext import commands
import os
from dotenv import load_dotenv

intents = disnake.Intents()
intents.voice_states = True
intents.message_content = False
intents.messages = False

load_dotenv()
bot = commands.Bot(intents=intents)

bot.remove_command("help")

DISCORD_TOKEN = os.environ.get("TOKEN")

initial_extensions = "filemodule", "Event"

@bot.event
async def on_ready():
    print(""" 
             ____  _   _ ___ _   _ ____   ___  _   _       ____  _______     __
            / ___|| | | |_ _| \ | |  _ \ / _ \| | | |     |  _ \| ____\ \   / /
            \___ \| |_| || ||  \| | | | | | | | | | |     | | | |  _|  \ \ / / 
             ___) |  _  || || |\  | |_| | |_| | |_| |  _  | |_| | |___  \ V /  
            |____/|_| |_|___|_| \_|____/ \___/ \___/  (_) |____/|_____|  \_/  """)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
    for item in os.walk(initial_extensions):
        files = filter(lambda f: f.endswith('.py'), item[-1])
        for file in files:
            filename, _ = os.path.splitext(file)
            module_filename = os.path.join(initial_extensions, filename).replace('\\', '.').replace('/', '.')
            bot.load_extension(module_filename)
            print(f'Module {file} Đã tải lên thành công')
            
try:
    bot.run(DISCORD_TOKEN)
except Exception as e:
    if  "LoginFailure" in str(e):
        print(f"Đăng nhập thất bại: {repr(e)}")
