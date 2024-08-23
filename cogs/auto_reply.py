import discord
from discord.ext import commands

class Auto_Reply(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.triggers_responses = {
            "Hi": "Hello, welcome!"
        }
        
   
            
async def setup(client: commands.Bot) -> None:
    await client.add_cog(Auto_Reply(client))
