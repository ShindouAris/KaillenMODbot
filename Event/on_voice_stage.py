import disnake
from disnake.ext import commands
import pytz # if you don't have this, do pip install pytz, it's used for timezones
from datetime import datetime
from utils.client import BotCore

HCM = pytz.timezone('Asia/Ho_Chi_Minh')

class OnVCUpdate(commands.Cog):
    def __init__(self, client: BotCore):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: disnake.Member, before: disnake.VoiceState, after: disnake.VoiceState):
        if member.bot: #! Bỏ qua bot
            return
        checkmember = await self.client.serverdb.check_mute(member.top_role.id, member.guild.id)
        if checkmember["info"] == True:
            return #! Nếu người dùng có role trong danh sách bị mute thì bỏ qua
        
        if before.channel != after.channel:
       
            try:
                data = await self.client.serverdb.get_log_channel(member.guild.id)
            except KeyError:
                return

            if data is None:
                return
            try:
                channel = self.client.get_channel(data["channel_id"])
            except KeyError:
                return
            
            embed = disnake.Embed(
                title="Cập nhật trạng thái kênh giọng nói",
                description=f"{member.mention} đã thay đổi",
                color=disnake.Color.red(),
                timestamp=datetime.now(HCM),
            )

            embed.add_field(name="Trước đó", value=before.channel, inline=False)
            embed.add_field(name="Sau khi cập nhật", value=after.channel, inline=False)

            await channel.send(embed=embed)

def setup(client: BotCore):
    client.add_cog(OnVCUpdate(client))