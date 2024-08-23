import discord
import discord.ui
from discord.ui import *
from discord import *
from discord.ext import commands
import json
import os
import asyncio

intents = Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True

client = commands.Bot(command_prefix="!", intents=intents, description="Hi!")

@client.event
async def setup_hook():
    for ext in os.listdir("./cogs"):
        if ext.endswith(".py"):
            try:
                await client.load_extension(f"cogs.{ext[:-3]}")
                print(f"Loaded: {ext[:-3]}")
            except Exception as e:
                print(f"Failed to load extension {ext[:-3]}: {e}")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name="Server"))
    print("Bot Is Online Now!")
    print("-------------------------------")
    try:
        client.add_view(OPEN_TICKET())
        
        synced = await client.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)


class OPEN_TICKET(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green, custom_id="open")
    async def _open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        admin_role = interaction.guild.get_role() #Admin's role

        overwrites = {
            interaction.user: discord.PermissionOverwrite(view_channel=True),
            admin_role: discord.PermissionOverwrite(view_channel=True),
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False)
        }

        category = interaction.guild.get_channel() #Category"s id
        channel = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user.name}", category=category, overwrites=overwrites)
        await interaction.response.send_message(f"created ticket - <#{channel.id}>", ephemeral=True)

        embed = discord.Embed(title="", description="Welcome, thank you for choosing our server for a unique experience. Please write your complete request so that the administrators can arrive as soon as possible!", color=discord.Color.dark_purple())
        await channel.send(embed=embed)
       
@client.event
async def on_member_join(member: discord.Member):
    try:
        guild = member.guild
        Member_Role = discord.utils.get(guild.roles, id="Role id") 
        await member.add_roles(Member_Role)        
        channel_id = client.get_channel()#channel id
        await channel_id.send(f"Hi {member.mention}")
        embed = discord.Embed(title="", description="")
        embed.set_author(icon_url=member.avatar.url, name=member.name)
        embed.add_field(name="", value="**Welcome to Our Server**\n", inline=False)
        embed.add_field(name="", value="", inline=False)
        embed.add_field(name="", value="**\nGood luck in our server!**")
        embed.set_image(url="Link")
        current_time = member.joined_at.strftime("%Y-%m-%d at %H:%M")
        embed.set_footer(text=f"{current_time}")
        await channel_id.send(embed=embed)
    except discord.Forbidden as e:
        print(f"Error adding role to member {member.name}: {e}")

@client.command(aliases = ["s" , "S"])
@commands.has_permissions(administrator = True)
async def setup(ctx):
    embed = discord.Embed(title="",
                        description="To Open A ticket please click the button below:",
                        color=discord.Color.dark_purple())
    embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
    view = OPEN_TICKET()
    await ctx.send(embed=embed, view=view)


with open("Config/config.json", "r") as f:
    data = json.load(f)
    TOKEN = data["TOKEN"]


async def main():
    async with client:
        await client.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
