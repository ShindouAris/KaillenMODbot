from disnake import Webhook
import aiohttp


class Process_webhook():
    def __init__(self):
        self.__init__ = None
    
    async def process_webhook(self, webhook_uri, embed):
        async with aiohttp.ClientSession() as session:
            webhok = Webhook.from_url(webhook_uri, session=session)
            await webhok.send(embed=embed, username="Kaillen Mod bot", avatar_url="https://i.ibb.co/XDNRtjC/bot-iocn.png")