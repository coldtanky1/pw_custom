import asyncio
import discord
import math
from discord.ext import commands
from discord.utils import get
from schema import *
from sim_funcs.NAI_func import NAI_Determiner

new_line = '\n'

def limit_happiness(happiness):
    print("line 12")
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
        result = UserInfo.select().where(UserInfo.user_id == user_id).tuples().first()

        if result:  # If "user" is provided
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness, corp_tax = result

            # fetch user stats
            stats_result = UserStats.select().where(UserStats.name == name).tuples().first()

            # fetch user's production infra
            infra_result = Infra.select(
                Infra.basic_house, Infra.small_flat, Infra.apt_complex,
                Infra.skyscraper, Infra.lumber_mill, Infra.coal_mine,
                Infra.iron_mine, Infra.lead_mine, Infra.bauxite_mine,
                Infra.oil_derrick, Infra.uranium_mine, Infra.farm,
                Infra.aluminium_factory, Infra.steel_factory, Infra.oil_refinery,
                Infra.ammo_factory, Infra.concrete_factory, Infra.militaryfactory,
                Infra.corps).where(Infra.name == name).tuples().first()

            # fetch user's mil stats
            mil_result = UserMil.select().where(UserMil.name == name).tuples().first()

            if stats_result and mil_result and infra_result:
                name, nation_score, gdp, adult, balance = stats_result
                name, troops, planes, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result
                basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps = infra_result

                workers = round(adult//1.2)
                soldiers = round((adult//6) - troops)
 
                tax_revenue_bonus = 1

                match gov_type:
                    case "Anarchy":
                        tax_revenue_bonus *= 0
                    case "Communism":
                        tax_revenue_bonus *= 0.5
                    case "Democracy":
                        tax_revenue_bonus *= 1.2
                    case "Fascism":
                        tax_revenue_bonus *= 0.9
                    case "Monarchy":
                        tax_revenue_bonus *= 1.1
                    case "Socialism":
                       tax_revenue_bonus *= 0.6

                NAI = NAI_Determiner(user_id=user_id)
                tax_revenue = round(tax_rate * (NAI * adult) * tax_revenue_bonus)
                gdp_per_capita = round(gdp // adult)
 
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
                # Adds flag to embed
                cus_result = UserCustom.select().where(UserCustom.name == name).first()
                flag = cus_result.flag
                if flag:
                    embed.set_thumbnail(url=flag)
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
        result = UserInfo.select().where(UserInfo.user_id == user_id).tuples().first()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness, corp_tax = result

            # fetch user's mil stats
            mil_result = UserMil.select(
                UserMil.troops, UserMil.planes, UserMil.tanks,
                UserMil.artillery, UserMil.anti_air, UserMil.barracks,
                UserMil.tank_factory, UserMil.plane_factory, UserMil.artillery_factory,
                UserMil.anti_air_factory).where(UserMil.name == name).tuples().first()

            if mil_result:
                troops, planes, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result

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

                # Adds flag to embed
                cus_result = UserCustom.select().where(UserCustom.name == name).first()
                flag = cus_result.flag
                if flag:
                    embed.set_thumbnail(url=flag)

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
