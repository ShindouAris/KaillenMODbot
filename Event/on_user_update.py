import disnake 
from disnake.ext import commands


from utils.ClientUser import ClientUser
class OnMemberUpdate(commands.Cog):
    def __init__(self, client: ClientUser):
        self.client = client
    
    @commands.Cog.listener()
    async def on_member_update(self, before: disnake.Member, after: disnake.Member):
        # Bỏ qua bot
        if after.bot or before.bot:
            return
    
        # Kiểm tra thay đổi vai trò
        if before.roles != after.roles:
            
            roleUpdate = list(set(after.roles) - set(before.roles))
            if roleUpdate:
                roleChange = ", ".join([role.mention for role in roleUpdate])
                loc = "user_added_role"
            else:
                removed_roles = list(set(before.roles) - set(after.roles))
                if removed_roles:
                    roleChange = ", ".join([role.mention for role in removed_roles])
                    loc = "user_removed_role"
                else:
                    return  # Không có thay đổi về vai trò
                
            kwargs = {
                "userName": after.name,
                "role": roleChange
            }

            # Lấy ngôn ngữ của server
            language = await self.client.serverdb.guild_language(after.guild.id)

            # Lấy URI của webhook
            # webhook_uri = await self.client.serverdb.get_webhook(after.guild.id)
            webhook_uri = await self.client.serverdb.get_guild_webhook(after.guild.id)
            
            # Kiểm tra xem webhook_uri có tồn tại không
            # if not webhook_uri or "webhook_uri" not in webhook_uri:
            #     return
            
            # Tạo Embed và thêm trường với thông tin vai trò
            embed = disnake.Embed()
            txt = self.client.handle_language.get(language["language"], 'user', loc)
            embed.description = txt.format(**kwargs)

            # Gửi webhook
            # await self.client.webhook_utils.process_webhook(webhook_uri["webhook_uri"], embed)
            await self.client.webhook_utils.process_webhook(webhook_uri, embed)
    
def setup(bot: ClientUser): bot.add_cog(OnMemberUpdate(bot))
