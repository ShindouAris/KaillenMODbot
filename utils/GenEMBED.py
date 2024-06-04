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