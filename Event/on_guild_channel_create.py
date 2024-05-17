import disnake
from disnake.ext import commands
import pytz # if you don't have this, do pip install pytz, it's used for timezones
from datetime import datetime
from utils.ClientUser import ClientUser

HCM = pytz.timezone('Asia/Ho_Chi_Minh')

class OnGuildChannelCreate(commands.Cog):
    def __init__(self, client: ClientUser):
        self.client = client 

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: disnake.TextChannel):
        if channel.name.startswith("ticket"):
            return
   

        data = await self.client.serverdb.get_webhook(channel.guild.id)

        if data is None:
            return
        try:
          logchannel = data["webhook_uri"]
        except KeyError:
            return

        embed = disnake.Embed(
            title="Kênh tạo ra",
            description=f"{channel.mention} đã được tạo ra",
            color=disnake.Color.red(),
            timestamp=datetime.now(HCM),
        )

        # await logchannel.send(embed=embed)
        await self.client.webhook_utils.process_webhook(logchannel, embed)

def setup(client: ClientUser):
    client.add_cog(OnGuildChannelCreate(client))