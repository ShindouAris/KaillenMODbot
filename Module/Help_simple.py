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
        change_language_cmd = f"</change_language:" + str(self.bot.get_global_command_named("change_language", cmd_type=disnake.ApplicationCommandType.chat_input).id) + ">"
        server_language = await self.bot.serverdb.guild_language(inter.guild_id)
        serverDes =  self.bot.handle_language.get(server_language["language"], "ServerLogDescription")
        role_Des =  self.bot.handle_language.get(server_language["language"], "ignoreroleDescription")
        pingDes =  self.bot.handle_language.get(server_language["language"], "pingDescription")
        change_language_Des = self.bot.handle_language.get(server_language["language"], "changeLanguageDescription")
        
        embed = disnake.Embed(title=f"Help - {inter.me.name}")
        embed.add_field(name=f"{serverlogcmd}", value=serverDes, inline=False)
        embed.add_field(name=f"{ignorecmd}", value=role_Des, inline=False)
        embed.add_field(name=f"{pingcmd}", value=pingDes, inline=False)
        embed.add_field(name=f"{change_language_cmd}", value=change_language_Des)
        
        await inter.edit_original_response(embed=embed)
        
        
def setup(bot: ClientUser):
    bot.add_cog(SlashCommandHelp(bot))