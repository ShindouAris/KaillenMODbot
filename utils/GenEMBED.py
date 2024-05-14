import disnake
from disnake.ext import commands

import pytz # if you don't have this, do pip install pytz, it's used for timezones
from datetime import datetime

HCM = pytz.timezone('Asia/Ho_Chi_Minh')


class Embed():
    def __init__(self):
        pass

    # Embeds stuff
    def gen_error_embed(message: str):
        embed = disnake.Embed(
            title="❌ Đã xảy ra lỗi",
            description=message,
            color=disnake.Color.red()
        )
        embed.set_image(url="https://media.discordapp.net/attachments/1158024306006171722/1172548248712519690/New_Project_12_1F9D8FE.gif?ex=6560b7a7&is=654e42a7&hm=3e1ad259424752013faa667b7fd45f93dece5975d3eccdf4ba773f498fc02963&")
        return embed

    def gen_nouser_embed(message: str):
        embed = disnake.Embed(
            title="❌ Không tìm thấy người dùng",
            description=message,
            color=disnake.Color.red()
        )
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1158024306006171722/1172548248712519690/New_Project_12_1F9D8FE.gif?ex=6560b7a7&is=654e42a7&hm=3e1ad259424752013faa667b7fd45f93dece5975d3eccdf4ba773f498fc02963&")
        embed.set_image(url="https://media.discordapp.net/attachments/1158024306006171722/1172548248712519690/New_Project_12_1F9D8FE.gif?ex=6560b7a7&is=654e42a7&hm=3e1ad259424752013faa667b7fd45f93dece5975d3eccdf4ba773f498fc02963&")
        return embed

    def gen_banned_embed(time: int, reason: str):
        embed = disnake.Embed(
            title="Tài khoản bị cấm!",
            description=f"Tài khoản của bạn đã bị cấm từ {disnake.utils.format_dt(disnake.utils.utcfromtimestamp(time), style='R')} với lý do: {reason}",
            color=disnake.Color.red()
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1117362735911538768/1131107858046533722/fail.png")
        return embed

    # PREMIUM EMBEDS
    def gen_embed(title: str, description: str):
        embed = disnake.Embed(
            title=title,
            description=description,
            color=disnake.Color.red()
        )
        embed.set_footer(text="Premium Guild", icon_url="")
        embed.set_thumbnail(url="")
        return embed

    # NON PREMIUM EMBEDS
    def gen_NON_embed(title: str, description: str):
        embed = disnake.Embed(
            title=title,
            description=description,
            color=disnake.Color.red()
        )
        embed.set_footer(text="Powered by ShinroChisadin || Upgrade lên Premium để xóa dòng này")
        embed.set_thumbnail(url="")
        return embed
    
    def gen_leave_embed(title: str, description: str, image_url: str, guild_name: str):
        embed = disnake.Embed(
            title=title,
            description=description,
            color=disnake.Color.red()
        )
        embed.set_footer(text=datetime.now(HCM).strftime("%d/%m/%Y %H:%M:%S") + " | " + guild_name)
        embed.set_thumbnail(url=image_url)
        return embed 
    
    def gen_join_embed(title: str, description: str, image_url: str, guild_name: str):
        embed = disnake.Embed(
            title=title,
            description=description,
            color=disnake.Color.red()
        )
        embed.set_footer(text=datetime.now(HCM).strftime("%d/%m/%Y %H:%M:%S") + " | " + guild_name)
        embed.set_thumbnail(url=image_url)
        return embed