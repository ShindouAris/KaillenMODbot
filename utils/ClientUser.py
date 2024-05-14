from __future__ import annotations


import aiohttp
import disnake
from disnake.ext import commands
from utils.server.server import Server

class ClientUser(commands.AutoShardedBot):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serverdb = Server()
        
        
    async def on_ready(self):   
        self.db = await self.serverdb.connect()