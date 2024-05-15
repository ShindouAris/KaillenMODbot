# -*- coding: utf-8 -*-
import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction

from disnake import Option, OptionType, ApplicationCommandInteraction
from utils.ClientUser import ClientUser
from typing import Union
from utils.GenEMBED import Embed

class Serverlog(commands.Cog):
    def __init__(self, bot):
        self.bot: ClientUser = bot

    emoji = "🛠️"
    name = "Sererlog"
    desc_prefix = f"[{emoji} {name}] | "
    
    @commands.cooldown(1, 300, commands.BucketType.guild) 
    @commands.has_guild_permissions(manage_guild=True, manage_channels=True)
    @commands.slash_command(name="serverlog", description=f"{desc_prefix}Set the serverlog channel", options=[Option("channel", "The channel to set the serverlog to", OptionType.channel, required=True)])
    async def serverlog(self, ctx: Union[commands.Context, ApplicationCommandInteraction], channel: disnake.TextChannel):
        check = await self.bot.serverdb.check_database(ctx.guild.id)
        if check["status"] == "No_Data":    
                    if isinstance(ctx, ApplicationCommandInteraction):
                        await ctx.response.defer()
                    await self.bot.serverdb.setupserverlog(ctx.guild.id, channel.id)
                    embed = disnake.Embed(title="Server Log", description=f"<:verify:1134033164151566460> Đã kích hoạt server log cho máy chủ {ctx.author.guild.name}\nKênh đã thiết lập: {channel.mention}")
                    embed.set_thumbnail(url="https://media.discordapp.net/stickers/1039992459209490513.png")
                    embed.set_footer(text=f"Thiết lập bởi {ctx.author.name} - {ctx.author.id}", 
                                     icon_url=ctx.author.avatar.url)
                    await ctx.edit_original_response(embed=embed)
        elif check["status"] == "Data_Found":
                    if isinstance(ctx, ApplicationCommandInteraction):
                        await ctx.response.defer()
                    if check["channel_id"] == channel.id:
                        remove = await self.bot.serverdb.remove_server_log(ctx.guild_id, channel.id)
                        if remove["status"] == "failed":
                            await ctx.send("Đã xảy ra lỗi", delete_after=5)
                        await ctx.edit_original_response("Đã xóa dữ liệu", delete_after=5)
                        
                    else:
                        old_channel_id = await self.bot.serverdb.get_log_channel(ctx.guild_id)
                        await self.bot.serverdb.remove_server_log(ctx.guild_id, old_channel_id["channel_id"])
                        await self.bot.serverdb.setupserverlog(ctx.guild.id, channel.id)
                        embed = disnake.Embed(title="Server Log", description=f"<:verify:1134033164151566460> Đã thay đổi kênh server log cho máy chủ {ctx.author.guild.name}\nKênh đã thiết lập: {channel.mention}")
                        embed.set_thumbnail("https://media.discordapp.net/stickers/1039992459209490513.png")
                        embed.set_footer(text=f"Thiết lập bởi {ctx.author.name} - {ctx.author.id}", 
                                        icon_url=ctx.author.avatar.url)
                        await ctx.send(embed=embed)

    @commands.cooldown(1, 300, commands.BucketType.guild) 
    @commands.has_guild_permissions(manage_roles=True, manage_guild=True)
    @commands.slash_command(name="ignorerole", description=f"{desc_prefix} Ignore a role from serverlog", 
                            options=[disnake.Option("role", "The role to ignore", OptionType.role, required=True, max_length=20, min_length=1, max_value=20)])
    async def ignorerole(self, ctx: Union[commands.Context, ApplicationCommandInteraction], role: disnake.Role):
        await ctx.response.defer(ephemeral=True)
        check = await self.bot.serverdb.check_database(ctx.guild.id)
        ADD_embed = disnake.Embed(title="ADD ROLE", description=f"Đã thêm role {role.name} vào danh sách bỏ qua", color=disnake.Color.green()).set_footer(text=f"Người thực hiện: {ctx.author}", icon_url=self.bot.user.avatar)
        REMOVE_embed = disnake.Embed(title="REMOVE ROLE", description=f"Đã xóa role {role.name} khỏi danh sách bỏ qua", color=disnake.Color.green()).set_footer(text=f"Người thực hiện: {ctx.author}", icon_url=self.bot.user.avatar)
        if check["status"] == "Data_Found":
                        role_check = await self.bot.serverdb.check_role(ctx.guild.id, role.id)
                        if role_check["info"] == False: #?
                            await self.bot.serverdb.setup_ignored_roles(ctx.guild.id, role.id)
                            await ctx.send(embed=ADD_embed)
                        elif role_check["info"] == "No":
                            await self.bot.serverdb.setup_ignored_roles(ctx.guild.id, role.id)
                            await ctx.send(embed=ADD_embed)
                        else:
                            await self.bot.serverdb.setup_ignored_roles(ctx.guild.id, role.id)
                            await ctx.edit_original_response(embed=REMOVE_embed)
        elif check["status"] == "No_Data":
            cmd = f"</serverlog:" + str(self.bot.pool.controller_bot.get_global_command_named("serverlog", cmd_type=disnake.ApplicationCommandType.chat_input).id) +">"
            await ctx.edit_original_response(embed=Embed.gen_error_embed(f"Vui lòng sử dụng lệnh\n" 
                                                                   f"```/serverlog```\n" 
                                                                   f"Để thiết lập hệ thống log máy chủ\n"
                                                                   f"Hoặc bấm vào đây {cmd}"))
            return
def setup(bot: ClientUser):
    bot.add_cog(Serverlog(bot))