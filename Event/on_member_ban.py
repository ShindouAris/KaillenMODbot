import disnake
from disnake.ext import commands
import pytz # if you don't have this, do pip install pytz, it's used for timezones
from datetime import datetime
from utils.client import BotCore

HCM = pytz.timezone('Asia/Ho_Chi_Minh')

class BanEvent(commands.Cog):
    def __init__(self, client: BotCore):
        self.client = client

    @commands.Cog.listener()
    async def on_member_ban(self, guild: disnake.Guild, user: disnake.User):
 

        data = await self.client.serverdb.get_log_channel(guild.id)

        if data is None:
            return
        
        try:
            channel = guild.get_channel(data["channel_id"]) # How tf i can forget this
        except KeyError:
            return

        embed = disnake.Embed(
            title="Thành viên bị cấm",
            description=f"{user.mention} đã bị cấm khỏi máy chủ",
            color=disnake.Color.red(),
            timestamp=datetime.now(HCM),
        )

        await channel.send(embed=embed)

def setup(client: BotCore):
    client.add_cog(BanEvent(client))