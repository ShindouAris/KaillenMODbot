import disnake
from disnake.ext import commands
import pytz # if you don't have this, do pip install pytz, it's used for timezones
from datetime import datetime
from utils.client import BotCore

HCM = pytz.timezone('Asia/Ho_Chi_Minh')

class OnGuildRoleUpdate(commands.Cog):
    def __init__(self, client: BotCore):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: disnake.Role, after: disnake.Role):
        if before.name != after.name:


            data = await self.client.serverdb.get_log_channel(before.guild.id)

            if data is None:
                return
            try:
                channel = self.client.get_channel(data["channel_id"])
            except KeyError:
                return

            embed = disnake.Embed(
                title="Cập nhật vai trò",
                description=f"{before.mention} đã thay đổi",
                color=disnake.Color.red(),
                timestamp=datetime.now(HCM),
            )

            embed.add_field(name="Trước đó", value=before.name, inline=False)
            embed.add_field(name="Sau khi cập nhật", value=after.name, inline=False)

            await channel.send(embed=embed)

def setup(client: BotCore):
    client.add_cog(OnGuildRoleUpdate(client))
    