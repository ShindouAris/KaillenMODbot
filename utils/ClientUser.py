from __future__ import annotations

import os
import disnake
from colorama import *
from disnake.ext import commands
from utils.server.server import Server  
from utils.server.language_handle import LocalizationManager
from dotenv import load_dotenv
from utils.server.process_webhook import Process_webhook
import logging

load_dotenv()

FORMAT = '%(asctime)s || [%(levelname)s] [%(funcName)s]: %(message)s'

logger = logging.getLogger(__name__)
class LoadBot:
    
    
    def load(self):
        logging.basicConfig(level=logging.INFO, format=FORMAT)
        logger.info("Booting Client....")
        
        DISCORD_TOKEN = os.environ.get("TOKEN")
        
        
        intents = disnake.Intents()
        intents.voice_states = True
        intents.message_content = True
        intents.guilds = True
        intents.moderation = True
        intents.messages = True
           
        sync_cfg = True
        command_sync_config = commands.CommandSyncFlags(
                            allow_command_deletion=sync_cfg,
                            sync_commands=sync_cfg,
                            sync_commands_debug=sync_cfg,
                            sync_global_commands=sync_cfg,
                            sync_guild_commands=sync_cfg
                        )  
        
        bot  = ClientUser(intents=intents, command_prefix="k!", command_sync_flag=command_sync_config)        
        
        bot.load_modules()
        print("-"*40)
        bot.load_events()
        

        
        try:
            bot.run(DISCORD_TOKEN)
        except Exception as e:
            if  "LoginFailure" in str(e):
                logger.error("An Error occured:", repr(e))

        

class ClientUser(commands.AutoShardedBot):
    
    def __init__(self, *args, intents, command_sync_flag, command_prefix: str, **kwargs) -> None:
        super().__init__(*args, **kwargs, intents=intents, command_sync_flags=command_sync_flag, command_prefix=command_prefix)
        self.uptime = disnake.utils.utcnow()
        self.serverdb = Server()
        self.db =None
        self.handle_language = LocalizationManager()
        self.webhook_utils = Process_webhook()
    
    
    async def on_ready(self):
            print("-"*40)
            logger.info(f"|{Fore.GREEN} Client: {self.user.name} - {self.user.id} Ready{Style.RESET_ALL}")
            await self.process_rpc()
            if not os.environ.get("MONGOSERVER"):
                logger.warning(f"| {Fore.RED}[ ❌ ] [MongoDB] No Database connected, abort")
                return
            await self.serverdb.connect_to_MongoDB()
            self.handle_language.load_localizations()
            print("-"*40)
            
    async def on_resume(self):
        logger.info(f"Client Resumed")
            
    async def process_rpc(self):
        activity = disnake.Activity(
                        type=disnake.ActivityType.watching,
                        name="Guild log",
                    )
        logger.info('Load RPC')
        await ClientUser.change_presence(self, activity=activity)
    

    def load_modules(self):

        modules_dir = "Module"

        load_status = {
            "reloaded": [],
            "loaded": []
        }
        
        for item in os.walk(modules_dir):
            files = filter(lambda f: f.endswith('.py'), item[-1])
            for file in files:
                filename, _ = os.path.splitext(file)
                module_filename = os.path.join(modules_dir, filename).replace('\\', '.').replace('/', '.')
                try:
                    self.reload_extension(module_filename)
                    logger.debug(f'{Fore.GREEN} [ ✅ ] Module {file} Đã tải lên thành công{Style.RESET_ALL}')
                except (commands.ExtensionAlreadyLoaded, commands.ExtensionNotLoaded):
                    self.load_extension(module_filename)
                    logger.debug(f'{Fore.GREEN} [ ✅ ] Module {file} Đã tải lên thành công{Style.RESET_ALL}')
                except Exception as e:
                    logger.error(f"[❌] Đã có lỗi xảy ra với Module {file}: Lỗi: {repr(e)}")
                    continue
                
        return load_status

    
    def load_events(self):

        eventdir =  "Event"

        event_loadstat = {
            "loaded": [],
           "reloaded": []
        }

        for item in os.walk(eventdir):
            files = filter(lambda f: f.endswith('.py'), item[-1])
            for file in files:
                filename, _ = os.path.splitext(file)
                module_filename = os.path.join(eventdir, filename).replace('\\', '.').replace('/', '.')
                try:
                    self.reload_extension(module_filename)
                    logger.debug(f'{Fore.GREEN} [ ✅ ] Event {file} Đã tải lên thành công{Style.RESET_ALL}')
                except (commands.ExtensionAlreadyLoaded, commands.ExtensionNotLoaded):
                    self.load_extension(module_filename)
                    logger.debug(f'{Fore.GREEN} [ ✅ ] Event {file} Đã tải lên thành công{Style.RESET_ALL}')
                except Exception as e:
                    logger.error(f" [❌] Đã có lỗi xảy ra với Event {file}: Lỗi: {repr(e)}")
                    continue
                
        return event_loadstat