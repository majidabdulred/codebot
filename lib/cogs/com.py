from random import choice
from discord.ext.commands import Cog
from discord.ext.commands import command, Context, BadArgument
from discord import Embed

from ..db.query import db
from ..models.warrior import get_warrior

BASE = "https://www.codewars.com/api/v1/users/"


class MyCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hi", aliases=["Hello", "Hi", "hello", "hola", "hey"])
    async def say_hello(self, ctx: Context):
        await ctx.send(f"{choice(('Hi', 'Hiya', 'Hey', 'Hola', 'Hello', 'Yo'))} {ctx.author.mention}")

    @command(name="showall")
    async def showall(self, ctx):
        await ctx.send(f"```\n{str(db.show_all())}```")

    @command(name="del")
    async def deluser(self, ctx):
        member = ctx.message.mentions
        if len(member) != 1:
            raise BadArgument
        elif not db.check_id_exists(str(member[0].id)):
            await ctx.send("User doesn't exists")
        elif db.deluser(member[0].id):
            await ctx.send("User successfully deleted")
        else:
            await ctx.send("Deletion Failed !")

    @command(name="reg")
    async def reg(self, ctx, username):
        member = ctx.message.mentions
        if len(member) != 1:
            raise BadArgument
        elif await get_warrior(username) is None:
            await ctx.send(f"There is no codewars profile named as {username}")
        else:
            if db.add_member(member[0].id, username):
                await ctx.send(f"{member[0].mention} successfully registered as {username}.")
            else:
                await ctx.send("Registration Failed !!!")

    @command(name="info", aliases=["INFO"])
    async def info(self, ctx, user: str, from_info_mentioned=False):
        if ctx.message.mentions and not from_info_mentioned:
            await self.info_mentioned(ctx)
            return

        user = await get_warrior(user)

        if user is None:
            await ctx.send("User not found")
        else:
            embed = Embed(title=f"{user.rank}",
                          description=f"{user.username}", color=0xd41616)
            embed.set_footer(text="Ver : 0.0.1 (Beta)")
            embed.set_author(name=f"{user.name}", url=f"https://www.codewars.com/users/{user.username}")
            embed.insert_field_at(index=1, name="Honor", value=f"{user.honor}")
            embed.insert_field_at(index=2, name="Position", value=f"{user.position}")
            embed.insert_field_at(index=3, name="Completed", value=f"{user.completed}")
            embed.insert_field_at(index=4, name="Clan", value=f"{user.clan}")

            await ctx.send(embed=embed)

    async def info_mentioned(self, ctx):
        username = db.get_username(ctx.message.mentions[0].id)

        print("Called info")
        await self.info(ctx, username, True)

    @Cog.listener()
    async def on_ready(self):
        pass


def setup(bot):
    bot.add_cog(MyCommands(bot))
