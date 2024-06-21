######################################
# Author: Yuuki (@yuuki.dn)
# Version: 1.1-BETA
# DMs me if you want to buy a bot <3
######################################

import disnake
from disnake.ext import commands
import disnake.http

import re

USER_NOT_FOUND_EMBED = disnake.Embed(
    title="❌ Không thể tìm thấy thông tin của người dùng được yêu cầu",
    color=0xFF0000
)

USER_NO_AVATAR_EMBED = disnake.Embed(
    title="❌ Người dùng này không đặt avatar",
    color=0xFF0000
)

USER_NO_BANNER_EMBED = disnake.Embed(
    title="❌ Người dùng này không đặt banner",
    color=0xFF0000
)


def build_button_table(avatar: bool, user_id: str) -> disnake.ui.View:
    # avatar = True if avatar is currently displayed
    view = disnake.ui.View(timeout=60)
    avatar_btn = disnake.ui.Button(
        style=disnake.ButtonStyle.secondary if avatar else disnake.ButtonStyle.primary,
        label="Avatar",
        disabled=avatar,
        custom_id=f"avatar_{user_id}",
        row = 0
    )
    avatar_global_btn = disnake.ui.Button(
        style=disnake.ButtonStyle.secondary if avatar else disnake.ButtonStyle.primary,
        label="Global Avatar",
        disabled=avatar,
        custom_id=f"avatar_{user_id}_g",
        row = 0
    )
    banner_btn = disnake.ui.Button(
        style=disnake.ButtonStyle.secondary if not avatar else disnake.ButtonStyle.primary,
        label="Banner",
        disabled=not avatar,
        custom_id=f"banner_{user_id}",
        row = 0
    )
    delete_btn = disnake.ui.Button(style=disnake.ButtonStyle.danger, emoji="🗑️", custom_id="delete", row = 0)
    view.add_item(avatar_btn)
    view.add_item(avatar_global_btn)
    view.add_item(banner_btn)
    view.add_item(delete_btn)
    return view
    

def parse_userid(text: str) -> str:
    res: re.Match = re.search(r"\d{17,21}", text)
    if res is None: return None
    return res.group(0)


class UserGlobalInfo:
    id: str = None
    name: str = None
    avatar_id: str = None
    banner_id: str = None
    
    # Static function
    def from_data(data: dict):
        info = UserGlobalInfo()
        info.id = data["id"]
        info.name = data["username"]
        info.avatar_id = data["avatar"]
        info.banner_id = data["banner"]
        if data["global_name"] is not None:
            info.name = data["global_name"]
        return info
        

async def get_user_global_info(bot: commands.Bot, user_id: str) -> UserGlobalInfo:
    if user_id is None or user_id.strip().__len__() < 18: return None
    try:
        data = await bot.http.request(disnake.http.Route("GET", f"/users/{user_id}"))
        return UserGlobalInfo.from_data(data)
    except Exception as e:
        print(repr(e))
        return None


def build_avatar_embed(name: str, url: str, _global: str = False) -> disnake.Embed:
    embed = disnake.Embed(
        title=f"Avatar {'toàn cầu' if _global else 'máy chủ'} của {name}",
        color=0xFFFFFF,
        timestamp=disnake.utils.utcnow()
    )
    embed.set_image(url)
    return embed


def build_banner_embed(name: str, url: str) -> disnake.Embed:
    embed = disnake.Embed(
        title=f"Banner của {name}",
        color=0xFFFFFF,
        timestamp=disnake.utils.utcnow()
    )
    embed.set_image(url)
    return embed


