from os import getenv
from glob import glob
from dotenv import load_dotenv
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound, BadArgument, MissingRequiredArgument
from discord.errors import HTTPException, Forbidden

PREFIX = "!code "
COGS = [path.split("/")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)
load_dotenv()


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None

        super().__init__(command_prefix=PREFIX)

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"[+] Cog loaded - {cog}")
        print("[+] Setupcomplete")

    def run(self, version):
        self.version = version
        print("[+] Running setup")
        self.setup()

        self.TOKEN = getenv("DISCORD_TOKEN")

        print("[+] Running Bot......")
        super().run(self.TOKEN, reconnect=True)

    async def on_message(self, message):

        if not message.author.bot and message.author != message.guild.me:
            await self.process_commands(message)

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(632799582350475265)
            self.stdch = self.get_channel(854215344075440138)
            await self.stdch.send("Now Online")
        else:
            print("Bot reconnecting....")

    async def on_connect(self):
        print("[+] Bot Connected")

    async def on_disconnect(self):
        print("[!] Bot Disconnected")

    async def _on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

    async def on_command_error(self, context, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass

        elif isinstance(exc, MissingRequiredArgument):
            await context.send("One or more arguments are missing")

        elif isinstance(exc.original, HTTPException):
            await context.send("Unable to send message")

        elif isinstance(exc.original, Forbidden):
            await context.send("Don't have permissions")

        elif hasattr(exc, "original"):
            raise exc.original

        else:
            raise exc

    # async def process_commands(self, message):
    #     print("processing command")
    #     ctx = await self.stdch.send(message, cls=Context)
    #     print("after process")
    #     if ctx.command is not None and ctx.guild is not None:
    #         if self.ready:
    #             print("invoked")
    #             await self.invoke(ctx)
    #         else:
    #             await ctx.send("I am not ready")


bot = Bot()
