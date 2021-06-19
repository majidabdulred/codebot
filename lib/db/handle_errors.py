from psycopg2 import errors
from ..db.query import db
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import CommandNotFound, BadArgument, MissingRequiredArgument,BadBoolArgument


async def handle_errors(exc, ctx):
    print(f"[!] {exc}")
    if any([isinstance(exc, error) for error in (MissingRequiredArgument,BadArgument,BadBoolArgument)]):
        await ctx.send("Command not used properly.")

    elif isinstance(exc,CommandNotFound):
        await ctx.send("This isn't a command")
    elif isinstance(exc.original, HTTPException):
        await ctx.send("Unable to send message")

    elif isinstance(exc.original, Forbidden):
        await ctx.send("Don't have permissions")

    elif isinstance(exc.original, errors.InFailedSqlTransaction):
        db.conn.rollback()
        await ctx.send("Error Occured - InFailedSqlTransaction. Try again")

    elif isinstance(exc.original, errors.UniqueViolation):
        db.conn.rollback()
        await ctx.send("Member already registered")

    elif isinstance(exc.original, IndexError):
        await ctx.send("User not registered! Register it using\n```\n!code reg <codewars_username> <@mention>```")

    elif isinstance(exc, ConnectionError):
        await ctx.send(
            "Database connection could not be established. Please retry or send `!code redb` to restablish connection.")

    elif hasattr(exc, "original"):
        raise exc.original

    else:
        raise exc
