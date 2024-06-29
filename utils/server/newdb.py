import asyncio
import logging
from typing import Any

from asgiref.sync import sync_to_async as s2a
from pymongo import MongoClient


defaultConfig = {
    "id": int,
    "webhook_url": str,
    "language": str,
    "ignoreroles": set()
}
logger = logging.getLogger(__name__)

class Databases():
    def __init__(self) -> None:
        pass

    async def loadDB(self, serveruri = None):
        self.dbclient = MongoClient(host=serveruri)
        self.guild = self.dbclient.db.guild
        logger.info("Database init ok")

    async def setupdefault(self, guildID = None):
        if guildID is None: return
        await s2a(self.guild.insert_one)({"id": guildID, 
                                          "language": "vi", 
                                          "webhook_url": None, 
                                          "ignoreroles": []})

    async def setupserverlog(self, guildID, webhook_url):




        await s2a(self.guild.update_one)({"id":guildID,
                                          "webhook_url": webhook_url})

    async def get_webhook(self, guildID):
        data = await s2a(self.guild.find_one)({"id": guildID})
        return data["webhook_url"]

    async def guild_language(self, guildID):
        data = await s2a(self.guild.find_one)({"id": guildID})
        return data["language"]

    async def update_language(self, guildID, language):
        await s2a(self.guild.update_one)({"id": guildID, 
                                          "language": language})
        
    async def setup_ignored_roles(self, guild_id: int, role_id: int):
                data = await s2a(self.guild.find_one)({"id": guild_id})
                if data is None:
                    await s2a(self.guild.insert_one)({"id": guild_id, "ignoreroles": [role_id]})
                    return {
                            "status": "success",
                            "action": "insert"
                        }
                else:
                    await s2a(self.guild.update_one)({"id": guild_id}, {"$push": {"ignoreroles": role_id}})
                    return {
                                "status": "success",
                                "action": "update_sql"
                    }
                
    async def remove_ignore_role(self, guildID, roleID):
        await s2a(self.guild.update_one)({"id": guildID}, {"$pull": {"ignoreroles": roleID}})

    async def check_mute(self, role: str, guild: int) -> bool:
                raw_data = await s2a(self.guild.find_one)({"id": guild})

                data = raw_data["ignoreroles"]

                if data is None or data == []:
                    return False

                for roleData in data:
                    if str(roleData) not in role:
                            continue
                    else:
                        return True

    async def check_role(self, guildID, roleID):
        data = await s2a(self.guild.find_one)({"id": guildID})
        if data is None:
            return {
                "info": False,
                "data": "None"
            }
        elif roleID not in data["ignoreroles"]:
                                                                                            return {
                                                                                                            "info": False,
                                                                                                                            "data": "None"
                                                                                                                                        }


 

        elif roleID in data["ignoreroles"]:
            return {
                "info": True,
                "data": data
            }
        
    async def check_database(self, guildID):
        raw_data = await s2a(self.guild.find_one)({"id": guildID})
        if raw_data["webhook_url"] is None:
            return {"status": "No_Data"}
        else:
            return {"status": "Data_Found", "webhook_uri": raw_data["webhook_url"]}




    
        

