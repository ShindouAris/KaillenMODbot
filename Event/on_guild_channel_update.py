import disnake
from disnake.ext import commands
import pytz # if you don't have this, do pip install pytz, it's used for timezones
from datetime import datetime
from utils.client import BotCore

HCM = pytz.timezone('Asia/Ho_Chi_Minh')

class OnGuildChannelUpdate(commands.Cog):
    def __init__(self, client: BotCore):
        self.client = client 

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: disnake.TextChannel, after: disnake.TextChannel):
        if before.name.startswith("ticket"): #! Ingore ticket channel
            return
        if before.name != after.name:

        

            data = await self.client.serverdb.get_log_channel(before.guild.id)

            if data is None:
                return

            try:
                channel = self.client.get_channel(data["channel_id"])
            except KeyError:
                return

            embed = disnake.Embed(
                title="Cập nhật kênh",
                description=f"{before.mention} đã thay đổi",
                color=disnake.Color.red(),
                timestamp=datetime.now(HCM),
            )

            embed.add_field(name="Trước đó", value=before.name, inline=False)
            embed.add_field(name="Sau khi cập nhật", value=after.name, inline=False)

            await channel.send(embed=embed)
        try:
            if before.topic != after.topic:
                if before.topic == None and after.topic == " ":
                    return # -*- ? -*-
                data = await self.client.serverdb.get_log_channel(before.guild.id)

                if data is None:
                    return

                try:
                    channel = self.client.get_channel(data["channel_id"])
                except KeyError:
                    return

                embed = disnake.Embed(
                    title="Cập nhật kênh",
                    description=f"{before.mention} đã thay đổi",
                    color=disnake.Color.red(),
                    timestamp=datetime.now(HCM),
                )

                embed.add_field(name="Trước đó", value=before.topic, inline=False)
                embed.add_field(name="Sau khi cập nhật", value=after.topic, inline=False)

                await channel.send(embed=embed)
        except AttributeError:
            pass

def setup(client: BotCore):
    client.add_cog(OnGuildChannelUpdate(client))