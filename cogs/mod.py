import discord
from discord import app_commands
from discord.ext.commands import MissingPermissions 
from discord.ext import commands


class Mod(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="nick", description="Use to change a member's nickname")
    @app_commands.checks.has_permissions(manage_nicknames=True)
    async def nick(self, interaction: discord.Interaction, member: discord.Member, nick: str):
        try:
            embed = discord.Embed(color=discord.Colour.dark_purple(), title="", description="")
            embed.add_field(name="Nickname changer:", value=f"Done!", inline=True)
            await member.edit(nick=nick)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception:
            embed = discord.Embed(color=discord.Colour.dark_purple(), title="", description="")
            embed.add_field(name="Nickname changer:", value="Please target a member or choose a nickname.", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
     

    @app_commands.command(name="clear", description="Clear command")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, channel: discord.TextChannel, amount: int = 10):
        embed = discord.Embed(color=discord.Colour.dark_purple(), title="", description="")
        embed.add_field(name="", value=f"Cleared {amount} message(s) successfully!", inline=True)
        await channel.purge(limit=amount)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        

    @app_commands.command(name="kick", description="Kick a member from the server")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, user: discord.Member = None, reason: str = None):
        try:
            await user.kick(reason=reason)
            embed = discord.Embed(color=discord.Colour.dark_purple(), title="", description="")
            embed.add_field(name="", value=f"The user **{user}** has been kicked! Reason = **{reason}**", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception:
            embed = discord.Embed(color=discord.Colour.dark_purple(), title="", description="")
            embed.add_field(name="", value="Please target someone.", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            



    @app_commands.command(name="ban", description="Ban a member from the server")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, user: discord.Member = None, reason: str = None):
        try:
            await user.ban(reason=reason)
            embed = discord.Embed(color=discord.Colour.dark_purple(), title="", description="")
            embed.add_field(name="", value=f"The user **{user}** has been banned! Reason = **{reason}**", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception:
            embed = discord.Embed(color=discord.Colour.dark_purple(), title="", description="")
            embed.add_field(name="", value="Please target a member.", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            



    @app_commands.command(name="unban", description="Unban a user")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: str):
        try:
            guild = interaction.guild
            user = discord.Object(id=user_id)
            await guild.unban(user)
            embed = discord.Embed(color=discord.Colour.dark_purple(), title="", description="")
            embed.add_field(name="", value=f"The user **{user_id}** has been unbanned!", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception:
            embed = discord.Embed(color=discord.Colour.dark_purple(), title="", description="")
            embed.add_field(name="", value="Please provide a valid user ID.", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            

            

    @app_commands.command(name="mute", description="Mute a member in the server")
    @app_commands.checks.has_permissions(mute_members=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member = None):
        try:
            guild = interaction.guild
            muted_role = discord.utils.get(guild.roles, name="Muted")
            if not muted_role:
                muted_role = await guild.create_role(name="Muted")
                for channel in guild.channels:
                    await channel.set_permissions(muted_role, speak=False, send_messages=False)
            await member.add_roles(muted_role)

            embed = discord.Embed(title="", description=f"{member.mention} has been muted.", color=discord.Colour.dark_purple())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception:
            embed = discord.Embed(color=discord.Colour.dark_purple(), title="", description="")
            embed.add_field(name="", value="Please target a member.", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            


    @app_commands.command(name="unmute", description="Unmute a member in the server")
    @app_commands.checks.has_permissions(mute_members=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member = None):
        try:
            guild = interaction.guild
            muted_role = discord.utils.get(guild.roles, name="Muted")
            if muted_role in member.roles:
                await member.remove_roles(muted_role)
                embed = discord.Embed(title="Unmute", description=f"{member.mention} has been unmuted.", color=discord.Colour.dark_purple())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title="Unmute", description=f"{member.mention} is not muted.", color=discord.Colour.dark_purple())
                await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception:
            embed = discord.Embed(color=discord.Colour.dark_purple(), title="", description="")
            embed.add_field(name="Unmute", value="Please target a member.", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command(name="dm", description="Send a direct message to a member of the server")
    @app_commands.checks.has_permissions(administrator=True)
    async def dm(self, interaction: discord.Interaction, member: discord.Member, content: str):
        await member.send(content)
        await interaction.response.send_message(f"{interaction.user.mention} I sent the content to {member.mention}: {content}", ephemeral=True)


    @app_commands.command(name="lock", description="To prevent sending in the chat room")
    @app_commands.checks.has_permissions(administrator=True)
    async def lock(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(title="", description="", color=discord.Colour.dark_purple())
            await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
            embed.add_field(name="Lock:", value=f"Channel locked by {interaction.user}", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception:
            embed = discord.Embed(title="", description="", color=discord.Colour.dark_purple())
            embed.add_field(name="Lock:", value="You can't lock this channel because you don't have permission.", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command(name="unlock", description="To allow sending in the chat room")
    @app_commands.checks.has_permissions(administrator=True)
    async def unlock(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(title="", description="", color=discord.Colour.dark_purple())
            await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
            embed.add_field(name="Unlock:", value=f"Channel unlocked by {interaction.user}", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception:
            embed = discord.Embed(title="", description="", color=discord.Colour.dark_purple())
            embed.add_field(name="Unlock:", value="You can't unlock this channel because you don't have permission.", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)



    @app_commands.command(name="set_slowmode", description="Adjust the slow mode of the channel")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def set_slowmode(self, interaction: discord.Interaction, channel: discord.TextChannel, slowmode_seconds: int):
        embed = discord.Embed(title="", description="", color=discord.Colour.dark_purple())
        await channel.edit(slowmode_delay=slowmode_seconds)
        embed.add_field(name="", value=f"Slow mode for {channel.mention} set to {slowmode_seconds} seconds.", inline=True)
        await interaction.response.send_message(embed=embed)



    @commands.command(name="close", description="Closes the ticket room and deletes it." , aliases = ["c", "C" , "Close" , "CLOSE"])
    @commands.has_permissions(administrator=True)
    async def close(self, interaction: discord.Interaction):
        try:
            await interaction.channel.delete()
        except Exception:
            await interaction.response.send_message("An error occurred. Please try again.", ephemeral=True)




async def setup(client: commands.Bot):
    await client.add_cog(Mod(client))