class Avatar(commands.Cog):
    bot: commands.Bot = None
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
   
    @commands.command(aliases=["a", "av", "avt"])
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    async def avatar(self, ctx: commands.Context) -> None:
        # Pass --global or -g flag if you need to get global avatar
        msg = ctx.message.content
        parse_arg = msg.split()
        _global = False
        for i in ("-g", "--global"):
            try:
                parse_arg.index(i)
                _global = True
                break
            except: pass
        user_id = parse_userid(msg)
        if user_id is None: user_id = str(ctx.author.id)
        if not _global:
            try:
                user = ctx.guild.get_member(int(user_id))
                if user is None: raise Exception()
                return await ctx.reply(
                    embed = build_avatar_embed(user.display_name, user.display_avatar.url, _global),
                    view = build_button_table(True, str(user.id))
                )
            except: pass
        info = await get_user_global_info(self.bot, user_id)
        if info == None: return await ctx.reply(embed=USER_NOT_FOUND_EMBED)
        if info.avatar_id == None: return await ctx.reply(embed=USER_NO_AVATAR_EMBED)
        url = f"https://cdn.discordapp.com/avatars/{info.id}/{info.avatar_id}.{'gif' if info.avatar_id.startswith('a_') else 'png'}?size=1024"
        await ctx.reply(
            embed = build_avatar_embed(info.name, url, _global),
            view = build_button_table(True, info.id)
        )
    
    
    @commands.command(aliases=["bn"])
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    async def banner(self, ctx: commands.Context):
        msg = ctx.message.content
        user_id = parse_userid(msg)
        if user_id is None: user_id = str(ctx.author.id)
        info = await get_user_global_info(self.bot, user_id)
        if info == None: return await ctx.reply(embed=USER_NOT_FOUND_EMBED)
        if info.banner_id == None: return await ctx.reply(embed=USER_NO_BANNER_EMBED)
        url = f"https://cdn.discordapp.com/banners/{info.id}/{info.banner_id}.{'gif' if info.banner_id.startswith('a_') else 'png'}?size=4096"
        await ctx.reply(
            embed = build_banner_embed(info.name, url),
            view = build_button_table(False, info.id)
        )
            
            
    @commands.slash_command(
        name="avatar",
        description="Hiển thị avatar của người dùng",
        options=[
            disnake.Option(
                name="user",
                description="Nhập ID người dùng hoặc mention người dùng (Bỏ trống để lấy avatar của chính bạn)",
                type=disnake.OptionType.string,
            ),
            disnake.Option(
                name="global",
                description="Lấy avatar toàn cầu (Mặc định: Không)",
                type=disnake.OptionType.boolean,
                choices=[
                    disnake.OptionChoice("Có (Lấy avatar toàn cầu)", True),
                    disnake.OptionChoice("Không (Lấy avatar máy chủ)", False),
                ]
            ),
            disnake.Option(
                name="ephemeral",
                description="Chỉ hiển thị phản hồi với riêng bạn (Mặc định: Không)",
                type=disnake.OptionType.boolean,
                choices=[
                    disnake.OptionChoice("Có (Phản hồi riêng tư)", True),
                    disnake.OptionChoice("Không (Phản hồi công khai)", False),
                ]
            )
        ]
    )
    async def avatar_slash(self, inter: disnake.ApplicationCommandInteraction):
        msg = inter.options.get("user", "")
        _global = inter.options.get("global", False)
        _ephemeral = inter.options.get("ephemeral", False)
        user_id = parse_userid(msg)
        if user_id is None: user_id = str(inter.author.id)
        if not _global:
            try:
                user = inter.guild.get_member(int(user_id))
                if user is None: raise Exception()
                return await inter.response.send_message(
                    embed = build_avatar_embed(user.display_name, user.display_avatar.url, _global),
                    view = build_button_table(True, str(user.id)),
                    ephemeral = _ephemeral
                )
            except: pass
        info = await get_user_global_info(self.bot, user_id)
        if info == None: return await inter.response.send_message(embed=USER_NOT_FOUND_EMBED)
        if info.avatar_id == None: return await inter.response.send_message(embed=USER_NO_AVATAR_EMBED)
        url = f"https://cdn.discordapp.com/avatars/{info.id}/{info.avatar_id}.{'gif' if info.avatar_id.startswith('a_') else 'png'}?size=1024"
        await inter.response.send_message(
            embed = build_avatar_embed(info.name, url, _global),
            view = build_button_table(True, info.id),
            ephemeral = _ephemeral
        )
            
    
    @commands.slash_command(
        name="banner",
        description="Hiển thị banner của người dùng",
        options=[
            disnake.Option(
                name="user",
                description="Nhập ID người dùng hoặc mention người dùng (Bỏ trống để lấy banner của chính bạn)",
                type=disnake.OptionType.string,
            ),
            disnake.Option(
                name="ephemeral",
                description="Chỉ hiển thị phản hồi với riêng bạn (Mặc định: Không)",
                type=disnake.OptionType.boolean,
                choices=[
                    disnake.OptionChoice("Có (Phản hồi riêng tư)", True),
                    disnake.OptionChoice("Không (Phản hồi công khai)", False),
                ]
            )
        ]
    )
    async def banner_slash(self, inter: disnake.ApplicationCommandInteraction):
        msg = inter.options.get("user", "")
        _ephemeral = inter.options.get("ephemeral", False)
        user_id = parse_userid(msg)
        if user_id is None: user_id = str(inter.author.id)
        info = await get_user_global_info(self.bot, user_id)
        if info == None: return await inter.response.send_message(embed=USER_NOT_FOUND_EMBED)
        if info.banner_id == None: return await inter.response.send_message(embed=USER_NO_BANNER_EMBED)
        url = f"https://cdn.discordapp.com/banners/{info.id}/{info.banner_id}.{'gif' if info.banner_id.startswith('a_') else 'png'}?size=1024"
        await inter.response.send_message(
            embed = build_banner_embed(info.name, url),
            view = build_button_table(False, info.id),
            ephemeral = _ephemeral
        )
        
        
    async def avatar_btn(self, event: disnake.MessageInteraction, user_id: str, _global: bool = False):
        if not _global:
            try:
                user = event.guild.get_member(int(user_id))
                if user is None: raise Exception()
                return await event.response.edit_message(
                    embed = build_avatar_embed(user.display_name, user.display_avatar.url, _global),
                    view = build_button_table(True, str(user.id))
                )
            except: pass
        info = await get_user_global_info(self.bot, user_id)
        if info == None: return await event.response.edit_message(embed=USER_NOT_FOUND_EMBED)
        if info.avatar_id == None: return await event.response.edit_message(embed=USER_NO_AVATAR_EMBED)
        url =  f"https://cdn.discordapp.com/avatars/{info.id}/{info.avatar_id}.{'gif' if info.avatar_id.startswith('a_') else 'png'}?size=1024"
        await event.response.edit_message(
            embed = build_avatar_embed(info.name, url, _global),
            view = build_button_table(True, info.id)
        )
        
    
    async def banner_btn(self, event: disnake.MessageInteraction, user_id: str):
        info = await get_user_global_info(self.bot, user_id)
        if info == None: return await event.response.edit_message(embed=USER_NOT_FOUND_EMBED)
        if info.banner_id == None: return await event.response.edit_message(embed=USER_NO_BANNER_EMBED)
        url = f"https://cdn.discordapp.com/banners/{info.id}/{info.banner_id}.{'gif' if info.banner_id.startswith('a_') else 'png'}?size=4096"
        await event.response.edit_message(
            embed = build_banner_embed(info.name, url),
            view = build_button_table(False, info.id)
        )
    
    
    @commands.Cog.listener("on_button_click")
    async def button_event(self, event: disnake.MessageInteraction):
        action_id = event.data.custom_id
        if re.match(r"avatar_\d{18,20}(_g)?", action_id) is not None: return await self.avatar_btn(event, action_id.split("_")[1], action_id.endswith("_g"))
        elif re.match(r"banner_\d{18,20}", action_id) is not None: return await self.banner_btn(event, action_id.split("_")[1])
        elif action_id == "delete":  await event.message.delete()
        

def setup(bot: commands.Bot):
    bot.add_cog(Avatar(bot))
