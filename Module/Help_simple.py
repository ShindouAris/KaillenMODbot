import disnake
from disnake.ext import commands
from utils.ClientUser import ClientUser


class SlashCommandHelp(commands.Cog):
    def __init__(self, bot: ClientUser):
        self.bot = bot
    
    @commands.cooldown(1, 20, commands.BucketType.guild)
    @commands.slash_command(name="help", description="Nhận trợ giúp về các lệnh")
    async def helpcmd(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        serverlogcmd = f"</serverlog:" + str(self.bot.get_global_command_named("serverlog", cmd_type=disnake.ApplicationCommandType.chat_input).id) +">"
        ignorecmd = f"</ignorerole:" + str(self.bot.get_global_command_named("ignorerole", cmd_type=disnake.ApplicationCommandType.chat_input).id) +">"
        pingcmd = f"</ping:" + str(self.bot.get_global_command_named("ping", cmd_type=disnake.ApplicationCommandType.chat_input).id) +">"
        
        embed = disnake.Embed(title=f"Trợ giúp lệnh - {inter.me.name}")
        embed.add_field(name=f"{serverlogcmd}", value="Cài đặt kênh log cho server", inline=False)
        embed.add_field(name=f"{ignorecmd}", value="Cài đặt role sẽ bị bỏ qua cho hệ thống log server", inline=False)
        embed.add_field(name=f"{pingcmd}", value="Kiểm tra ping của bot", inline=False)
        
        await inter.edit_original_response(embed=embed)
        
        
def setup(bot: ClientUser):
    bot.add_cog(SlashCommandHelp(bot))