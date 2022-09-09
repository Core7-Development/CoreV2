import discord
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks
from datetime import datetime

logs_id = 1017840856201441451

class ModLogs(commands.Cog, name="modlogs"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        z = self.bot.get_channel(logs_id)
        embed = discord.Embed(title = f"{message.author}'s Message was Deleted", description = f"Deleted Message: {message.content}\nAuthor: {message.author.mention}\nLocation: {message.channel.mention}", timestamp = datetime.now(), color = discord.Colour.red())
        embed.set_author(name = message.author.name, icon_url = message.author.display_avatar)
        await z.send(embed = embed)
        
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        z = self.bot.get_channel(logs_id)
        embed = discord.Embed(title = f"{before.author} Edited Their Message", description = f"Before: {before.content}\nAfter: {after.content}\nAuthor: {before.author.mention}\nLocation: {before.channel.mention}", timestamp = datetime.now(), color = discord.Colour.blue())
        embed.set_author(name = after.author.name, icon_url = after.author.display_avatar)
        await z.send(embed = embed)
        
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        z = self.bot.get_channel(logs_id)
        if len(before.roles) > len(after.roles):
            role = next(role for role in before.roles if role not in after.roles)
            embed = discord.Embed(title = f"{before}'s Role has Been Removed", description = f"{role.name} was removed from {before.mention}.",  timestamp = datetime.now(), color = discord.Colour.red())
        elif len(after.roles) > len(before.roles):
            role = next(role for role in after.roles if role not in before.roles)
            embed = discord.Embed(title = f"{before} Got a New Role", description = f"{role.name} was added to {before.mention}.",  timestamp = datetime.now(), color = discord.Colour.green())
        elif before.nick != after.nick:
            embed = discord.Embed(title = f"{before}'s Nickname Changed", description = f"Before: {before.nick}\nAfter: {after.nick}",  timestamp = datetime.now(), color = discord.Colour.blue())
        else:
            return
        embed.set_author(name = after.name, icon_url = after.display_avatar)
        await z.send(embed = embed)
        
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        z = self.bots.get_channel(logs_id)
        embed = discord.Embed(title = f"{channel.name} was Created", description = channel.mention, timestamp = datetime.now(), color = discord.Colour.green())
        await z.send(embed = embed)
        
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        z = self.bot.get_channel(logs_id)
        embed = discord.Embed(title = f"{channel.name} was Deleted", timestamp = datetime.now(), color = discord.Colour.red())
        await z.send(embed = embed)



async def setup(bot):
    await bot.add_cog(ModLogs(bot))