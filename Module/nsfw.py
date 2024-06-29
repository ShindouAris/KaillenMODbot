from disnake.ext import commands
from disnake import Option, OptionChoice, Embed, ApplicationCommandInteraction
from utils.ClientUser import ClientUser
import requests

desc_prefix = "[🔞 Nsfw]"
TagList = ["waifu", "neko", "trap", "blowjob"]
base_api = "https://api.waifu.pics/"


async def make_request(type: str, category: str) -> str:

    resp = requests.get(base_api + type + "/" + category)
    if resp.status_code != 200:
        return None
    return resp.json()["url"]


class Nsfw(commands.Cog):
    def __init__(self, client: ClientUser):
        self.client = client
        # base_api = "https://api.waifu.pics/"
        


    @commands.is_nsfw()
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.slash_command(name="nsfw", 
                            description=f"{desc_prefix} nsfw nuh uh", 
                            options=[Option(name="tag", description="something idk")])
    async def nsfw(self, ctx: ApplicationCommandInteraction, tag: str = "waifu"):
        await ctx.response.defer()
        pic = await make_request("nsfw", tag)
        if pic is None: return ctx.edit_original_response("⚠️")
        emb = Embed(title="😋")
        emb.set_image(pic)
        await ctx.edit_original_response(embed=emb)

    @nsfw.autocomplete("tag")
    async def nsfwautocopml(inter, tags: str):
        tags = tags.lower()
        return [tags for tags in TagList]


def setup(userClient: ClientUser): userClient.add_cog(Nsfw(userClient))
    

