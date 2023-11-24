import discord , typing
import time
import random
import discord.ui
from discord.ui import *
from discord import *
from discord.ext import commands  , tasks
from discord import Embed 
from discord.ext.commands import BadArgument, MissingPermissions , MissingRequiredArgument
import sqlite3
from sqlite3 import *
# Other necessary imports
from itertools import cycle
import os
import requests
import pyshorteners
import optional
import asyncio
import datetime


print(discord.__version__)



# Enable all standard intents and message content
# (prefix commands generally require message content)
intents = Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True

client = commands.Bot(command_prefix="", intents=intents , description="Hi!")


# Streaming(name="Nothing" , url="https://www.twitch.tv/hussain_301")

@client.event
async def on_ready():
    # down if i want to change status only change dnd

    # await client.change_presence(status=discord.Status.dnd, activity=discord.Game("!help"))  #playing !help

    await client.change_presence(status=discord.Status.dnd,activity=discord.Activity(type= discord.ActivityType.listening ,name="/help" )) #Lestining To !help

    #await client.change_presence(status=discord.Status.dnd,activity=discord.Streaming(name="Test" , url="https://www.twitch.tv/hussain_301")) #Streaming
    
    print("Bot Is Online Now!")
    print("-------------------------------")
    try:
        synced = await client.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)


@client.event
async def on_member_join(member):
    # ctx.send(input("Enter the channel id where you want to send welcome messages: "))
    channel_id = client.get_channel(833379508093845554)
    # channel = client.get_channel(int(channel_id))
    # img_url = "https://i.imgur.com/your_image.png" # Replace with your image url
    # , file=discord.File(img_url))
    await channel_id.send(f"Welcome {member.mention} To Our Server!")


@client.command(aliases = ["!invite" ,"!INVITE"])
async def invite(ctx):
    button = Button(label="Invite", url="https://discord.com/api/oauth2/authorize?client_id=1080195766410293389&permissions=8&scope=bot")
    view = discord.ui.View()
    view.add_item(button)
    embed = discord.Embed(
    color=discord.Colour.dark_purple(), title="", description="")
    embed.add_field(name="Invite Link:", value=f"""Press the invite button down below to add me to your server, thank you!""", inline=True)
    await ctx.reply(embed=embed , view=view)
    
    
@client.tree.command(name="invite" , description="Add Me To Your Server!")
async def invite(interaction: discord.Interaction):
    button = Button(label="Invite", url="https://discord.com/api/oauth2/authorize?client_id=1080195766410293389&permissions=8&scope=bot")
    view = discord.ui.View()
    view.add_item(button)
    embed = discord.Embed(
    color=discord.Colour.dark_purple(), title="", description="")
    embed.add_field(name="Invite Link:", value=f"""Press the invite button down below to add me to your server, thank you!""", inline=True)
    await interaction.response.send_message(embed=embed , view=view , ephemeral=False)


