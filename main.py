import sqlite3
import asyncio
import os
import time
import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import subprocess
import re
import globals

new_line = '\n'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents, case_insensitive=True)

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

# Load the bot
async def main():
    await load()
    await bot.start(token)

# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = sqlite3.connect('player_info.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_info(
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        turns_accumulated INTEGER,
        gov_type TEXT,
        tax_rate REAL,
        conscription TEXT,
        freedom TEXT,
        police_policy TEXT,
        fire_policy TEXT,
        hospital_policy TEXT,
        war_status TEXT,
        happiness INTEGER,
        corp_tax REAL
        )
    ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_stats(
        name TEXT PRIMARY KEY,
        nation_score INTEGER,
        gdp INTEGER,
        adult INTEGER,
        balance INTEGER
        )
    ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_mil(
        name TEXT PRIMARY KEY,
        troops INTEGER,
        planes INTEGER,
        weapon INTEGER,
        tanks INTEGER,
        artillery INTEGER,
        anti_air INTEGER,
        barracks INTEGER,
        tank_factory INTEGER,
        plane_factory INTEGER,
        artillery_factory INTEGER,
        anti_air_factory INTEGER
        )
    ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS infra(
        name TEXT PRIMARY KEY,
        basic_house INTEGER,
        small_flat INTEGER,
        apt_complex INTEGER,
        skyscraper INTEGER,
        lumber_mill INTEGER,
        coal_mine INTEGER,
        iron_mine INTEGER,
        lead_mine INTEGER,
        bauxite_mine INTEGER,
        oil_derrick INTEGER,
        uranium_mine INTEGER,
        farm INTEGER,
        aluminium_factory INTEGER,
        steel_factory INTEGER,
        oil_refinery INTEGER,
        ammo_factory INTEGER,
        concrete_factory INTEGER,
        militaryfactory INTEGER,
        corps INTEGER,
        hospital INTEGER,
        police_station INTEGER,
        fire_station INTEGER,
        schools INTEGER
        )
    ''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS resources(
        name TEXT PRIMARY KEY,
        wood INTEGER,
        coal INTEGER,
        iron INTEGER,
        lead INTEGER,
        bauxite INTEGER,
        oil INTEGER,
        uranium INTEGER,
        food INTEGER,
        steel INTEGER,
        aluminium INTEGER,
        gasoline INTEGER,
        ammo INTEGER,
        concrete INTEGER
        )
    ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_custom(
        name TEXT PRIMARY KEY,
        flag TEXT
    )
''')

globals.init()

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
