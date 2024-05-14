import disnake
from disnake.ext import commands
import pytz # if you don't have this, do pip install pytz, it's used for timezones
from datetime import datetime
from utils.ClientUser import ClientUser

HCM = pytz.timezone('Asia/Ho_Chi_Minh')

class OnGuildRoleCreate(commands.Cog):
    def __init__(self, client: ClientUser):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: disnake.Role): 
  

        data = await self.client.serverdb.get_log_channel(role.guild.id)

        if data is None:
            return
        try:
            channel = self.client.get_channel(data["channel_id"])
        except KeyError:
            return
        
        embed = disnake.Embed(
            title="Vai trò được tạo ra",
            description=f"{role.name} was created",
            color=disnake.Color.red(),
            timestamp=datetime.now(HCM),
        )

        await channel.send(embed=embed)

def setup(client: ClientUser):
    client.add_cog(OnGuildRoleCreate(client))