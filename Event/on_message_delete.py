import disnake
from disnake.ext import commands
import pytz # if you don't have this, do pip install pytz, it's used for timezones
from datetime import datetime
from utils.ClientUser import ClientUser as BotCore

HCM = pytz.timezone('Asia/Ho_Chi_Minh')

class OnMessageDelete(commands.Cog):
    def __init__(self, client: BotCore):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message):
        try:
            check = await self.client.serverdb.check_mute(message.author.top_role.id, message.guild.id)
        except AttributeError: #! Ignore DM
            return
        if message.author.bot:
            return
        elif check["info"] == True:
            return
        else:
            pass

        
        data = await self.client.serverdb.get_log_channel(message.guild.id)

        if data is None:
            return
        try:
            channel = self.client.get_channel(data["channel_id"])
        except KeyError:
            return  # Ignore if channel is None
        
        

        embed = disnake.Embed(
            title="Đã xóa tin nhắn",
            description=f"Tin nhắn được gửi bởi {message.author.mention} đã xóa ở {message.channel.mention}",
            color=disnake.Color.red(),
            timestamp=datetime.now(HCM),  # Use Set time for consistency
        )
        if message.content.startswith("https://media.discordapp.net/attachments"):
            embed.set_image(url=message.content)
        elif message.content.startswith("https://cdn.discordapp.com/attachments"):
            embed.set_image(url=message.content)
        elif message.content.startswith("https://tenor.com/view"):
            embed.set_image(url=message.content)
        elif message.content.startswith("https://giphy.com/gifs"):
            embed.set_image(url=message.content)
        elif message.content.startswith("https://imgur.com"):
            embed.set_image(url=message.content)
        elif message.attachments:
            embed.set_image(url=message.attachments[0].url)
        else:
            embed.add_field(name="Tin nhắn", value=message.content, inline=False)
        

        await channel.send(embed=embed)

def setup(client: BotCore):
    client.add_cog(OnMessageDelete(client))