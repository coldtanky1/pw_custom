import sqlite3
import asyncio
import discord
import math
from discord.ext import commands
from discord.utils import get
import globals

new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = globals.conn
cursor = globals.cursor

def limit_happiness(happiness):
    return min(120, happiness)

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def stats(self, ctx, user: discord.Member = None):
        if user is None:
            user_id = ctx.author.id
        else:
            user_id = user.id

        # fetch username
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:  # If "user" is provided
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness, corp_tax = result

            # fetch user stats
            cursor.execute('SELECT * FROM user_stats WHERE name = ?', (name,))
            stats_result = cursor.fetchone()

            # fetch user's production infra
            cursor.execute(
                'SELECT basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps FROM infra WHERE name = ?',
                (name,))
            infra_result = cursor.fetchone()

            # fetch user's mil stats
            cursor.execute(
                'SELECT troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory FROM user_mil WHERE name = ?',
                (name,))
            mil_result = cursor.fetchone()

            if stats_result and mil_result and infra_result:
                name, nation_score, gdp, adult, balance = stats_result
                troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result
                basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps = infra_result

                workers = round(adult//1.2)
                soldiers = round((adult//6) - troops)

                total_pop = adult

                tax_revenue = round(tax_rate * total_pop)

                gdp_per_capita = round(gdp // total_pop)

                embed = discord.Embed(
                    title=f"📊 {name}'s Stats",
                    description=f'Name: {name}',
                    color=0x04a5e5
                )
                # These are different in case that we decide to display less stats when checking another user
                if user_id == ctx.author.id:
                    embed.add_field(name='`[---NATION---]`', value=f"{new_line}"
                                                                   f"🫅 Ruler: <@{user_id}>{new_line}"
                                                                   f"🏆 Nation Score: {nation_score:,}{new_line}"
                                                                   f"⏰ Turns: {turns_accumulated:,}{new_line}"
                                                                   f"😊 Happiness: {happiness}{new_line}", inline=False)
                    embed.add_field(name='`[---ECONOMY---]`', value=f'{new_line}'
                                                                    f"📈 Gross Domestic Product: {gdp:,}{new_line}"
                                                                    f"📈 GDP Per Capita: {gdp_per_capita:,}{new_line}"
                                                                    f"📊 Tax Income: {tax_revenue:,}{new_line}"
                                                                    f"💰 Balance: {balance:,}{new_line}", inline=False)
                    embed.add_field(name='`[---POLITICS---]`', value=f'{new_line}'
                                                                     f"🏦Government: {gov_type}{new_line}", inline=False)
                    embed.add_field(name='`[---DEMOGRAPHICS---]`', value=f'{new_line}'
                                                                         f"👨 Adults: {adult:,}{new_line}"
                                                                         f"👷‍♂️ Workers: {workers:,}{new_line}"
                                                                         f"💂Manpower: {soldiers:,}{new_line}", inline=False)
                else:
                    embed.add_field(name='`[---NATION---]`', value=f"{new_line}"
                                                                   f"🫅 Ruler: <@{user_id}>{new_line}"
                                                                   f"🏆 Nation Score: {nation_score:,}{new_line}"
                                                                   f"😊 Happiness: {happiness}{new_line}", inline=False)
                    embed.add_field(name='`[---ECONOMY---]`', value=f'{new_line}'
                                                                    f"📈 Gross Domestic Product: {gdp:,}{new_line}"
                                                                    f"📈 GDP Per Capita: {gdp_per_capita:,}{new_line}"
                                                                    f"📊 Tax Income: {tax_revenue:,}{new_line}"
                                                                    f"💰 Balance: {balance:,}{new_line}", inline=False)
                    embed.add_field(name='`[---POLITICS---]`', value=f'{new_line}'
                                                                     f"🏦Government: {gov_type}{new_line}", inline=False)
                    embed.add_field(name='`[---DEMOGRAPHICS---]`', value=f'{new_line}'
                                                                         f"👨 Adults: {adult:,}{new_line}"
                                                                         f"👷‍♂️ Workers: {workers:,}{new_line}"
                                                                         f"💂Manpower: {soldiers:,}{new_line}",
                                    inline=False)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description=f'Cannot find stats.')
                await ctx.send(embed=embed)
        else:
            if user_id == ctx.author.id:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description=f'You do not have a nation.{new_line}'
                                                  f'To create one, type `$create`.')
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description=f'This user does not have a nation.{new_line}'
                                                  f'To create one, type `$create`.')
                await ctx.send(embed=embed)

    @commands.command()
    async def mstats(self, ctx):
        user_id = ctx.author.id

        # fetch username
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness, corp_tax = result

            # fetch user's mil stats
            cursor.execute(
                'SELECT troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory FROM user_mil WHERE name = ?',
                (name,))
            mil_result = cursor.fetchone()

            if mil_result:
                troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result

                embed = discord.Embed(
                    title=f"⚔ {name}'s Military Stats",
                    description='',
                    color=0xe64553
                )
                embed.add_field(name='🪖 Troops', value=f'{troops:,}', inline=False)
                embed.add_field(name='', value='', inline=False)
                embed.add_field(name='⛟ Tanks', value=f'{tanks:,}', inline=False)
                embed.add_field(name='', value='', inline=False)
                embed.add_field(name='💥 Artillery', value=f'{artillery:,}', inline=False)
                embed.add_field(name='', value='', inline=False)
                embed.add_field(name='💥 Anti-Air', value=f'{anti_air:,}', inline=False)
                embed.add_field(name='', value='', inline=False)
                embed.add_field(name='🛫 Planes', value=f'{planes:,}', inline=False)
                embed.add_field(name='', value='', inline=False)
                embed.add_field(name='🎖 Barracks', value=f'{barracks:,}', inline=False)
                embed.add_field(name='', value='', inline=False)
                embed.add_field(name='🛡️ War Status', value=f'{war_status}', inline=False)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description=f'Cannot find stats.')
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Stats(bot))
