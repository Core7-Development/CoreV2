import asyncio
import json

from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Context
from helpers import checks

tag_location = "database/tags.json"


class Tags(commands.Cog, name="tags"):
    def __init__(self, bot):
        self.bot = bot

        try:
            with open(tag_location) as f:
                try:
                    self.tags = json.load(f)
                # chceck
                except json.JSONDecodeError:
                    self.create_tags()
        except FileNotFoundError:
            self.create_tags()

        asyncio.Task(self.save_tags())

    def create_tags(self):
        save = "{}"
        with open(tag_location, "w") as f:
            f.write(save)
        with open(tag_location) as f:
            self.tags = json.load(f)

    @commands.hybrid_command(
        name="rmtag",
        description="removes a tag",
    )
    @checks.not_blacklisted()
    async def rmtag(self, ctx, command: str):
        """Removes a tag
        Usage:
        self.rmtag tag"""
        command = command.lower()
        if command in self.tags:
            del self.tags[command]
            await ctx.send("Tag {} has been removed :thumbsup:".format(command))
        else:
            await ctx.send("Tag not registered, could not delete :thumbsdown: ")

    @commands.hybrid_command(
        name="tags",
        description="shows you all tags",
    )
    @checks.not_blacklisted()
    async def _tags(self, ctx):
        """Lists the tags added
        Usage:
        self.tags"""
        taglist = "```diff\nTags:"
        for x in self.tags.keys():
            taglist = "{}\n- {}".format(taglist, x)
        await ctx.send("{0} ```".format(taglist))

    @commands.hybrid_command(
        name="tag",
        description="adds tags",
    )
    @checks.not_blacklisted()
    async def tag(self, ctx, userinput: str, *, output: str = None):
        """Adds or displays a tag
        Usage:
        self.tag tag_name tag_data
        If 'tag_name' is a saved tag it will display that, else it will
        create a new tag using 'tag_data'"""
        userinput = userinput.lower()
        if userinput in self.tags:
            await ctx.send(self.tags[userinput])
        else:
            if output is not None:
                self.tags[userinput] = output
                if output.startswith("http"):
                    await ctx.send("Tag {} has been added with value <{}>".format(userinput, output))
                else:
                    await ctx.send("Tag {} has been added with value {}".format(userinput, output))

    async def save_tags(self):
        while True:
            save = json.dumps(self.tags)
            with open(tag_location, "w") as data:
                data.write(save)
            await asyncio.sleep(60)


async def setup(bot):
    await bot.add_cog(Tags(bot))