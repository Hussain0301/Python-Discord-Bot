import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from datetime import timedelta, datetime
import re

class Security(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.warning_threshold = 5
        self.timeout_durations = [
            timedelta(minutes=1), timedelta(minutes=5), timedelta(minutes=10), timedelta(minutes=20), timedelta(minutes=30)
        ]
        self.blacklist_words = ["Bad Word"]

        self.admin_role_ids = [] #Admin role
        
        self.spam_message_limit = 5
        self.spam_time_window = timedelta(seconds=3)
        self.mute_duration = timedelta(minutes=10)
        self.role_change_limit = 2
        self.role_change_interval = timedelta(seconds=30)
        self.room_change_limit = 3
        self.room_change_interval = timedelta(seconds=3)

        self.user_warnings = {}
        self.post_timeout_offenses = {}
        self.message_tracker = {}
        self.role_change_tracker = {}
        self.room_change_tracker = {}
        self.anti_spam = commands.CooldownMapping.from_cooldown(5, 15, commands.BucketType.member)
        self.too_many_viol = commands.CooldownMapping.from_cooldown(2, 60, commands.BucketType.member)

    async def ban_user(self, guild, user, reason):
        await guild.ban(user, reason=reason)
        await user.send(f"You've been banned for: {reason}")
        self.user_warnings.pop(user.id, None)
        self.post_timeout_offenses.pop(user.id, None)
        self.message_tracker.pop(user.id, None)
        self.role_change_tracker.pop(user.id, None)
        self.room_change_tracker.pop(user.id, None)

    async def warn_user(self, guild, user, reason):
        self.user_warnings[user.id] = self.user_warnings.get(user.id, 0) + 1
        warning_level = self.user_warnings[user.id]

        if warning_level <= self.warning_threshold:
            await user.edit(timed_out_until=discord.utils.utcnow() + self.timeout_durations[warning_level - 1], reason="Out of limits of warnings.")

        warning_role_name = f"Warning {warning_level}"
        warning_role = discord.utils.get(guild.roles, name=warning_role_name)
        if not warning_role:
            warning_role = await guild.create_role(name=warning_role_name)

        await user.add_roles(warning_role)
        await user.send(f'Warning {warning_level}: {reason}')

        for role in user.roles:
            if role.id in self.admin_role_ids:
                await user.remove_roles(role)
                await user.send(f'Removed admin role {role.name}')

        if warning_level >= self.warning_threshold:
            await self.ban_user(guild, user, "Out of limits of warnings.")
            self.user_warnings[user.id] = 0
            self.post_timeout_offenses[user.id] = 0

    async def mute_user(self, guild, user, reason):
        mute_role_name = "Muted"
        mute_role = discord.utils.get(guild.roles, name=mute_role_name)
        if not mute_role:
            mute_role = await guild.create_role(name=mute_role_name, permissions=discord.Permissions(send_messages=False, speak=False))
        await user.add_roles(mute_role)
        await user.send(f'You have been mute for {self.mute_duration.total_seconds() / 60:.0f} minutes: {reason}')

        await discord.utils.sleep_until(datetime.utcnow() + self.mute_duration)
        await user.remove_roles(mute_role)

    async def track_role_change(self, user_id):
        now = datetime.utcnow()
        if user_id not in self.role_change_tracker:
            self.role_change_tracker[user_id] = []
        self.role_change_tracker[user_id].append(now)

        self.role_change_tracker[user_id] = [timestamp for timestamp in self.role_change_tracker[user_id] if now - timestamp <= self.role_change_interval]

        return len(self.role_change_tracker[user_id])
    
    async def track_room_change(self, user_id):
        now = datetime.utcnow()
        if user_id not in self.room_change_tracker:
            self.room_change_tracker[user_id] = []
        self.room_change_tracker[user_id].append(now)

        self.room_change_tracker[user_id] = [timestamp for timestamp in self.room_change_tracker[user_id] if now - timestamp <= self.room_change_interval]

        return len(self.room_change_tracker[user_id])

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        user = message.author

        message_splited = message.content.lower().split()
        for word in message_splited:
            if word in self.blacklist_words:
                await message.delete()
                if user.id in self.post_timeout_offenses:
                    await self.ban_user(message.guild, user, "Out of limits of warnings.")
                else:
                    await self.warn_user(message.guild, user, "Don't say any bad words again please.")

        if not message.author.guild_permissions.manage_messages:
            link = message.content
            url = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
            if url.search(link):
                await message.delete()
                if user.id in self.post_timeout_offenses:
                    await self.ban_user(message.guild, user, "Out of limits of warnings.")
                else:
                    await self.warn_user(message.guild, user, "Don't send any links again please.")
                return

        if type(message.channel) is not discord.TextChannel or message.author.bot:
            return
        bucket = self.anti_spam.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            await message.delete()
            voli = self.too_many_viol.get_bucket(message)
            check = voli.update_rate_limit()
            if check:
                await message.author.timeout(timedelta(minutes=10), reason="Spamming")
                try:
                    await message.author.send("You've been muted for spamming.")
                except:
                    pass
                if user.id in self.post_timeout_offenses:
                    await self.ban_user(message.guild, user, "Out of limits of warnings.")
                else:
                    await self.warn_user(message.guild, user, "Spamming")
                return

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):
            user = entry.user
            role_change_count = await self.track_role_change(user.id)

            if role_change_count >= self.role_change_limit:
                await self.warn_user(role.guild, user, "Spamming role creation")
                return

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
            user = entry.user
            role_change_count = await self.track_role_change(user.id)

            if role_change_count >= self.role_change_limit:
                await self.warn_user(role.guild, user, "Spamming role deletion")
                return
    
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):
            user = entry.user
            room_change_count = await self.track_room_change(user.id)

            if room_change_count >= self.room_change_limit:
                await self.warn_user(channel.guild, user, "Spamming channel creation")
                return

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
            user = entry.user
            room_change_count = await self.track_room_change(user.id)

            if room_change_count >= self.room_change_limit:
                await self.warn_user(channel.guild, user, "Spamming channel deletion")
                return

    @app_commands.command(name="add", description="Add a word to the blacklisted words")
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def add(self, interaction: discord.Interaction, words: str):
        blw = words.split()
        for word in blw:
            if word not in self.blacklist_words:
                self.blacklist_words.append(word.strip())
        await interaction.response.send_message(f"{len(blw)} word(s) have been added to the blacklist", ephemeral=True)

    @app_commands.command(name="pblw", description="Shows you the list of blacklisted words")
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def blacklisted_words_print(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"The list of blacklisted words is: {self.blacklist_words}", ephemeral=True)
        
    @app_commands.command(name="rpblw", description="Deletes a blacklisted word from the list.")
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def rpblw(self, interaction: discord.Interaction, word: str):
        if word in self.blacklist_words:
            self.blacklist_words.remove(word)
            await interaction.response.send_message(f"{word} has been deleted from the blacklist.", ephemeral=True)
        else:
            await interaction.response.send_message(f"The word '{word}' isn't in the blacklist.", ephemeral=True)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Security(client))
