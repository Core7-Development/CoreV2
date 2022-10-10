import json
import os
import sys

import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Context
from helpers import checks


from reactionmenu import ViewMenu, ViewButton
import Paginator


if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class Help(commands.Cog, name="help"):
    def __init__(self, bot):
        self.bot = bot

    # These arguments override the default ones.

   


    # @commands.hybrid_command(
    #     name="help",
    #     description="List all commands the bot has loaded."
    # )
    # async def help(self, context: Context) -> None:
    #     prefix = self.bot.config["prefix"]
    #     embed = discord.Embed(title="Help", description="List of available commands:", color=0x9C84EF)
    #     for i in self.bot.cogs:
    #         cog = self.bot.get_cog(i.lower())
    #         commands = cog.get_commands()
    #         data = []
    #         for command in commands:
    #             description = command.description.partition('\n')[0]
    #             data.append(f"{prefix}{command.name} - {description}")
    #         help_text = "\n".join(data)
    #         embed.add_field(name=i.capitalize(), value=f'```{help_text}```', inline=False)
    #     await context.send(embed=embed)


    @commands.hybrid_command(
        name="help",
        description="List all commands the bot has loaded."
    )
    async def help(self, context: Context) -> None:
        prefix = self.bot.config["prefix"]
        embeds = []

        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())

            embed=discord.Embed(title=i.capitalize(), description="", color=0x36393f)
            commands = cog.get_commands()
            command_list = [command.name for command in commands]
            command_description = [command.help for command in commands]

            for c in command_list:
                embed.add_field(name=c, value=command_description[command_list.index(c)], inline=False)
            
            embeds.append(embed)
            #help_text = '\n'.join(f'{prefix}{n} - {h}' for n, h in zip(command_list, command_description))


        PreviousButton = discord.ui.Button(label="⬅️",style=discord.ButtonStyle.gray)
        NextButton = discord.ui.Button(label="➡️",style=discord.ButtonStyle.gray)
        PageCounterStyle = discord.ButtonStyle.gray # Only accepts ButtonStyle instead of Button
        InitialPage = 0 # Page to start the paginator on.
        timeout = 42069 # Seconds to timeout. Default is 60

        await Paginator.Simple(
            PreviousButton=PreviousButton,
            NextButton=NextButton,
            PageCounterStyle=PageCounterStyle,
            InitialPage=InitialPage,
            timeout=timeout).start(context, pages=embeds)
        
    
    

    # @commands.hybrid_command(
    #     name="help",
    #     description="shows you all commands",
    # )
    # @checks.not_blacklisted()
    # async def help(self, context: Context) -> None:
    #     """
    #     List all commands from every Cog the bot has loaded.
    #     """
    
    #     user = context.author
    #     home_btn = SButton(label='Home', emoji='🏠', custom_id="home", rewrite=True)
    #     left_btn = SButton(label='', emoji='◀️', custom_id="backward", rewrite=True)
    #     right_btn = SButton(label='', emoji='▶', custom_id="forward", rewrite=True)
    #     delete_btn = SButton(label='Delete', delete_msg=True, custom_id="delete", rewrite=True, style = ButtonStyle.danger)

    #     menu = SDropMenu(placeholder="Select a module", custom_id="cmds-list", rewrite=True)

    #     buttons = [home_btn, left_btn, right_btn, delete_btn]
    #     menus = [menu]

    #     prefix = config["prefix"]
    #     if not isinstance(prefix, str):
    #         prefix = prefix[0]
    #     embedMain = discord.Embed(title="Help", description="List of available commands:", color=0x36393f)
    #     embeds = [embedMain]
    #     for i in self.bot.cogs:
    #         cog = self.bot.get_cog(i.lower())

    #         embed=discord.Embed(title=i.capitalize(), description="", color=0x36393f)
    #         commands = cog.get_commands()
    #         command_list = [command.name for command in commands]
    #         command_description = [command.help for command in commands]

    #         for c in command_list:
    #             embed.add_field(name=c, value=command_description[command_list.index(c)], inline=False)
            
    #         embeds.append(embed)
    #         #help_text = '\n'.join(f'{prefix}{n} - {h}' for n, h in zip(command_list, command_description))


    #     cmd_list = [
    #         SOption(name="Fun", embed=embeds[1]),
    #         SOption(name="Moderation", embed=embeds[2]),
    #         SOption(name="Owner", embed=embeds[3]),
    #         SOption(name="Template", embed=embeds[4]),
    #         SOption(name="Help", embed=embeds[5]),
    #         SOption(name="General", embed=embeds[6])
    #     ]

    #     view_ = Paginator(user, embeds, commands_list=cmd_list, menus=menus, buttons=buttons).view()
    #     await context.send(embed=embeds[0], view=view_)
        
        

async def setup(bot):
    await bot.add_cog(Help(bot))