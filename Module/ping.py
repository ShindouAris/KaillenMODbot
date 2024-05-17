import disnake
from disnake.ext import commands
import psutil, humanize
from os import getpid
from utils.ClientUser import ClientUser
import platform

class Ping(commands.Cog):
    def __init__(self, bot: ClientUser):
        self.bot = bot

    @commands.slash_command()
    async def ping(self, ctx):
        embed = disnake.Embed(
            title="Pong!",
            description=f"Độ trễ API: {round(self.bot.latency * 100)}ms",
            color=disnake.Color.green()
        )
        await ctx.send(embed=embed)
        
    about_cd = commands.CooldownMapping.from_cooldown(1, 5, commands.BucketType.member)
        
    @commands.slash_command(
        description=f"Xem thông tin về tôi.", cooldown=about_cd, dm_permission=False
    )
    async def about(
            self,
            inter: disnake.AppCmdInter
    ):
        await inter.response.defer(ephemeral=True)
        python_ram = psutil.Process(getpid()).memory_info().rss

        ram_msg = f"> <:python:1204300262911774761> **⠂Sử dụng RAM (Python):** `{humanize.naturalsize(python_ram)} \ {humanize.naturalsize(psutil.virtual_memory()[0])}`\n"
        
        latency = round(self.bot.latency * 100)
        if latency >= 1000:
            latency_bot = f"Độ trễ rất cao {latency}"
        elif latency >= 200:
            latency_bot = f"Độ trễ cao {latency}"
        elif latency >= 100:
            latency_bot = f"Độ trễ trung bình {latency}"
        else:
            latency_bot = f"{latency}"
            
        embed = disnake.Embed(description="", color=0xC03865)
        
        embed.description += f"### Thông tin của {self.bot.user.name}#{self.bot.user.discriminator}:\n"
        
        embed.description += f"> <:python:1204300262911774761> **Phiên bản của Python:** `{platform.python_version()}`\n" \
                             f"> <:disnake:1204300267257069569> **Phiên bản của Disnake:** `Pre-release {disnake.__version__}`\n" \
                             f"> <:home:1208751844373827607> **Hệ điều hành đang sử dụng:** `{platform.system()} {platform.release()} {platform.machine()}`\n" \
                             f"> <:cpu:1146331051556339712> **Mức sử dụng CPU:** `{psutil.cpu_percent()}% \ 100%, ({psutil.cpu_count()} Core)`\n" \
                             f"> 📶 **Độ trễ API:** `{latency_bot}ms`\n" \
                             f"{ram_msg}" \
                             f"> <a:loading:1204300257874288681> **Lần khởi động lại cuối cùng:** <t:{int(self.bot.uptime.timestamp())}:R>\n" \
                             f"> <:hsr_OneiricShard:1241024010964172870> **ShardID:** {self.bot.shard_id}"
        
        try:
            await inter.edit_original_message(embed=embed)
        except (AttributeError, disnake.InteractionNotEditable):
            try:
                await inter.response.edit_message(embed=embed)
            except:
                await inter.send(embed=embed, ephemeral=True)             


def setup(bot: ClientUser):
    bot.add_cog(Ping(bot))