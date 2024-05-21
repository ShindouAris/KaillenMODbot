import disnake
from disnake.ext import commands
from utils.ClientUser import ClientUser

class Owner(commands.Cog):
    def __init__(self, bot: ClientUser):
        self.bot = bot
        
    async def reload_module(self):
    
        self.bot.load_modules()
        self.bot.load_events()
        
    @commands.is_owner()
    @commands.slash_command(name="reload", description="Tải lại các module")
    async def _reload_module(self, ctx: disnake.ApplicationCommandInteraction):
        await ctx.response.defer()
        await self.reload_module()
        await ctx.edit_original_response("Đã tải lại các module và event")
        
def setup(bot: ClientUser):
    bot.add_cog(Owner(bot))