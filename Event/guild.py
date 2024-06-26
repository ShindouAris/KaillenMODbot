import logging

import disnake
from disnake.ext import commands

from utils.ClientUser import ClientUser

logger = logging.getLogger(__name__)

class GuildEntry(commands.Cog):
    def __init__(self, bot: ClientUser):
        self.client = bot
        
        
    @commands.Cog.listener("on_guild_remove")
    async def remove_data(self, guild: disnake.Guild):

        logger.info(f"Bị xóa khỏi máy chủ: {guild.name} - [{guild.id}]")
        data = await self.client.serverdb.get_guild_webhook(guild.id)
        
        if data["status"] == "No_Data":
            return
        
        guild_webhook = data
        
        try:
            await self.client.serverdb.remove_server_log(guild.id, guild_webhook)
            await self.client.serverdb.remove_ignored_role_data(guild.id)
            await  self.client.serverdb.remove_language_on_leave(guild.id)
            await self.client.serverdb.delwebhookcache(guild.id)
            await self.client.serverdb.delrolecache(guild.id)
        except Exception as e:
            logger.error(f"Đã xảy ra lỗi {e}")


def setup(bot: ClientUser): bot.add_cog(GuildEntry(bot))