@client.command(aliases = ["!nick" , "!NICK"])
@commands.has_permissions(administrator = True)
@commands.has_permissions(change_nickname = True)
@commands.has_permissions(manage_nicknames = True)
async def nick(ctx, member: discord.Member ,*, nick):
    try:
        embed = discord.Embed(color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(name="Change NickName:", value=f"""Done!""", inline=True)
        await member.edit(nick=nick)
        await ctx.reply(embed = embed)
    except:
        embed = discord.Embed(color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(name="Change NickName:", value=f"""Please Target Somone Or Choose  A Nick""", inline=True)
        await ctx.reply(embed = embed)
    time.sleep(1)
    await ctx.channel.purge(limit = 2)    
    
    
    
@client.tree.command(name="nick" , description="Use To Change Nick Name")
@discord.app_commands.checks.has_permissions(manage_nicknames = True)
@discord.app_commands.checks.has_permissions(administrator = True)
@discord.app_commands.checks.has_permissions(change_nickname = True)
async def nick(interaction: discord.Interaction, member: discord.Member , nick : str or str and float):
    try:
        embed = discord.Embed(color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(name="Change NickName:", value=f"""Done!""", inline=True)
        await member.edit(nick=nick)
        await interaction.response.send_message(embed = embed , ephemeral=True)
    except:
        embed = discord.Embed(color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(name="Change NickName:", value=f"""Please Target Somone Or Choose  A Nick""", inline=True)
        await interaction.response.send_message(embed = embed , ephemeral=True)
        




@client.tree.command(name="ping" , description="Shows Bot Ping")
async def ping(interaction:discord.Interaction): #Ping slash command
    embed = discord.Embed(
        color=discord.Colour.dark_purple(), title="", description="")
    embed.add_field(
        name="Ping:", value=f"""{int(client.latency *1000)}ms""", inline=True)
    embed.set_footer(text=f'Requested by <@{interaction.user}>.', icon_url=interaction.user.avatar)
    await interaction.response.send_message(embed=embed , ephemeral=False)
    

@client.command(aliases=["!ping", "!Ping"])  # ping command
async def ping(ctx):
    embed = discord.Embed(
        color=discord.Colour.dark_purple(), title="", description="")
    embed.add_field(
        name="Ping:", value=f"""{int(client.latency *1000)}ms""", inline=True)
    await ctx.reply(embed=embed)
    



@client.command(aliases=["Hi", "HI", "هلا", "hI"])
async def hi(ctx, user):
    await ctx.send(f"Hello {user.mention}")


@client.command(aliases=["A", "a", "!avatar", "!Avatar"])
async def avatar(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    embed = discord.Embed(title=member.name + "#" + member.discriminator)
    embed.set_image(url=member.avatar)
    await ctx.send(embed=embed)
    
    
    
@client.tree.command(name="avatar", description="Show User Avatar")
async def avatar(interaction:discord.Interaction,  member:discord.User = None  ):
    member = interaction.user if not member else member
    embed = discord.Embed(title=member.name + "#" + member.discriminator)
    embed.set_image(url=member.avatar)
    await interaction.response.send_message(embed=embed , ephemeral=False)


# clear command
@client.command(aliases=["!مسح", "!Clear", "!clear", "!CLEAR"])
@commands.has_permissions(administrator = True)
async def clear(ctx, *, amount=10):
    ctx.author.guild_permissions.administrator
    await ctx.channel.purge(limit=amount + 1)
    embed = discord.Embed(
        color=discord.Colour.dark_purple(), title="", description="")
    embed.add_field(
        name="Clear:", value=f"Clear {amount} message has been successfully cleared!", inline=True)
    await ctx.send(embed=embed)
    await ctx.channel.purge(limit=1)
    
    
@client.tree.command(name="clear" ,  description="Clear Command")
@discord.app_commands.checks.has_permissions(manage_messages = True)
@discord.app_commands.checks.has_permissions(administrator = True)
@discord.app_commands.checks.bot_has_permissions(manage_messages = True)
async def clear(interaction : discord.Interaction , channel: discord.TextChannel, amount: int=10 ):
    embed = discord.Embed(color=discord.Colour.dark_purple(), title="", description="")
    embed.add_field(name="Clear:", value=f"Clear {amount} message has been successfully cleared!", inline=True)
    await channel.purge(limit=amount)
    await interaction.response.send_message(embed=embed , ephemeral=True)



@client.command(aliases=["!kick", "!Kick", "!طرد"])  # kick command
@commands.has_permissions(kick_members=True)
@commands.has_permissions(administrator = True)
async def kick(ctx, user: discord.Member = None, *, reason=None):
    try:
        await user.kick(reason=reason)
        embed = discord.Embed(
            color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(
            name="Kicked:", value=f"""The User **{user}**has been kickid! Reason = **{reason}**""", inline=True)
        await ctx.reply(embed=embed)
    except:
        embed = discord.Embed(
            color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(
            name="Kicked", value=f""" Please Target Someone """, inline=True)
        await ctx.reply(embed=embed)
    time.sleep(1)
    await ctx.channel.purge(limit=2)
    
    
@client.tree.command(name="kick" , description="To Give Someone Kick")
@discord.app_commands.checks.has_permissions(kick_members=True)
@discord.app_commands.checks.has_permissions(administrator = True)
async def kick(interaction:discord.Interaction , user:discord.Member=None , reason :str =None):
    try:
        await user.kick(reason=reason)
        embed = discord.Embed(
            color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(
            name="Kicked:", value=f"""The User **{user}**has been kickid! Reason = **{reason}**""", inline=True)
        await interaction.response.send_message(embed=embed , ephemeral=True)
    except:
        embed = discord.Embed(
            color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(
            name="Kicked", value=f""" Please Target Someone """, inline=True)
        await interaction.response.send_message(embed=embed , ephemeral=True)



@client.command(aliases=["!ban", "!Ban", "!Band", "!حظر"])  # ban command
@commands.has_permissions(ban_members=True)
@commands.has_permissions(administrator = True)
async def ban(ctx, user: discord.Member = None, *, reason=None):
    try:
        await user.ban(reason=reason)
        embed = discord.Embed(
            color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(
            name="Banned:", value=f"""The User **{user}**has been Banned! Reason = **{reason}**""", inline=True)
        await ctx.reply(embed=embed)
    except:
        embed = discord.Embed(
            color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(
            name="Banned", value=f""" Please Target Someone """, inline=True)
        await ctx.reply(embed=embed)
    time.sleep(1)
    await ctx.channel.purge(limit=2)
    
    
@client.tree.command(name="ban" , description="Give Someone Ban")  # ban command
@discord.app_commands.checks.has_permissions(ban_members=True)
@discord.app_commands.checks.has_permissions(administrator = True)
async def ban(interaction: discord.Interaction, user: discord.Member = None, reason: str = None):
    try:
        await user.ban(reason=reason)
        embed = discord.Embed(
            color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(
            name="Banned:", value=f"""The User **{user}**has been Banned! Reason = **{reason}**""", inline=True)
        await interaction.response.send_message(embed=embed ,ephemeral=True)
    except:
        embed = discord.Embed(
            color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(
            name="Banned", value=f""" Please Target Someone """, inline=True)
        await interaction.response.send_message(embed=embed , ephemeral=True)



@client.command(aliases=["!unban", "!UNBAN", "!Unband", "!UnBan", "!UnBand", "!unband", "!UNBAND"])
@commands.has_permissions(ban_members=True)
@commands.has_permissions(administrator = True)
async def unban(ctx, member: discord.User = None):
    try:
        guild = ctx.guild
        if ctx.author.guild_permissions.ban_members:
            await guild.unban(user=member)
            embed = discord.Embed(
                color=discord.Colour.dark_purple(), title="", description="")
            embed.add_field(
                name="Unban:", value=f"""The User **{member}** has been Unbanned!""", inline=True)
            await ctx.reply(embed=embed)
    except:
        embed = discord.Embed(
            color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(
            name="Unban", value=f""" Please Target Someone """, inline=True)
        await ctx.reply(embed=embed)
    time.sleep(1)
    await ctx.channel.purge(limit=2)
    
    
@client.tree.command(name="unban" , description="To Unbanned Someone")
@discord.app_commands.checks.has_permissions(ban_members=True)
@discord.app_commands.checks.has_permissions(administrator = True)
async def unban(interaction:discord.Interaction , user_id : discord.Member  = None):
    try:
        guild = interaction.guild
        if interaction.author.guild_permissions.ban_members:
            user = discord.Object(int(user_id))
            await interaction.guild.unban(user)
            embed = discord.Embed(
                color=discord.Colour.dark_purple(), title="", description="")
            embed.add_field(
                name="Unban:", value=f"""The User **{user}** has been Unbanned!""", inline=True)
            await interaction.response.send_message(embed=embed , ephemeral=True)
    except:
        embed = discord.Embed(
            color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(
            name="Unban", value=f""" Please Target Someone """, inline=True)
        await interaction.response.send_message(embed=embed , ephemeral=True)



@client.command(aliases=["!mute", "!Mute", "!MUTE"])
@commands.has_permissions(mute_members = True)
@commands.has_permissions(administrator = True)
async def mute(ctx, member: discord.Member = None):
    try:
        guild = ctx.guild
        Muted = discord.utils.get(guild.roles, name="Muted")
        if not Muted:
            Muted = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permissions(Muted, speak=False, send_messages=False)
        await member.add_roles(Muted)

        embed = discord.Embed(
            title="Mute", description=f"{member.mention} has been muted.", color=discord.Colour.dark_purple())
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(
            color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(
            name="Mute", value=f""" Please Target Someone """, inline=True)
        await ctx.reply(embed=embed)
    time.sleep(1)
    await ctx.channel.purge(limit=2)
    
    
@client.tree.command(name="mute" , description="To Give Someone Mute")
@discord.app_commands.checks.has_permissions(mute_members=True)
@discord.app_commands.checks.has_permissions(administrator = True)
async def mute(interaction: discord.Interaction, member: discord.Member = None):
    try:
        guild = interaction.guild
        Muted = discord.utils.get(guild.roles, name="Muted")
        if not Muted:
            Muted = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permissions(Muted, speak=False, send_messages=False)
        await member.add_roles(Muted)

        embed = discord.Embed(
            title="Mute", description=f"{member.mention} has been muted.", color=discord.Colour.dark_purple())
        await interaction.response.send_message(embed=embed , ephemeral=True)
    except:
        embed = discord.Embed(
            color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(
            name="Mute", value=f""" Please Target Someone """, inline=True)
        await interaction.response.send_message(embed=embed , ephemeral=True)  
    



@client.command(aliases=["!unmute", "!UNmute", "!UNMUTE", "!unMute"])
@commands.has_permissions(mute_members = True)
@commands.has_permissions(administrator = True)
async def unmute(ctx, member: discord.Member = None):
    try:
        guild = ctx.guild
        Muted = discord.utils.get(guild.roles, name="Muted")
        if Muted in member.roles:
            await member.remove_roles(Muted)
            embed = discord.Embed(
                title="Unmute", description=f"{member.mention} has been unmuted.", color=discord.Colour.dark_purple())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Unmute", description=f"{member.mention} is not muted.", color=discord.Colour.dark_purple())
            await ctx.send(embed=embed)
    except:
        embed = discord.Embed(
            color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(
            name="Unmute", value=f""" Please Target Someone """, inline=True)
        await ctx.reply(embed=embed)
    time.sleep(1)
    await ctx.channel.purge(limit=2)
    
    
    
@client.tree.command(name="unmute" , description="To Unmute Someone")
@discord.app_commands.checks.has_permissions(mute_members=True)
@discord.app_commands.checks.has_permissions(administrator = True)
async def unmute(interaction: discord.Interaction, member: discord.Member = None):
    try:
        guild = interaction.guild
        Muted = discord.utils.get(guild.roles, name="Muted")
        if Muted in member.roles:
            await member.remove_roles(Muted)
            embed = discord.Embed(
                title="Unmute", description=f"{member.mention} has been unmuted.", color=discord.Colour.dark_purple())
            await interaction.response.send_message(embed=embed , ephemeral=True)
        else:
            embed = discord.Embed(
                title="Unmute", description=f"{member.mention} is not muted.", color=discord.Colour.dark_purple())
            await interaction.response.send_message(embed=embed , ephemeral=True)
    except:
        embed = discord.Embed(
            color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(
            name="Unmute", value=f""" Please Target Someone """, inline=True)
        await interaction.response.send_message(embed=embed , ephemeral=True)





@client.command(aliases=["!server", "!serverinfo"])
async def serverinfo(ctx):
    name = str(ctx.guild.name)
    # description = str(ctx.guild.description) description=description,

    embed = discord.Embed(title=name + " Server Information",
                          color=discord.Colour.dark_purple())
    try:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    except:
        url = None

    embed.set_author(name="ServerInfo Command")

    embed.add_field(name="Server created on", value=ctx.guild.created_at.strftime(
        "%d %b %Y "), inline=False)  # %H:%M:%S for time in sec,h,min

    embed.add_field(name="Server region", value=str(
        ctx.guild.preferred_locale), inline=False)

    embed.add_field(name="Server ID", value=str(ctx.guild.id), inline=False)

    embed.add_field(name="Server owner", value=str(
        ctx.guild.owner), inline=False)

    embed.add_field(name="Members", value=str(
        ctx.guild.member_count), inline=False)

    embed.set_footer(
        text=f'Requested by <@{ctx.author}>.', icon_url=ctx.author.avatar)

    await ctx.send(embed=embed)
    
    
    
@client.tree.command(name="serverinfo" , description="Shows Server Info")
async def serverinfo(interaction: discord.Interaction):
    name = str(interaction.guild.name)
    # description = str(ctx.guild.description) description=description,

    embed = discord.Embed(title=name + " Server Information",
                          color=discord.Colour.dark_purple())
    try:
        embed.set_thumbnail(url=interaction.guild.icon.url)
    except:
        url = None

    embed.set_author(name="ServerInfo Command")

    embed.add_field(name="Server created on", value=interaction.guild.created_at.strftime(
        "%d %b %Y "), inline=False)  # %H:%M:%S for time in sec,h,min

    embed.add_field(name="Server region", value=str(
        interaction.guild.preferred_locale), inline=False)

    embed.add_field(name="Server ID", value=str(interaction.guild.id), inline=False)

    embed.add_field(name="Server owner", value=str(
        interaction.guild.owner), inline=False)

    embed.add_field(name="Members", value=str(
        interaction.guild.member_count), inline=False)

    embed.set_footer(
        text=f'Requested by <@{interaction.user}>.', icon_url=interaction.user.avatar)

    await interaction.response.send_message(embed=embed , ephemeral=False)

    


@client.command(aliases=["!user", "!userinfo"])
async def userinfo(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author

    embed = discord.Embed(title="User Information", color=discord.Colour.dark_purple())

    embed.set_author(name="UserInfo Command")

    embed.set_thumbnail(url=member.avatar.url)

    embed.add_field(name="Name", value=member.name, inline=False)

    embed.add_field(name="Nickname", value=member.nick, inline=False)

    embed.add_field(name="ID", value=member.id, inline=False)

    embed.add_field(name="Status", value=str(member.status), inline=False)

    if member.activity is not None:
        embed.add_field(name="Activity", value=str(member.activity), inline=False)

    embed.add_field(name="Roles", value=" ".join([role.mention for role in member.roles]), inline=False)

    embed.set_footer(text=f'Requested by {ctx.author.name}.', icon_url=ctx.author.avatar)

    await ctx.send(embed=embed)
    
    
    
    
@client.tree.command(name = "user")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None ):

  if member is None:
    member = interaction.user

  member_id = int(member.id)
  fetch_member = interaction.guild.get_member(member_id)

  embed = discord.Embed(title="User Information",
                        color=discord.Colour.dark_purple())

  embed.set_author(name="UserInfo Command")

  embed.set_thumbnail(url=member.display_avatar.url)

  embed.add_field(name="Name", value=member.name, inline=False)

  embed.add_field(name="Nickname", value=member.nick, inline=False)

  embed.add_field(name="ID", value=member.id, inline=False)

  embed.add_field(name="Status", value=fetch_member.status, inline=False)

  embed.add_field(name="Activity",
                  value=str(fetch_member.activity.details),
                  inline=False)

  embed.add_field(name="Roles",
                  value=" ".join([role.mention for role in member.roles]),
                  inline=False)

  embed.set_footer(text=f'Requested by <@{interaction.user}>.',
                   icon_url=interaction.user.avatar)

  await interaction.response.send_message(embed=embed, ephemeral=False)
    
    


@client.command(aliases=["!dm", "!DM", "!Dm", "!dM"])
@commands.has_permissions(administrator = True)
async def dm(ctx, member: discord.Member, *, message):
    
    try:
        embed = discord.Embed(
        title=f"Hi {member}", description=message, color=discord.Color.dark_purple())
        await member.send(embed=embed)
        embed = discord.Embed(color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(name="DM:", value=f"""Done!""", inline=True)
        await ctx.reply(embed=embed)
    except:
        embed = discord.Embed(color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(name="DM", value=f""" Please Target Someone """, inline=True)
        await ctx.reply(embed=embed)
    time.sleep(1)
    await ctx.channel.purge(limit=2)
    
    
    
    
@client.tree.command(name="dm" , description="Send Something To Someone")
@commands.has_permissions(administrator = True)
async def dm(interaction: discord.Interaction, member: discord.Member, message: str or str and float or int):
    try:
        embed = discord.Embed(title=f"Hi {member}", description = message, color=discord.Color.dark_purple())
        await member.send(embed=embed)
        embed = discord.Embed(color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(name="DM:", value=f"""Done!""", inline=True)
        await interaction.response.send_message(embed=embed , ephemeral=True)
    except:
        embed = discord.Embed(color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(name="DM", value=f""" Please Target Someone """, inline=True)
        await interaction.response.send_message(embed=embed , ephemeral=True)
    


@client.command(aliases =["!lock" , "!Lock"])
@commands.has_permissions(administrator=True)
async def lock(ctx):
    try:
        embed = discord.Embed(title="", description = "", color=discord.Color.dark_purple())
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        embed.add_field(name="lock:", value=f"""Channel locked by {ctx.author.mention}""", inline=True)
        await ctx.reply(embed=embed)
    except:
        embed = discord.Embed(title="", description = "", color=discord.Color.dark_purple())
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        embed.add_field(name="lock:", value=f"""You cant lock this channel because you dont have a premission.""", inline=True)
        await ctx.reply(embed=embed)
    time.sleep(1)
    await ctx.channel.purge(limit= 2)

@client.tree.command(name = "lock" , description = "To lock any room")
@commands.has_permissions(administrator = True)
@commands.bot_has_permissions(administrator = True)
async def lock(interaction: discord.Interaction):
    try:
        embed = discord.Embed(title="", description = "", color=discord.Color.dark_purple())
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
        embed.add_field(name="lock:", value=f"""Channel locked by {interaction.user}""", inline=True)
        await interaction.response.send_message(embed=embed , ephemeral=True)
    except:
        embed = discord.Embed(title="", description = "", color=discord.Color.dark_purple())
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
        embed.add_field(name="lock:", value=f"""You cant lock this channel because you dont have a premission.""", inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)


@client.command(aliases =["!unlock" , "!Unlock"])
@commands.has_permissions(administrator=True)
async def unlock(ctx):
    try:
        embed = discord.Embed(title="", description = "", color=discord.Color.dark_purple())
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        embed.add_field(name="unlock:", value=f"""Channel unlocked by {ctx.author.mention}""", inline=True)
        await ctx.reply(embed=embed)
    except MissingPermissions:
        embed = discord.Embed(title="", description = "", color=discord.Color.dark_purple())
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        embed.add_field(name="lock:", value=f"""You cant lock this channel because you dont have a premission.""", inline=True)
        await ctx.reply(embed=embed)
    time.sleep(1)
    await ctx.channel.purge(limit= 2)

@client.tree.command(name = "unlock" , description = "To unlock any room")
@commands.has_permissions(administrator = True)
@commands.bot_has_permissions(administrator = True)
async def unlock(interaction: discord.Interaction):
    try:
        embed = discord.Embed(title="", description = "", color=discord.Color.dark_purple())
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
        embed.add_field(name="unlock:", value=f"""Channel unlocked by {interaction.user}""", inline=True)
        await interaction.response.send_message(embed=embed , ephemeral=True)
    except:
        embed = discord.Embed(title="", description = "", color=discord.Color.dark_purple())
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
        embed.add_field(name="unlock:", value=f"""You cant unlock this channel because you dont have a premission.""", inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)


@client.tree.command(name = "rps" , description = "Rock Paper Scissors")
async def rps(interaction : discord.Interaction , rock_paper_scissors : str = "rock" or "paper" or "scissors"):
    embed = discord.Embed(title="", description = "", color=discord.Color.dark_purple())
    bot_rock , bot_paper , bot_scissors = "rock" , "paper" , "scissors"
    bot_hand = bot_rock , bot_paper , bot_scissors 
    bot_choice = random.choice(bot_hand)
    if bot_choice == rock_paper_scissors:
        embed.add_field(name="The Result:", value=f"""My choice was: **{bot_choice}** , We tied.""", inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=False)
    else:
        if bot_choice == bot_rock and rock_paper_scissors == "paper":
            embed.add_field(name="The Result:", value=f"""My choice was: **{bot_choice}**, You are the winner.""", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=False)
        else:
            if bot_choice == bot_rock and rock_paper_scissors == "scissors":
                embed.add_field(name="The Result:", value=f"""My choice was: **{bot_choice}**, I am the winner.""", inline=True)
                await interaction.response.send_message(embed=embed, ephemeral=False)
            else:
                if bot_choice == bot_paper and rock_paper_scissors == "rock":
                    embed.add_field(name="The Result:", value=f"""My choice was: **{bot_choice}**, I am the winner.""", inline=True)
                    await interaction.response.send_message(embed=embed, ephemeral=False)
                else:
                    if bot_choice == bot_paper and rock_paper_scissors == "scissors":
                        embed.add_field(name="The Result:", value=f"""My choice was: **{bot_choice}**, You are the winner.""", inline=True)
                        await interaction.response.send_message(embed=embed, ephemeral=False)
                    else:
                        if bot_choice == bot_scissors and rock_paper_scissors == "rock":
                            embed.add_field(name="The Result:", value=f"""My choice was: **{bot_choice}**, You are the winner.""", inline=True)
                            await interaction.response.send_message(embed=embed, ephemeral=False)
                        else:
                            if bot_choice == bot_scissors and rock_paper_scissors == "paper":
                                embed.add_field(name="The Result:", value=f"""My choice was: **{bot_choice}**, I am the winner.""", inline=True)
                                await interaction.response.send_message(embed=embed, ephemeral=False)

@client.command (name='rps', aliases=['!rockpaperscissors',"!rps"])
async def rps(ctx, *,user_choice : str =  None,  arg: str=None) :
    try:
        embed = discord.Embed(title="", description = "", color=discord.Color.dark_purple())
        choices = ['rock', 'paper', 'scissors']
        bot_choice = random.choice (choices) # picks a random choice
        if user_choice is str:
            user_choice = user_choice.lower()
        elif user_choice is None:
            embed.add_field(name="Error:", value=f"""Sorry but there seems to be a problem while running the command! Please make sure you put one of the following as your choice.\n {choices[0]},{choices[1]},{choices[2]}""", inline=True)
            await ctx.reply(embed=embed)
        elif bot_choice == user_choice:
            embed.add_field(name="The Result:", value=f"""My choice was: **{bot_choice}** , We tied.""", inline=True)
            await ctx.reply(embed=embed)
        elif bot_choice == 'rock' and user_choice == 'paper':
            embed.add_field(name="The Result:", value=f"""My choice was: **{bot_choice}**, You are the winner.""", inline=True)
            await ctx.reply(embed=embed)
        elif bot_choice == 'rock' and user_choice == 'scissors':
            embed.add_field(name="The Result:", value=f"""My choice was: **{bot_choice}**, I am the winner.""", inline=True)
            await ctx.reply(embed=embed)
        elif bot_choice == 'paper' and user_choice == 'rock':
            embed.add_field(name="The Result:", value=f"""My choice was: **{bot_choice}**, I am the winner.""", inline=True)
            await ctx.reply(embed=embed)
        elif bot_choice == "paper" and user_choice == 'scissors':
            embed.add_field(name="The Result:", value=f"""My choice was: **{bot_choice}**, You are the winner.""", inline=True)
            await ctx.reply(embed=embed)
        elif bot_choice == 'scissors' and user_choice == 'paper':
            embed.add_field(name="The Result:", value=f"""My choice was: **{bot_choice}**, I am the winner.""", inline=True)
            await ctx.reply(embed=embed)
        elif bot_choice == 'scissors' and user_choice == 'rock':
            embed.add_field(name="The Result:", value=f"""My choice was: **{bot_choice}**, You are the winner.""", inline=True)
            await ctx.reply(embed=embed)
        else:
            embed.add_field(name="Error:", value=f"""Sorry but there seems to be a problem while running the command! Please make sure you put one of the following as your choice.\n {choices[0]},{choices[1]},{choices[2]}""", inline=True)
            await ctx.reply(embed = embed)
    except MissingRequiredArgument:
        embed.add_field(name="Error:", value=f"""Sorry but there seems to be a problem while running the command! Please make sure you put one of the following as your choice.\n {choices[0]},{choices[1]},{choices[2]}""", inline=True)
        await ctx.reply(embed=embed)


@client.tree.command(name="short" , description="Short a link")
async def short(interaction : discord.Interaction , url : str):
    embed = discord.Embed(title="", description = "", color=discord.Color.dark_purple())
    shortner = pyshorteners.Shortener()
    x = shortner.tinyurl.short(url)
    embed.add_field(name="Your Short link:", value=f"""{x}""", inline=True)
    await interaction.response.send_message(embed = embed)
    
@client.command(aliases=["!short" , "!SHORT"])
async def short(ctx , url:str):
    embed = discord.Embed(title="", description = "", color=discord.Color.dark_purple())
    shortner = pyshorteners.Shortener()
    x = shortner.tinyurl.short(url)
    embed.add_field(name="Your Short link:", value=f"""{x}""", inline=True)
    await ctx.reply(embed = embed)


@client.tree.command(name="set_slowmode", description="Set slow mode for a channel")
@commands.has_permissions(manage_channels=True)
async def set_slowmode(interaction: discord.Interaction, channel: discord.TextChannel, slowmode_seconds: int):
    embed = discord.Embed(title="", description = "", color=discord.Color.dark_purple())
    await channel.edit(slowmode_delay=slowmode_seconds)
    embed.add_field(name="Slow Mode:", value=f"""Slow mode for {channel.mention} set to {slowmode_seconds} seconds.""", inline=True)
    await interaction.response.send_message(embed = embed)
    
@client.command(aliases=["!set_slowmode", "!Set_slowmode", "!SET_SLOWMODE", "!Set_Slowmode"])
@commands.has_permissions(administrator=True)
@commands.has_permissions(manage_channels=True)
async def set_slowmode(ctx, channel: discord.TextChannel = None or str or int or str and int, slowmode_seconds: int = 3):
    if channel is None:
        channel = ctx.channel
    else:
        if channel is int:
            ctx.send("Channel can not be a number. Please try again, [!set_slowmode #your_channel_name 3(slowmode seconeds)]")
        else:
            pass
    try:
        embed = discord.Embed(title="", description="", color=discord.Color.dark_purple())
        await channel.edit(slowmode_delay=slowmode_seconds)
        embed.add_field(name="Slow Mode:", value=f"Slow mode for {channel.mention} set to {slowmode_seconds} seconds.", inline=True)
        await ctx.reply(embed=embed)
        await asyncio.sleep(1)
        await ctx.channel.purge(limit=2)
    except:
        embed = discord.Embed(title="", description="", color=discord.Color.dark_purple())
        embed.add_field(name="Slow Mode:", value="There was an error. Please try again.", inline=True)
        await ctx.reply(embed=embed)
    
types_of_data = str or int or str and int
@client.tree.command(name = "suggestion" , description= "Use this command for make your message as a suggestion.")
async def suggestion(interaction : discord.Interaction , message : str or int or str and int):
    embed = discord.Embed(title="", description = "", color=discord.Color.dark_purple())
    embed.add_field(name="New suggestion:", value=f"""**{message}**""", inline=True)
    embed.set_footer(text=f'Requested by <@{interaction.user}>.', icon_url=interaction.user.avatar)
    msg = await interaction.response.send_message(embed = embed , ephemeral= False)
    msg = await interaction.original_response()
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')

@client.command(aliases=["!suggestion", "!SUGGESTION"])
async def suggestion(ctx, *, message):
    embed = discord.Embed(title="", description="", color=discord.Color.dark_purple())
    embed.add_field(name="New suggestion:", value=f"**{message}**", inline=True)
    embed.set_footer(text=f'Requested by {ctx.author}.', icon_url=ctx.author.avatar)
    msg = await ctx.reply(embed=embed)
    original_msg = await ctx.channel.fetch_message(msg.id)
    await original_msg.add_reaction('✅')
    await original_msg.add_reaction('❌')
    
    
snipe_author = {}
snipe_msg = {}
snipe_reply = {}
snipe_time = {}

@client.event
async def on_message_delete(message: discord.Message):
    if message.channel.type == "private" or message.author.bot : return 
    
    snipe_author[message.channel.id] = message.author
    snipe_msg[message.channel.id] = message.content
    snipe_time[message.channel.id] = f"<t:{int(datetime.datetime.now().timestamp())}:R>"
    
    if message.reference:
        snipe_reply[message.channel.id] = message.reference.resolved
    else:
        try: del snipe_reply[message.channel.id]
        except: pass

@client.command(aliases = ["!s" , "!snipe"])
async def snipe(ctx ,channel: typing.Optional[discord.TextChannel]):
    embed1 = discord.Embed(color=discord.Colour.dark_purple(), title="", description="")
    channel = channel or ctx.channel
    snipe_content = snipe_msg.get(channel.id)
    
    if snipe_content is None:
        embed1.add_field(name="", value="No message was deleted.", inline=False)
        return await ctx.send(embed = embed1)
    
    snipe_author_mention = snipe_author[channel.id].mention
    embed = discord.Embed(color=discord.Colour.dark_purple(), title="", description = f"Message deleted by: {snipe_author_mention}\n**Content:**\n{snipe_content}\n**Time:** {snipe_time[channel.id]}")
    snipe_reply_m = snipe_reply.get(channel.id)
    if snipe_reply_m:
        embed.add_field(
            name = "Replied to :",
            value = f"[{snipe_reply[channel.id].author}]({snipe_reply[channel.id].jump_url})"
        )
    
    await ctx.reply(embed = embed)
    


@client.remove_command("help")
@client.command(aliases=["!help", "!HELP", "!Help"])
async def help(ctx):
    help_embed = discord.Embed(
        color=discord.Colour.dark_purple(), title="", description="")
    help_embed.set_author(name="Help Command")
    help_embed.add_field(name="Moderation Commands:", value="", inline=False)
    help_embed.add_field(name="/clear:", value="Use it to clear spacific number of messages , default number of messages is 10 messages.", inline=False)
    help_embed.add_field(name="/kick:", value="Use it to kick user from your server. ", inline=False)
    help_embed.add_field(name="/ban:", value="Use it to ban user from your server. ", inline=False)
    help_embed.add_field(name="/unban:", value="Use it to unban user. Important: To work this command use user id.", inline=False)
    help_embed.add_field(name="/mute:", value="Use it to mute user from text.", inline=False)
    help_embed.add_field(name="/unmute:", value="Use it to unmute user from text.", inline=False)
    help_embed.add_field(name="/dm:", value="Use it to send to user some direct message.", inline=False)
    help_embed.add_field(name="/lock:", value="Use it to lock any text room and only Admins who can type in a locked room.", inline=False)
    help_embed.add_field(name="/unlock:", value="Use it to unlock any text room and only Admins who can type in a locked room.", inline=False)
    help_embed.add_field(name="/set_slowmode:", value="Set a slow mode for a channel.", inline=False)
    
    help_embed.add_field(name="______________________", value="", inline=False)
    
    help_embed.add_field(name="Public Commands:", value="", inline=False)
    help_embed.add_field(name="/help", value="Help commands.", inline=False)
    help_embed.add_field(name="/serverinfo:",value="Use it to show server information.", inline=False)
    help_embed.add_field(name="/user:", value="Use it to show user information.", inline=False)
    help_embed.add_field(name="/ping:", value="Use it to show bot letancy.", inline=False)
    help_embed.add_field(name="/avatar:", value="Use it to show user or your avatar.", inline=False)
    help_embed.add_field(name="/invite:", value="Use it to get bot invite.", inline=False)
    help_embed.add_field(name="/rps:", value="Rock Paper Scissors Game.", inline=False)
    help_embed.add_field(name="/short:", value="Link Shorter.", inline=False)
    help_embed.add_field(name="/suggestion:" , value= f"Use this command for make your message as a suggestion.")
    help_embed.set_footer(text=f'Requested by <@{ctx.author}>.', icon_url=ctx.author.avatar)
    await ctx.send(embed=help_embed)
    
    
    
@client.tree.command(name="help" , description="Shows All Commands In The Bot")
async def help(interaction: discord.Interaction):
    help_embed = discord.Embed(
        color=discord.Colour.dark_purple(), title="", description="")
    help_embed.set_author(name="Help Command")
    help_embed.add_field(name="Moderation Commands:", value="", inline=False)
    help_embed.add_field(name="/clear:", value="Use it to clear spacific number of messages , default number of messages is 10 messages.", inline=False)
    help_embed.add_field(name="/kick:", value="Use it to kick user from your server. ", inline=False)
    help_embed.add_field(name="/ban:", value="Use it to ban user from your server. ", inline=False)
    help_embed.add_field(name="/unban:", value="Use it to unban user. Important: To work this command use user id.", inline=False)
    help_embed.add_field(name="/mute:", value="Use it to mute user from text.", inline=False)
    help_embed.add_field(name="/unmute:", value="Use it to unmute user from text.", inline=False)
    help_embed.add_field(name="/dm:", value="Use it to send to user some direct message.", inline=False)
    help_embed.add_field(name="/lock:", value="Use it to lock any text room and only Admins who can type in a locked room.", inline=False)
    help_embed.add_field(name="/unlock:", value="Use it to unlock any text room and only Admins who can type in a locked room.", inline=False)
    help_embed.add_field(name="/set_slowmode:", value="Set a slow mode for a channel.", inline=False)
    
    help_embed.add_field(name="______________________", value="", inline=False)
    
    help_embed.add_field(name="Public Commands:", value="", inline=False)
    help_embed.add_field(name="/help", value="Help commands.", inline=False)
    help_embed.add_field(name="/serverinfo:",value="Use it to show server information.", inline=False)
    help_embed.add_field(name="/user:", value="Use it to show user information.", inline=False)
    help_embed.add_field(name="/ping:", value="Use it to show bot letancy.", inline=False)
    help_embed.add_field(name="/avatar:", value="Use it to show user or your avatar.", inline=False)
    help_embed.add_field(name="/invite:", value="Use it to get bot invite.", inline=False)
    help_embed.add_field(name="/rps:", value="Rock Paper Scissors Game.", inline=False)
    help_embed.add_field(name="/short:", value="Link Shorter.", inline=False)
    help_embed.add_field(name="/suggestion:" , value= f"Use this command for make your message as a suggestion.")
    help_embed.set_footer(text=f'Requested by <@{interaction.user}>.', icon_url=interaction.user.avatar)
    await interaction.response.send_message(embed= help_embed , ephemeral= False)


client.run("MTA4MDE5NTc2NjQxMDI5MzM4OQ.Gx-zKI.XhiQE-ZXyuvUzqjr90rRbuwk6mMJ4fGcofR8K8")