import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Bot



class help(commands.Cog):
    def __init__(self, clinet: commands.Bot):
        self.client = clinet
        self.client.remove_command("help")

    @app_commands.command(name="help" , description="Shows all commands are available The Bot")
    async def help(self, interaction: discord.Interaction):
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
        help_embed.add_field(name="!setup:" , value="Create a ticket message for the main server." , inline= False)
        help_embed.add_field(name="!ssetup:" , value="Create a ticket message for the store server." , inline= False)
        help_embed.add_field(name="!close:" , value="Closes the ticket and deletes the chat room." , inline= False)
        help_embed.add_field(name="/add:" , value="Add a blacklist word to the list." , inline= False)
        help_embed.add_field(name="/pblw:" , value="Shows you the blacklisted words." , inline= False)
        help_embed.add_field(name="/rpblw:" , value="Deletes a blacklisted word from the list." , inline= False)
        
        help_embed.add_field(name="______________________", value="", inline=False)
        help_embed.add_field(name="Public Commands:", value="", inline=False)
        help_embed.add_field(name="/help", value="Help commands.", inline=False)
        help_embed.add_field(name="/server:",value="Use it to show server information.", inline=False)
        help_embed.add_field(name="/user:", value="Use it to show user information.", inline=False)
        help_embed.add_field(name="/ping:", value="Use it to show bot letancy.", inline=False)
        help_embed.add_field(name="/avatar:", value="Use it to show user or your avatar.", inline=False)
        help_embed.add_field(name="/short:", value="Links Shorter.", inline=False)
        help_embed.set_footer(text=f'Requested by <@{interaction.user}>.', icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed = help_embed , ephemeral = False)
        
        


        
async def setup(client: commands.Bot) -> None:
    await client.add_cog(help(client))