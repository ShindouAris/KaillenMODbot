import disnake
import asyncio
from disnake import OptionType, Option
from disnake.ext import commands
import sqlite3
from utils.ClientUser import ClientUser

class voice(commands.Cog):
    def __init__(self, bot):
        self.bot: ClientUser = bot
        self.is_hide: bool = False

    @commands.Cog.listener("on_voice_state_update")
    async def voicechatfuncion(self, member, before, after):
        vc_embed = disnake.Embed(title="Xin chào", description="",color=0x7289da)
        vc_embed.add_field(name=f'**Các lệnh của bot**', value=f'**Khóa kênh của bạn bằng cách sử dụng lệnh sau:**\n\n`.voice lock`\n\n ----------\n'
                         f'**Mở khóa kênh của bạn bằng lệnh sau:**\n\n`.voice lock`\n\n ----------\n\n'
                         f'**Thay đổi tên kênh của bạn bằng lệnh sau:**\n\n`.voice name <tên>`\n- -----------\n'
                         f'**Thay đổi giới hạn kênh của bạn bằng cách sử dụng lệnh sau:**\n\n` .voice limit <số>`\n---- --------\n'
                         f'**Cho phép người dùng tham gia bằng cách sử dụng lệnh sau:**\n\n`.voice permit @ai đó`\n-----------\n'
                         f'**Xác nhận quyền sở hữu kênh sau khi chủ sở hữu rời đi:**\n`.voice claim`\n------ ------\n'
                         f'**Xóa quyền và người dùng khỏi kênh của bạn bằng lệnh sau:**\n`.voice reject @ai đó`\n', inline='false')
        conn = sqlite3.connect('voice.db')
        c = conn.cursor()
        guildID = member.guild.id
        c.execute("SELECT voiceChannelID FROM guild WHERE guildID = ?", (guildID,))
        voice=c.fetchone()
        if voice is None:
            pass
        else:
            voiceID = voice[0]
            try:
                if after.channel.id == voiceID:
                    c.execute("SELECT * FROM voiceChannel WHERE userID = ?", (member.id,))
                    cooldown=c.fetchone()
                    if cooldown != None:
                        await member.send("Bạn tạo kênh quá nhanh!")
                        await asyncio.sleep(3)
                        return
                        
                    c.execute("SELECT voiceCategoryID FROM guild WHERE guildID = ?", (guildID,))
                    voice=c.fetchone()
                    c.execute("SELECT channelName, channelLimit FROM userSettings WHERE userID = ?", (member.id,))
                    setting=c.fetchone()
                    c.execute("SELECT channelLimit FROM guildSettings WHERE guildID = ?", (guildID,))
                    guildSetting=c.fetchone()
                    if setting is None:
                        name = f"Kênh của {member.name}"
                        if guildSetting is None:
                            limit = 0
                        else:
                            limit = guildSetting[0]
                    else:
                        if guildSetting is None:
                            name = setting[0]
                            limit = setting[1]
                        elif guildSetting is not None and setting[1] == 0:
                            name = setting[0]
                            limit = guildSetting[0]
                        else:
                            name = setting[0]
                            limit = setting[1]
                    categoryID = voice[0]
                    id = member.id
                    category = self.bot.get_channel(categoryID)
                    channel2 = await member.guild.create_voice_channel(name,category=category)
                    channelID = channel2.id
                    await member.move_to(channel2)
                    await channel2.set_permissions(self.bot.user, connect=True,read_messages=True)
                    await channel2.set_permissions(member, connect=True,read_messages=True)
                    await channel2.send(embed=vc_embed)
                    await channel2.edit(name= name, user_limit = limit)
                    c.execute("INSERT INTO voiceChannel VALUES (?, ?)", (id,channelID))
                    conn.commit()
                    def check(a,b,c):
                        return len(channel2.members) == 0
                    await self.bot.wait_for('voice_state_update', check=check)
                    await channel2.delete()
                    await asyncio.sleep(3)
                    c.execute('DELETE FROM voiceChannel WHERE userID=?', (id,))
            except:
                pass
        conn.commit()
        conn.close()

    @commands.slash_command()
    async def help(self, ctx: disnake.ApplicationCommandInteraction):
        vc_embed = disnake.Embed(title="Xin chào", description="",color=0x7289da)
        vc_embed.set_author(name=f"{ctx.guild.me.display_name}",url="https://discordbots.org/bot/472911936951156740", icon_url=f"{ctx.guild.me.display_avatar.url}")
        vc_embed.add_field(name=f'**Các lệnh của bot**', value=f'**Khóa kênh của bạn bằng cách sử dụng lệnh sau:**\n\n`.voice lock`\n\n ----------\n'
                         f'**Mở khóa kênh của bạn bằng lệnh sau:**\n\n`.voice lock`\n\n ----------\n\n'
                         f'**Thay đổi tên kênh của bạn bằng lệnh sau:**\n\n`.voice name <tên>`\n- -----------\n'
                         f'**Thay đổi giới hạn kênh của bạn bằng cách sử dụng lệnh sau:**\n\n` .voice limit <số>`\n---- --------\n'
                         f'**Cho phép người dùng tham gia bằng cách sử dụng lệnh sau:**\n\n`.voice permit @person`\n-----------\n'
                         f'**Xác nhận quyền sở hữu kênh sau khi chủ sở hữu rời đi:**\n`.voice claim`\n------ ------\n'
                         f'**Xóa quyền và người dùng khỏi kênh của bạn bằng lệnh sau:**\n`.voice reject @person`\n', inline='false')
        await ctx.response.send_message(embed=vc_embed)

    @commands.slash_command(name="default_setup", description="Tạo kênh join to create theo cài đặt mặc định")
    async def vc(self, ctx: disnake.ApplicationCommandInteraction):
                await ctx.response.defer(ephemeral=True)
                conn = sqlite3.connect('voice.db')
                c = conn.cursor()
                guildID = ctx.guild.id
                id = ctx.author.id
                new_cat = await ctx.guild.create_category_channel("Kênh Thoại")
                channel = await ctx.guild.create_voice_channel(name="Tham gia để tạo kênh 🔊", category=new_cat)
                c.execute("SELECT * FROM guild WHERE guildID = ? AND ownerID=?", (guildID, id))
                voice=c.fetchone()
                if voice is None:
                    c.execute ("INSERT INTO guild VALUES (?, ?, ?, ?)",(guildID,id,channel.id,new_cat.id))
                    await ctx.edit_original_response("Đã thiết đặt thành công")
                else:
                    c.execute ("UPDATE guild SET guildID = ?, ownerID = ?, voiceChannelID = ?, voiceCategoryID = ? WHERE guildID = ?",(guildID,id,channel.id,new_cat.id, guildID))
                    await ctx.edit_original_response("Đã thiết đặt thành công")
                conn.commit()
                conn.close()

    @commands.slash_command(description="Khóa kênh của bạn để không ai khác ngoài bạn có thể kết nối vào")
    async def lock(self, ctx: disnake.ApplicationCommandInteraction):
        await ctx.response.defer()
        user_channel = ctx.author.voice.channel
        if user_channel == None:
            await ctx.edit_original_response(f"{ctx.author.mention} Bạn không ở trong một kênh giọng nói nào cả." )
        conn = sqlite3.connect('voice.db')
        c = conn.cursor()
        id = ctx.author.id
        c.execute("SELECT voiceID FROM voiceChannel WHERE userID = ?", (id,))
        voice=c.fetchone()
        if voice is None:
            await ctx.edit_original_response(f"{ctx.author.mention} Bạn không sở hữu kênh." )
        else:
            channelID = voice[0]
            role = ctx.guild.default_role
            channel = self.bot.get_channel(channelID)
            await channel.set_permissions(role, connect=False)
            await ctx.edit_original_response(f'{ctx.author.mention} kênh đã được khóa! 🔒' )
        conn.commit()
        conn.close()
        
    @commands.slash_command(description="Ẩn kênh của bạn")
    async def hide(self, ctx: disnake.ApplicationCommandInteraction):
        await ctx.response.defer()
        user_channel = ctx.author.voice.channel
        if user_channel == None:
            await ctx.edit_original_response(f"{ctx.author.mention} Bạn không ở trong một kênh giọng nói nào cả." )
        conn = sqlite3.connect('voice.db')
        c = conn.cursor()
        id = ctx.author.id
        c.execute("SELECT voiceID FROM voiceChannel WHERE userID = ?", (id,))
        voice=c.fetchone()
        if voice is None:
            await ctx.edit_original_response(f"{ctx.author.mention} Bạn không sở hữu kênh." )
            return
        ovr = disnake.PermissionOverwrite()
        ovr.view_channel = False
        self.is_hide = True
        await ctx.channel.set_permissions(overwrite=ovr, target=ctx.guild.default_role)
        await ctx.edit_original_response(f"Đã ẩn kênh của bạn")
    
    @commands.slash_command(description="Hiện kênh của bạn nếu nó đang ẩn")
    async def unhide(self, ctx: disnake.ApplicationCommandInteraction):
        await ctx.response.defer()
        if not self.is_hide:
            await ctx.edit_original_response("Kênh không bị ẩn")
            return
        user_channel = ctx.author.voice.channel
        if user_channel == None:
            await ctx.edit_original_response(f"{ctx.author.mention} Bạn không ở trong một kênh giọng nói nào cả." )
        conn = sqlite3.connect('voice.db')
        c = conn.cursor()
        id = ctx.author.id
        c.execute("SELECT voiceID FROM voiceChannel WHERE userID = ?", (id,))
        voice=c.fetchone()
        if voice is None:
            await ctx.edit_original_response(f"{ctx.author.mention} Bạn không sở hữu kênh." )
            return
        ovr = disnake.PermissionOverwrite()
        ovr.view_channel = True
        self.is_hide = False
        await ctx.channel.set_permissions(overwrite=ovr, target=ctx.guild.default_role)
        await ctx.edit_original_response("Đã hiện lại kênh cho bạn")

    @commands.slash_command(description="Mở khóa kênh của bạn")
    async def unlock(self, ctx: disnake.ApplicationCommandInteraction):
        await ctx.response.defer()
        user_channel = ctx.author.voice.channel
        if user_channel == None:
            await ctx.edit_original_response(f"{ctx.author.mention} Bạn không ở trong một kênh giọng nói nào cả." )
        conn = sqlite3.connect('voice.db')
        c = conn.cursor()
        id = ctx.author.id
        c.execute("SELECT voiceID FROM voiceChannel WHERE userID = ?", (id,))
        voice=c.fetchone()
        if voice is None:
            await ctx.edit_original_response(f"{ctx.author.mention} Bạn không sở hữu kênh." )
        else:
            channelID = voice[0]
            role = ctx.guild.default_role
            channel = self.bot.get_channel(channelID)
            await channel.set_permissions(role, connect=True)
            await ctx.edit_original_response(f'{ctx.author.mention} kênh đã mở khóa 🔓' )
        conn.commit()
        conn.close()
        
    @commands.slash_command(name="setbitrate", options=[Option("bitrate",
                                                               "Thay đổi bitrate cho kênh thoại của bạn",
                                                               OptionType.integer,
                                                               True, max_value=96)])
    async def setbirate(self, ctx: disnake.ApplicationCommandInteraction, bitrate: int):
        await ctx.response.defer()
        user_channel = ctx.author.voice.channel
        if user_channel == None:
            await ctx.edit_original_response(f"{ctx.author.mention} Bạn không ở trong một kênh giọng nói nào cả." )
        conn = sqlite3.connect('voice.db')
        c = conn.cursor()
        id = ctx.author.id
        c.execute("SELECT voiceID FROM voiceChannel WHERE userID = ?", (id,))
        voice=c.fetchone()
        if voice is None:
            await ctx.edit_original_response(f"{ctx.author.mention} Bạn không sở hữu kênh." )
        else:
            channelID = voice[0]
            channel = ctx.guild.get_channel(channelID)
            await channel.bitrate(bitrate)
            await ctx.edit_original_response(f"Đã thay đổi bitrate của kênh thành {bitrate}")
        conn.commit()
        conn.close()

    @commands.slash_command(description="Phê duyệt người dùng nào đó vào kênh", options=[Option("member", 
                                                                                                description="Người dùng để cho phép",
                                                                                                type=OptionType.user,
                                                                                                required=True)])
    async def allow(self, ctx: disnake.ApplicationCommandInteraction, member : disnake.Member):
        await ctx.response.defer()
        user_channel = ctx.author.voice.channel
        if user_channel == None:
            await ctx.edit_original_response(f"{ctx.author.mention} Bạn không ở trong một kênh giọng nói nào cả." )
        conn = sqlite3.connect('voice.db')
        c = conn.cursor()
        id = ctx.author.id
        c.execute("SELECT voiceID FROM voiceChannel WHERE userID = ?", (id,))
        voice=c.fetchone()
        if voice is None:
            await ctx.edit_original_response(f"{ctx.author.mention} Bạn không sở hữu kênh này.")
        else:
            channelID = voice[0]
            channel = self.bot.get_channel(channelID)
            await channel.set_permissions(member, connect=True)
            await ctx.edit_original_response(f'{ctx.author.mention} Bạn đã cho phép {member.name} truy cập vào kênh. ✅' )
        conn.commit()
        conn.close()

    @commands.slash_command(description="Từ chối người dùng nào đó vào kênh", options=[Option("member", 
                                                                                                description="Người dùng để cho phép",
                                                                                                type=OptionType.user,
                                                                                                required=True)])
    async def reject(self, ctx: disnake.ApplicationCommandInteraction, member : disnake.Member):
        await ctx.response.defer()
        user_channel = ctx.author.voice.channel
        if user_channel == None:
            await ctx.edit_original_response(f"{ctx.author.mention} Bạn không ở trong một kênh giọng nói nào cả." )
        conn = sqlite3.connect('voice.db')
        c = conn.cursor()
        id = ctx.author.id
        guildID = ctx.guild.id
        c.execute("SELECT voiceID FROM voiceChannel WHERE userID = ?", (id,))
        voice=c.fetchone()
        if voice is None:
            await ctx.edit_original_response(f"{ctx.author.mention} Bạn không sở hữu kênh này." )
        else:
            channelID = voice[0]
            channel = self.bot.get_channel(channelID)
            for members in channel.members:
                if members.id == member.id:
                    c.execute("SELECT voiceChannelID FROM guild WHERE guildID = ?", (guildID,))
                    voice=c.fetchone()
                    channel2 = self.bot.get_channel(voice[0])
                    await member.move_to(channel2)
            await channel.set_permissions(member, connect=False,read_messages=True)
            await ctx.edit_original_response(f'{ctx.author.mention} Bạn đã từ chối {member.name} truy cập kênh. ❌' )
        conn.commit()
        conn.close()



    @commands.slash_command(description="Giới hạn số người dùng trong một kênh", options=[Option("limit", 
                                                                                                description="Giới hạn của kênh (đặt là 0 có nghĩa là tắt giới hạn)",
                                                                                                type=OptionType.integer,
                                                                                                max_value=99,
                                                                                                required=True)])
    async def limit(self, ctx: disnake.ApplicationCommandInteraction, limit):
        await ctx.response.defer()
        user_channel = ctx.author.voice.channel
        if user_channel == None:
            await ctx.edit_original_response(f"{ctx.author.mention} Bạn không ở trong một kênh giọng nói nào cả." )
        conn = sqlite3.connect('voice.db')
        c = conn.cursor()
        id = ctx.author.id
        c.execute("SELECT voiceID FROM voiceChannel WHERE userID = ?", (id,))
        voice=c.fetchone()
        if voice is None:
            await ctx.edit_original_response(f"{ctx.author.mention} Bạn không sở hữu kênh này." )
        else:
            channelID = voice[0]
            channel = self.bot.get_channel(channelID)
            await channel.edit(user_limit = limit)
            await ctx.edit_original_response(f'{ctx.author.mention} Bạn đã đặt giới hạn kênh là '+ '{}!'.format(limit) )
            c.execute("SELECT channelName FROM userSettings WHERE userID = ?", (id,))
            voice=c.fetchone()
            if voice is None:
                c.execute("INSERT INTO userSettings VALUES (?, ?, ?)", (id,f'{ctx.author.name}',limit))
            else:
                c.execute("UPDATE userSettings SET channelLimit = ? WHERE userID = ?", (limit, id))
        conn.commit()
        conn.close()


    @commands.slash_command(description="Đổi tên kênh thoại của bạn", options=[Option("name",
                                                                                                description="Tên mà bạn sẽ đặt cho kênh",
                                                                                                type=OptionType.string,
                                                                                                required=True)])
    async def name(self, ctx: disnake.ApplicationCommandInteraction,*, name):
        await ctx.response.defer()
        user_channel = ctx.author.voice.channel
        if user_channel == None:
            await ctx.edit_original_response(f"{ctx.author.mention} Bạn không ở trong một kênh giọng nói nào cả." )
        conn = sqlite3.connect('voice.db')
        c = conn.cursor()
        id = ctx.author.id
        c.execute("SELECT voiceID FROM voiceChannel WHERE userID = ?", (id,))
        voice=c.fetchone()
        if voice is None:
            await ctx.edit_original_response(f"{ctx.author.mention} Bạn không sở hữu kênh này." )
        else:
            channelID = voice[0]
            channel = self.bot.get_channel(channelID)
            await channel.edit(name = name)
            await ctx.edit_original_response(f'{ctx.author.mention} Bạn đã thay đổi tên kênh thành '+ '{}!'.format(name) )
            c.execute("SELECT channelName FROM userSettings WHERE userID = ?", (id,))
            voice=c.fetchone()
            if voice is None:
                c.execute("INSERT INTO userSettings VALUES (?, ?, ?)", (id,name,0))
            else:
                c.execute("UPDATE userSettings SET channelName = ? WHERE userID = ?", (name, id))
        conn.commit()
        conn.close()

    @commands.slash_command(description="Biến kênh thoại này thành của bạn")
    async def claim(self, ctx: disnake.ApplicationCommandInteraction):
        await ctx.response.defer()
        x = False
        conn = sqlite3.connect('voice.db')
        c = conn.cursor()
        user_channel = ctx.author.voice.channel
        if user_channel == None:
            await ctx.edit_original_response(f"{ctx.author.mention} Bạn không ở trong một kênh giọng nói nào cả." )
        else:
            id = ctx.author.id
            c.execute("SELECT userID FROM voiceChannel WHERE voiceID = ?", (user_channel.id,))
            voice=c.fetchone()
            if voice is None:
                await ctx.channel.send(f"{ctx.author.mention} Bạn không thể sở hữu kênh đó!" )
            else:
                for data in user_channel.members:
                    if data.id == voice[0]:
                        owner = ctx.guild.get_member(voice [0])
                        await ctx.edit_original_response(f"{ctx.author.mention} Kênh này đã được sở hữu bởi {owner.mention}!" )
                        x = True
                if x == False:
                    await ctx.edit_original_response(f"{ctx.author.mention} Bây giờ bạn là chủ sở hữu của kênh!" )
                    c.execute("UPDATE voiceChannel SET userID = ? WHERE voiceID = ?", (id, user_channel.id))
            conn.commit()
            conn.close()


def setup(bot: ClientUser):
    bot.add_cog(voice(bot))
