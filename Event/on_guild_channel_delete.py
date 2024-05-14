import disnake
from disnake.ext import commands
import pytz # if you don't have this, do pip install pytz, it's used for timezones
from datetime import datetime
from utils.client import BotCore

HCM = pytz.timezone('Asia/Ho_Chi_Minh')

class OnGuildChannelDelete(commands.Cog):
    def __init__(self, client: BotCore):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: disnake.TextChannel):

        if channel.name.startswith("ticket"): #! Ingore ticket channel
            return


        data = await self.client.serverdb.get_log_channel(channel.guild.id)

        if data is None:
            return

        try:
            logchannel = self.client.get_channel(data["channel_id"])
        except KeyError:
            return
        
        embed = disnake.Embed(
            title="Kênh đã xóa",
            description=f"{channel.name} đã bị xóa",
            color=disnake.Color.red(),
            timestamp=datetime.now(HCM),
        )

        await logchannel.send(embed=embed)

def setup(client: BotCore):
    client.add_cog(OnGuildChannelDelete(client))