import asyncio
import os
import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from schema import init_db

new_line = '\n'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents, case_insensitive=True)

load_dotenv()

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

# Load the bot
async def main():
    await load()
    await bot.start(os.getenv('DISCORD_TOKEN'))

init_db()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.command()
async def ping(ctx):
    lat = int(bot.latency * 1000)
    await ctx.send(f'Pong! {lat}ms')

def dev_check(usid):
    return usid == 837257162223910912 or usid == 669517694751604738

@bot.command()  # Help command and command list made specifically for devs
async def devhelp(ctx, cmd: str = ""):
    if dev_check(ctx.author.id):
        cmd = cmd.lower()
        match cmd:
            case "debug_mode" | "debugmode":
                embed = discord.Embed(colour=0xdc8a78, title="Dev Help | Debug Mode", type='rich',
                                      description=f'Syntax: `$debug_mode`{new_line}{new_line}'
                                                  f'Status: {globals.debug}{new_line}{new_line}'
                                                  f'Switches the global variable \'debug\' from on to off and vice versa. {new_line}'
                                                  f'While on, this can do many things, but for now it only disables the error handler and prints the error to the console.{new_line}'
                                                  f'Debug mode is switched to off on boot.')
                await ctx.send(embed=embed)
            case "debug" | "debug_status" | "debugstatus" | "dstatus":
                embed = discord.Embed(colour=0xdc8a78, title="Dev Help | Debug Status", type='rich',
                                      description=f'Syntax: `$debug_status`{new_line}{new_line}'
                                                  f'Status: {globals.debug}{new_line}{new_line}'
                                                  f'Shows whether debug mode is on or off')
                await ctx.send(embed=embed)
            case _:
                embed = discord.Embed(colour=0xdc8a78, title="Help | General", type='rich')  # General Tab
                embed.add_field(name="Debug", value="debug_mode - Turns debug mode on and off.\n"
                                                    "debug_status - Shows if debug mode is on or off.",
                                inline=False)
                await ctx.send(embed=embed)
    else:
        print(f'{ctx.author} attempted to enable debug')
        embed = discord.Embed(colour=0xEF2F73, title="Permission Denied", type='rich',
                              description=f'You are not a developer.')
        await ctx.send(embed=embed)


asyncio.run(main())
