import disnake
from disnake.ext import commands


from utils.ClientUser import ClientUser


class Ping(commands.Cog):
    def __init__(self, bot: ClientUser):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        embed = disnake.Embed(
            title="Pong!",
            description=f"Độ trễ API: {round(self.bot.latency * 100)}ms",
            color=disnake.Color.green()
        )
        await ctx.send(embed=embed)

def setup(bot: ClientUser):
    bot.add_cog(Ping(bot))