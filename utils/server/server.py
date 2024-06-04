import sqlite3
from colorama import Fore, Style
from dotenv import load_dotenv
from os import environ
from pymongo import MongoClient
from asgiref.sync import sync_to_async as s2a
import logging
load_dotenv()
SERVER_URI = environ.get("MONGOSERVER")
FORMAT = '%(asctime)s || [%(levelname)s] [%(funcName)s]: %(message)s'
logger = logging.getLogger(__name__)
class Server():
    def __init__(self):
        self.database = sqlite3.Connection = None
    
        
    async def connect_to_MongoDB(self, serveruri = SERVER_URI):
        """Connect to the database, if Aval"""
        logging.basicConfig(level=logging.INFO, format=FORMAT)
        self.client = MongoClient(serveruri)
        self.servers = self.client.db.servers
        self.ignored_roles = self.client.db.ignored_roles
        self.language = self.client.db.language
        logger.info(f"| {Fore.GREEN}[ ✅ ] Connected to Server Database{Style.RESET_ALL}")


    async def guild_language(self, guild_id: int) -> dict:
        data = await s2a(self.language.find_one)({"guild_id": guild_id})
        if data is None:
            return {
                "status": "NoData", "language": "vi"
            }
        else:
            return {"status": "DataFound", "language": data["language"]}
        
    async def func_language(self, guild_id, language):
        try:
            await s2a(self.language.insert_one)({"guild_id": guild_id, "language": language})
            return {"status": "Done", "msg": "Đã cài đặt thành công"}
        except Exception as e:
            return {
                "status": "Failed", "msg": f"Đã xảy ra lỗi {e}"
            }
            
    async def replace_language(self, guild_id: int, language: str):
        try:
            await s2a(self.language.update_one)({"guild_id": guild_id}, {"$set": {"language": language}})
            return {"status": "OK", "msg": "Đã cập nhật thành công"}
        except Exception as e:
            return {"status": "Failed", "msg": e}

    async def remove_language_on_leave(self, guild_id: int):
        test = await self.guild_language(guild_id)
        if test["status"] == "NoData":
            return

        await s2a(self.language.delete_one)({"guild_id": guild_id})


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
        
    async def check_database(self, guild):
        data = await s2a(self.servers.find_one)({"guild_id": guild})
        if not data:
            return {"status": "No_Data"}
        else:
            return {"status": "Data_Found", "webhook_uri": data["webhook_uri"]}
        
    async def check_server_db(self, guild_id: int):
        data = await s2a(self.servers.find_one)({"guild_id": guild_id})
        if data is None:
            return False
        else:
            return True
        
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
    
    async def get_webhook(self, guild_id: int):
        data = await s2a(self.servers.find_one)({"guild_id": guild_id})
        if data is None:
            return {
                "status": "No_Data"
            }
        else:
            return {
                "status": "Data_Found",
                "webhook_uri": data["webhook_uri"]
            }
        
    async def setupserverlog(self, guild_id: int, webhook_uri: str):
        data = await s2a(self.servers.find_one)({"guild_id": guild_id})
        if data is None:
            await s2a(self.servers.insert_one)({"guild_id": guild_id, "webhook_uri": webhook_uri})
            return {
                "status": "success"
            }
        else:
            return {
                "status": "error"
            }
    
    async def remove_server_log(self, guild_id: int, webhook_uri: str):
        try:
            await s2a(self.servers.delete_one)({"guild_id": guild_id, "webhook_uri": webhook_uri})
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
            
    async def remove_ignored_role_data(self, guild_id: int):
        data = await self.get_ignored_roles(guild_id)
        if data["status"] == "No_data":
            return {
                "status": "no_data"
            }
        try:
            await s2a(self.ignored_roles.delete_many)({"guild_id": guild_id})
            return {
                "status": "done"
            }
        except Exception as e:
            return {
                "status": "failed",
                "msg": f"Đã xảy ra lỗi: {e}"
            }