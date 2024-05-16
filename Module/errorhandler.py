import disnake
from disnake.ext import commands
from pymongo.errors import ServerSelectionTimeoutError

from utils.ClientUser import ClientUser
from utils.conv import time_format, perms_translations
from utils.error import ClientException, parse_error, paginator, send_message
import traceback



class HandleError(commands.Cog):
    def __init__(self, bot: ClientUser):
        self.bot = bot    
    
    @commands.Cog.listener('on_user_command_error')
    @commands.Cog.listener('on_message_command_error')
    @commands.Cog.listener('on_slash_command_error')
    async def on_interaction_command_error(self, inter: disnake.AppCmdInter, error: Exception):

        await self.hander_error_cmd(ctx=inter, error=error)
    
    async def hander_error_cmd(self, ctx: disnake.ApplicationCommandInteraction, error: Exception):        
        
        if isinstance(error, ClientException):
            return
        
        error_msg = parse_error(ctx, error)
        
        if isinstance(error, disnake.NotFound) and str(error).endswith("Unknown Interaction"):
            return
        
        kwargs = {"text": ""}
        color = disnake.Color.red()

        if not error_msg:

            kwargs["embeds"] = disnake.Embed(
                color=color,
                title = "Đã có một sự cố xảy ra, nhưng đó không phải lỗi của bạn:",
                description=f"```py\n{repr(error)[:2030].replace(self.bot.http.token, 'mytoken')}```"
            )
        else:

            kwargs["embeds"] = []

            for p in paginator(error_msg):
                kwargs["embeds"].append(disnake.Embed(color=color, description=p))

        try:
            await send_message(ctx, **kwargs)
        except:
            print(("-"*50) + f"\n{error_msg}\n" + ("-"*50))
            traceback.print_exc()
        
    @commands.Cog.listener("on_command_error")
    async def prefix_command_handle(self, ctx: disnake.AppCommandInter, error: Exception):
        
        if isinstance(error, commands.CommandNotFound):
            return
        
        error_txt = ""
        
        if isinstance(error, commands.NotOwner):
            error_txt = "**Chỉ nhà phát triển của tôi mới có thể sử dụng lệnh này**"

        if isinstance(error, commands.BotMissingPermissions):
            error_txt = "Tôi không có các quyền sau để thực thi lệnh này: ```\n{}```" \
                .format(", ".join(perms_translations.get(perm, perm) for perm in error.missing_permissions))

        if isinstance(error, commands.MissingPermissions):
            error_txt = "Bạn không có các quyền sau để thực hiện lệnh này: ```\n{}```" \
                .format(", ".join(perms_translations.get(perm, perm) for perm in error.missing_permissions))
                
        if isinstance(error, commands.NoPrivateMessage):
            error_txt = "Lệnh này không thể chạy trên tin nhắn riêng tư."
        
        if isinstance(error, commands.CommandOnCooldown):
            remaing = int(error.retry_after)
            if remaing < 1:
                remaing = 1
            error_txt = "**Bạn phải đợi {} mới có thể sử dụng lệnh này.**".format(time_format(int(remaing) * 1000, use_names=True))
            
        await ctx.send(error_txt)
            
def setup(bot: ClientUser):
    bot.add_cog(HandleError(bot))