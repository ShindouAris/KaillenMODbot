import disnake
from disnake.ext import commands
import pytz # if you don't have this, do pip install pytz, it's used for timezones
from datetime import datetime
from utils.client import BotCore

HCM = pytz.timezone('Asia/Ho_Chi_Minh')

class OnGuildChannelCreate(commands.Cog):
    def __init__(self, client: BotCore):
        self.client = client 

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: disnake.TextChannel):
        if channel.name.startswith("ticket"):
            return
   

        data = await self.client.serverdb.get_log_channel(channel.guild.id)

        if data is None:
            return
        try:
          logchannel = self.client.get_channel(data["channel_id"])
        except KeyError:
            return

        embed = disnake.Embed(
            title="Kênh tạo ra",
            description=f"{channel.mention} đã được tạo ra",
            color=disnake.Color.red(),
            timestamp=datetime.now(HCM),
        )

        await logchannel.send(embed=embed)

def setup(client: BotCore):
    client.add_cog(OnGuildChannelCreate(client))