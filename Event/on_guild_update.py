import disnake
from disnake.ext import commands
import pytz # if you don't have this, do pip install pytz, it's used for timezones
from datetime import datetime
from utils.client import BotCore

HCM = pytz.timezone('Asia/Ho_Chi_Minh')


class OnGuildUpdate(commands.Cog):
    def __init__(self, client: BotCore):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_update(self, before: disnake.Guild, after: disnake.Guild):
        if before.name != after.name:
        

            data = self.client.serverdb.get_log_channel(before.id)

            if data is None:
                return
            try:
                channel = self.client.get_channel(data["channel_id"])
            except KeyError:
                return
            
            embed = disnake.Embed(
                title="Máy chủ được cập nhật",
                description=f"{before.name} đã thay đổi",
                color=disnake.Color.red(),
                timestamp=datetime.now(HCM),
            )

            embed.add_field(name="Trước đó", value=before.name, inline=False)
            embed.add_field(name="Sau khi cập nhật", value=after.name, inline=False)

            await channel.send(embed=embed)

        elif before.icon != after.icon:
            data = self.client.serverdb.get_log_channel(before.id)

            if data is None:
                return
            try:
                channel = self.client.get_channel(data["channel_id"])
            except KeyError:
                return
            
            embed = disnake.Embed(
                title="Máy chủ được cập nhật",
                description=f"{before.name} đã thay đổi",
                color=disnake.Color.red(),
                timestamp=datetime.now(HCM),
            )

            embed.add_field(name="Trước đó", value=before.icon, inline=False)
            embed.add_field(name="Sau khi cập nhật", value=after.icon, inline=False)

            await channel.send(embed=embed)

def setup(client: BotCore):
    client.add_cog(OnGuildUpdate(client))