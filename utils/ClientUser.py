from __future__ import annotations

import os
from colorama import *
from disnake.ext import commands
from utils.server.server import Server       

class ClientUser(commands.AutoShardedBot):
    
    def __init__(self, *args, intents, command_sync_flag, command_prefix: str, **kwargs) -> None:
        super().__init__(*args, **kwargs, intents=intents, command_sync_flags=command_sync_flag, command_prefix=command_prefix)
        self.serverdb = Server()
        self.db =None
    
    
    # async def on_ready(self):   
    #     self.db = await self.serverdb.connect()
        
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
                self.load_extension(module_filename)
                print(f'Module {file} Đã tải lên thành công')
                
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
                self.load_extension(module_filename)
                print(f'Event {file} Đã tải lên thành công')
                
        return event_loadstat