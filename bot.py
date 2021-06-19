from os import getenv
from glob import glob
from dotenv import load_dotenv
from discord.ext.commands import Bot as BotBase
import signal
from lib.db.handle_errors import handle_errors
from lib.db.query import db

PREFIX = "!code "
COGS = [path.split("/")[-1][:-3] for path in glob("./lib/cogs/*.py")]
load_dotenv()


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.conn = 0

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

        print(f"[+] Running Bot {version} ......")
        super().run(self.TOKEN, reconnect=True)

    async def on_message(self, message):

        if not message.author.bot and message.author != message.guild.me:
            await self.process_commands(message)

    async def on_ready(self):
        if not self.ready:
            self.loop.add_signal_handler(getattr(signal, 'SIGINT'),
                                         lambda: self.loop.create_task(self.signal_handler()))
            self.loop.add_signal_handler(getattr(signal, 'SIGTERM'),
                                         lambda: self.loop.create_task(self.signal_handler()))
            self.ready = True

        else:
            print("Bot reconnecting....")

    async def signal_handler(self):
        print("[+] Time to go")
        db.close_it()
        await self.close()

    async def on_connect(self):
        print("[+] Bot Connected")

    async def on_disconnect(self):
        print("[!] Bot Disconnected")

    async def on_command_error(self, context, exc):
        print("[!] Error occured")
        await handle_errors(exc, context)


bot = Bot()
