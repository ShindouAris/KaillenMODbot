import disnake
from disnake.ext import commands
import os
from dotenv import load_dotenv
from utils.ClientUser import ClientUser

intents = disnake.Intents()
intents.voice_states = True
intents.message_content = True
intents.guilds = True
intents.moderation = True
intents.messages = True

load_dotenv()

command_sync_config = commands.CommandSyncFlags(
                    allow_command_deletion=True,
                    sync_commands=True,
                    sync_commands_debug=True,
                    sync_global_commands=True,
                    sync_guild_commands=True
                )

bot  = ClientUser(intents=intents, command_prefix="?", command_sync_flag=command_sync_config)

DISCORD_TOKEN = os.environ.get("TOKEN")

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
    
    bot.load_modules()
    bot.load_events()
    await bot.serverdb.connect()
    
try:
    bot.run(DISCORD_TOKEN)
except Exception as e:
    if  "LoginFailure" in str(e):
        print(f"Đăng nhập thất bại: {repr(e)}")
