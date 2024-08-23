import discord
from discord import app_commands
from discord.ext import commands
import pyshorteners


class public(commands.Cog):
    def __init__(self, clinet: commands.Bot):
        self.client = clinet
        
    @app_commands.command(name="ping" , description="Show you the ping of the bot.")
    async def ping(self, interaction:discord.Interaction): 
        embed = discord.Embed(
            color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(
            name="Ping:", value=f"""{int(self.client.latency *1000)}ms""", inline=True)
        embed.set_footer(text=f'Requested by <@{interaction.user}>.', icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed , ephemeral=False)


    
    @app_commands.command(name="avatar", description="Shows user's avatar")
    async def avatar(self, interaction:discord.Interaction,  member:discord.User = None  ):
        member = interaction.user if not member else member
        embed = discord.Embed(title=member.name + "#" + member.discriminator)
        embed.set_image(url=member.avatar)
        await interaction.response.send_message(embed=embed , ephemeral=False)



    @app_commands.command(name="server" , description="Shows server information")
    async def server(self, interaction: discord.Interaction):
        name = str(interaction.guild.name)
        embed = discord.Embed(title=name ,
                          color=discord.Colour.dark_purple())
        try:
            embed.set_thumbnail(url=interaction.guild.icon.url)
        except:
            url = None

        embed.add_field(name="Server created on", value=interaction.guild.created_at.strftime(
            "%d %b %Y "), inline=False)

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


 
    @app_commands.command(name="user" , description="Shows user's information.")
    async def user(self, interaction: discord.Interaction, member: discord.Member = None):

        if member is None:
                member = interaction.user

        member_id = int(member.id)
        fetch_member = interaction.guild.get_member(member_id)

        embed = discord.Embed(title="", color=discord.Colour.dark_purple())
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Name", value=member.name, inline=False)
        embed.add_field(name="Nickname", value=member.nick, inline=False)
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Status", value=str(fetch_member.status), inline=False)
        
    
        activity_details = getattr(fetch_member.activity, 'details', 'None')
        embed.add_field(name="Activity", value=activity_details, inline=False)

        embed.add_field(name="Roles", value=" ".join([role.mention for role in member.roles]), inline=False)
        embed.set_footer(text=f'Requested by {interaction.user}.', icon_url=interaction.user.avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=False)
            
        

    
        
    @app_commands.command(name="short" , description="Links shorter")
    @discord.app_commands.checks.has_permissions(administrator = True)
    async def short(self, interaction : discord.Interaction , url : str):
        embed = discord.Embed(title="", description = "", color=discord.Colour.dark_purple())
        shortner = pyshorteners.Shortener()
        x = shortner.tinyurl.short(url)
        embed.add_field(name="Your Short link:", value=f"""{x}""", inline=True)
        await interaction.response.send_message(embed = embed)
        
        

    
    
      
async def setup(client: commands.Bot) -> None:
    await client.add_cog(public(client))