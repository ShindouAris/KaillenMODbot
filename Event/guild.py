import disnake
from disnake.ext import commands
from utils.ClientUser import ClientUser

class GuildEntry(commands.Cog):
    def __init__(self, bot: ClientUser):
        self.client = bot
        
        
    @commands.Cog.listener()
    async def on_guild_remove(self, guild: disnake.Guild):

        print(f"Bị xóa khỏi máy chủ: {guild.name} - [{guild.id}]")
        
        data = self.client.serverdb.get_webhook(guild.id)
        
        if data["status"] == "No_Data":
            return
        
        guild_webhook = data["webhook_uri"]
        
        await self.client.serverdb.remove_server_log(guild.id, guild_webhook)

def setup(bot: ClientUser): bot.add_cog(GuildEntry(bot))
