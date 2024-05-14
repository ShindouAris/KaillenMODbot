import sqlite3
from colorama import Fore
from dotenv import load_dotenv
from os import environ
from pymongo import MongoClient, errors
from asgiref.sync import sync_to_async as s2a
load_dotenv()
SERVER_URI = environ.get("MONGOSERVER")
class Server():
    def __init__(self):
        self.database = sqlite3.Connection = None
    
        
    async def connect(self, serveruri = SERVER_URI):
        self.client = MongoClient(serveruri)
        self.servers = self.client.db.servers
        self.ignored_roles = self.client.db.ignored_roles
        self.join_channel = self.client.db.join_channel
        self.leave_channel = self.client.db.leave_channel
        self.auto_role = self.client.db.auto_role
        self.is_premium = self.client.db.is_premium
        self.warn_log = self.client.db.warn_log
        self.servercfg = self.client.db.servercfg
        self.id_tk = self.client.db.id_tk
        print(f"{Fore.GREEN}[ ✅ ] [MongoDB] Connected to Server Database")

    async def check_role(self ,guild: int, role_id: int):
        data = await s2a(self.ignored_roles.find_one)({"guild_id": guild, "role_id": role_id})
        if data is None:
            return {
                "info": False,
                "data": "None"
            }
        elif data["role_id"] != role_id:
            return {
                "info": "No",
                "data": "None"
            }
        
        elif data == role_id:
            return {
                "info": True,
                "data": data
            }
        
    async def check_mute(self, role: int, guild: int):
        data_ = await s2a(self.ignored_roles.find)({"guild_id": guild})
        data = [i["role_id"] for i in data_]
        if role in data:
            return {
                "info": True,
                "data": role
            }

        return {
            "info": False,
            "data": "None"
        }
    
    async def check_premium(self, guild: int):
        data = await s2a(self.is_premium.find_one)({"guild_id": guild})
        try:
            if data is None:
                return {
                    "info": False,
                    "data": "None"
                }
            elif data["is_premium"] == 1:
                return {
                    "info": True,
                    "data": data["is_premium"]
                }
            elif data["is_premium"] == 0:
                return {
                    "info": False,
                    "data": data["is_premium"]
                }
        except errors.ServerSelectionTimeoutError as e:
            return {
                "info": False,
                "data": e
            }
        
    async def check_database(self, guild):
        data = await s2a(self.servers.find_one)({"guild_id": guild})
        if not data:
            return {"status": "No_Data"}
        else:
            return {"status": "Data_Found", "channel_id": data["channel_id"]}
        
    async def check_server_db(self, guild_id: int):
        data = await s2a(self.servers.find_one)({"guild_id": guild_id})
        if data is None:
            return False
        else:
            return True
    
    async def get_auto_role(self, guild_id: int):
        data = await s2a(self.auto_role.find_one)({"guild_id": guild_id})
        if data is None:
            return {
                "status": "No_Data"
            }
        else:
            return {
                "status": "Data_Found",
                "role_id": data["role_id"]
            }
        
    async def get_ignored_roles(self, guild_id: int):
        data = await s2a(self.ignored_roles.find)({"guild_id": guild_id})
        if data is None:
            return {
                "status": "No_Data"
            }
        else:
            return {
                "status": "Data_Found",
                "role_id": data["role_id"]
            }
    
    async def get_log_channel(self, guild_id: int):
        data = await s2a(self.servers.find_one)({"guild_id": guild_id})
        if data is None:
            return {
                "status": "No_Data"
            }
        else:
            return {
                "status": "Data_Found",
                "channel_id": data["channel_id"]
            }
        
    async def setupserverlog(self, guild_id: int, channel_id: int):
        data = await s2a(self.servers.find_one)({"guild_id": guild_id})
        if data is None:
            await s2a(self.servers.insert_one)({"guild_id": guild_id, "channel_id": channel_id})
            return {
                "status": "success"
            }
        else:
            return {
                "status": "error"
            }
    
    async def remove_server_log(self, guild_id: int, channel_id: int):
        try:
            await s2a(self.servers.delete_one)({"guild_id": guild_id, "channel_id": channel_id})
            return {
                "status": "success"
            }
        except Exception:
            return {
                "status": "failed"
            }
        
        
    async def setup_ignored_roles(self, guild_id: int, role_id: int):
        data = await s2a(self.ignored_roles.find_one)({"guild_id": guild_id, "role_id": role_id})
        if data is None:
            await s2a(self.ignored_roles.insert_one)({"guild_id": guild_id, "role_id": role_id})
            return {
                "status": "success",
                "action": "insert"
            }
        else:
            await s2a(self.ignored_roles.delete_one)({"guild_id": guild_id, "role_id": role_id})
            return {
                "status": "success",
                "action": "delete"
            }    