import disnake
from disnake.ext import commands
import pytz # if you don't have this, do pip install pytz, it's used for timezones
from datetime import datetime
from utils.ClientUser import ClientUser

HCM = pytz.timezone('Asia/Ho_Chi_Minh')

class OnGuildRoleDelete(commands.Cog):
    def __init__(self, client: ClientUser):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: disnake.Role): 
    
        # Kiểm tra xem có dữ liệu về server này không
        guild_id = role.guild.id

        
        data = await self.client.serverdb.get_webhook(guild_id)

        if data is None:
            return
        try:
            channel = data["webhook_uri"]
        except KeyError:
            return

        embed = disnake.Embed(
            title="Vai trò đã xóa",
            description=f"{role.name} đã bị xóa",
            color=disnake.Color.red(),
            timestamp=datetime.now(HCM),
        )

        await self.client.webhook_utils.process_webhook(channel, embed)

def setup(client: ClientUser):
    client.add_cog(OnGuildRoleDelete(client))