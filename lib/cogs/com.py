from random import choice
from discord.ext.commands import Cog
from ..models.warrior import get_warrior
from discord.ext.commands import command, Context
from discord import Embed

BASE = "https://www.codewars.com/api/v1/users/"



class MyCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hi", aliases=["Hello", "Hi", "hello", "hola", "hey"])
    async def say_hello(self, ctx: Context):
        await ctx.send(f"{choice(('Hi', 'Hiya', 'Hey', 'Hola', 'Hello', 'Yo'))} {ctx.author.mention}")

    @command(name="info")
    async def info(self, ctx: Context, user: str):
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
            embed.set_image(url="https://www.codewars.com/users/majidabdulred/badges/large")
            await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        pass


def setup(bot):
    bot.add_cog(MyCommands(bot))
