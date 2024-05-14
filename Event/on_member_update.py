import disnake
from disnake.ext import commands
import pytz # if you don't have this, do pip install pytz, it's used for timezones
from datetime import datetime
from utils.client import BotCore

HCM = pytz.timezone('Asia/Ho_Chi_Minh')

class OnMemberUpdate(commands.Cog):
    def __init__(self, client: BotCore):
        self.client = client

    @commands.Cog.listener()
    async def on_member_update(self, before: disnake.Member, after: disnake.Member):
        if before.name != after.name:


            data = await self.client.serverdb.get_log_channel(before.guild.id)

            if data is None:
                return
            try:
                channel = before.guild.get_channel(data["channel_id"])
            except KeyError:
                return

            embed = disnake.Embed(
                title="User Updated",
                description=f"{before.mention} đã thay đổi",
                color=disnake.Color.red(),
                timestamp=datetime.now(HCM),
            )

            embed.add_field(name="Trước đó", value=before.name, inline=False)
            embed.add_field(name="Sau khi cập nhật", value=after.name, inline=False)

            await channel.send(embed=embed)
        elif before.discriminator != after.discriminator:
    
            if data is None:
                return

            try:
                channel = before.guild.get_channel(data["channel_id"])
            except KeyError:
                return

            embed = disnake.Embed(
                title="Cập nhật người dùng",
                description=f"{before.mention} đã thay đổi",
                color=disnake.Color.red(),
                timestamp=datetime.now(HCM),
            )

            embed.add_field(name="Trước đó", value=before.discriminator, inline=False)
            embed.add_field(name="Sau khi cập nhật", value=after.discriminator, inline=False)

            await channel.send(embed=embed)
        elif before.avatar != after.avatar:
            

            if data is None:
                return

            channel = before.guild.get_channel(data["channel_id"])

            embed = disnake.Embed(
                title="Cập nhật người dùng",
                description=f"{before.mention} đã thay đổi",
                color=disnake.Color.red(),
                timestamp=datetime.now(HCM),
            )

            embed.set_thumbnail(url=after.guild_avatar)

            await channel.send(embed=embed)

def setup(client: BotCore):
    client.add_cog(OnMemberUpdate(client))