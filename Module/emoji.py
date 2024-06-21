import disnake
from disnake import OptionType
from disnake import Option, ApplicationCommandInteraction, OptionChoice
from disnake.ext import commands

from random import randint
import aiohttp
import re
from urllib.parse import urlparse
from utils.client import BotCore
from asyncio import sleep
class emoji(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot

    @commands.slash_command(name="emoji", description="Nhóm lệnh quản lý emoji trên server của bạn")
    async def emoji(self, ctx): pass

    @emoji.sub_command(name="create",
                       description="Tạo emoji mới",
                       options=[
                            Option(name="url", description="Đường dẫn ảnh để tạo emoji", type=OptionType.string, required=True),
                            Option(name="name", description="Tên emoji", type=OptionType.string, required=False), 
                            Option(name="private", description="Chế độ riêng tư", type=OptionType.boolean, required=False, choices=[
                OptionChoice(name="Bật", value=True),
                OptionChoice(name="Tắt", value=False)
            ])
                          ])
    async def emoji_create(self, ctx: ApplicationCommandInteraction, url: str = None, name: str = None, private: bool = False):
        await ctx.response.defer(ephemeral=private)  
        if url is None:
            embed = disnake.Embed(title="❌ Bạn phải cung cấp tham số `url`", color=disnake.Color.red())
            await ctx.edit_original_message(embed=embed)
            return
        
        if "cdn.discordapp.com" in url:
            await ctx.edit_original_response("❌ Discord chặn link rồi, hãy thử upload lên các trang khác như imgur, imgbb,... nhé")    
            return
        
        list_emoji = []

        if name is None: 
            name = f"emoji_{str(randint(1000, 9999)).zfill(4)}"

        if url is not None:
            list_url = url.split(' ')
            async def check_url(url):
                result = urlparse(url)
                return all([result.scheme, result.netloc])
            for items in list_url:
                items = items.split('?')[0]
                if await check_url(items) and items.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    list_emoji.append({
                        "name": name,
                        "url": items
                        })
        if len(list_emoji) == 0:
            embed = disnake.Embed(
                title="<:AyakaAnnoyed:1135418690632957993> Không tìm thấy emoji nào trong yêu cầu của bạn",
                color=disnake.Color.red()
            )
            await ctx.edit_original_response(embed=embed)
            return
        try:
            for i in range(len(list_emoji)):
                emoji = list_emoji[i]
                async with aiohttp.ClientSession() as session:
                    async with session.get(emoji["url"], allow_redirects=False) as resp:
                        if resp.status != 200:
                            embed = disnake.Embed(
                                title="<:AyakaAnnoyed:1135418690632957993> Đã xảy ra lỗi!",
                                color=disnake.Colour.red(),
                            )
                            await ctx.edit_original_response(embed=embed)
                            print(resp.status)
                            return
                        img = await resp.read()
                await ctx.guild.create_custom_emoji(
                    name=emoji["name"],
                    image=img
                )
                embed = disnake.Embed(
                    title=f"<:AyakaKiss:1104064345249419405> Đã thêm emoji thành công! {i+1}/{len(list_emoji)}",
                    color=disnake.Colour.green(),
                )
                embed.set_author(
                    name=emoji["name"],
                    icon_url=emoji["url"]
                )
                embed.set_thumbnail(
                    url=emoji["url"]
                )
                await ctx.edit_original_response(embed=embed)
        except:
            embed = disnake.Embed(
                title="<:AyakaAnnoyed:1135418690632957993> Đã xảy ra lỗi!",
                color=disnake.Colour.red(),
            )
            await ctx.edit_original_response(embed=embed)
            
    # @commands.bot_has_guild_permissions(manage_emojis=True)
    @commands.slash_command(
        name="add_emoji",
        description="Thêm emoji vào server",
        options = [disnake.Option(
            name = "emoji",
            description = "Từ emoji mà bạn có thể sử dụng",
            type = OptionType.string,
            required = True
            ),
            disnake.Option(name="private", description="Chế độ riêng tư (Yêu cầu bạn phải bật nếu bạn ở trên kênh chat chính)", type=OptionType.boolean, required=False, choices=[
                OptionChoice(name="Bật", value=True),
                OptionChoice(name="Tắt", value=False)
            ])
            ])
    async def add_emoji(self, ctx: disnake.ApplicationCommandInteraction, emoji: str = None, private: bool = False):
        await ctx.response.defer(ephemeral=private)
        if emoji is None:
            embed = disnake.Embed(
                title="<:AyakaAnnoyed:1135418690632957993> Bạn phải cung cấp ít nhất một trong hai tham số `emoji` hoặc `url`",
                color=disnake.Color.red()
            )
            await ctx.edit_original_response(embed=embed)
            return
        list_emoji = []
        if emoji is not None:
            emoji_pattern = re.compile(r'<(a?:.*?:\d+)>')
            emoji_list = emoji_pattern.findall(emoji)
            for items in emoji_list:
                emoji_name = items.split(':')[1]
                emoji_id = items.split(':')[2]
                emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.{'gif' if items.startswith('a') else 'png'}"
                list_emoji.append({
                    "name": emoji_name,
                    "url": emoji_url
                    })
        
        if len(list_emoji) == 0:
            embed = disnake.Embed(
                title="<:AyakaAnnoyed:1135418690632957993> Không tìm thấy emoji nào trong yêu cầu của bạn",
                color=disnake.Color.red()
            )
            await ctx.edit_original_response(embed=embed)
            return
        try:
            for i in range(len(list_emoji)):
                emoji = list_emoji[i]
                async with aiohttp.ClientSession() as session:
                    async with session.get(emoji["url"]) as resp:
                        if resp.status != 200:
                            embed = disnake.Embed(
                                title="<:AyakaAnnoyed:1135418690632957993> Đã xảy ra lỗi!",
                                color=disnake.Colour.red(),
                            )
                            await ctx.edit_original_response(embed=embed)
                            return
                        img = await resp.read()

                await ctx.guild.create_custom_emoji(
                    name=emoji["name"],
                    image=img, reason=f"{ctx.author.name} đã copy emoji này :E"
                )
                embed = disnake.Embed(
                    title=f"<a:a_emoji169:1204063046717145128> Đã thêm emoji thành công! {i+1}/{len(list_emoji)}",
                    color=disnake.Colour.green(),
                )
                embed.set_author(
                    name=emoji["name"],
                    icon_url=emoji["url"]
                )
                embed.set_thumbnail(
                    url=emoji["url"]
                )
                await ctx.edit_original_response(embed=embed)
                await sleep(3)
        except Exception as e:
            if "Missing Permissions" in str(e):
                await ctx.edit_original_response("Tớ thiếu quyền, hãy đảm bảo bạn đã bật 2 quyền sau trong role của tớ :< \n https://i.ibb.co/BNY7NHk/image.png")
                return

            if "Maximum number of emojis reached" in str(e):
                await ctx.edit_original_response("Server của cậu hết slot rồi, xóa bớt trước khi thêm lại nhé :<", components=None)
                return

            embed = disnake.Embed(
                title="<:AyakaAnnoyed:1135418690632957993> Đã xảy ra lỗi!",
                description=e,
                color=disnake.Colour.red(),
            )
            await ctx.edit_original_response(embed=embed)

def setup(bot: BotCore):
    bot.add_cog(emoji(bot))
