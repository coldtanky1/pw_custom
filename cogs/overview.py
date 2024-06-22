import sqlite3
import asyncio
import discord
from discord.ext import commands

new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = sqlite3.connect('player_info.db')
cursor = conn.cursor()


class Overview(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def overview(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT name FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            name = result[0]

            # fetch user's resources
            cursor.execute(
                'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                (name,))
            res_result = cursor.fetchone()

            # fetch user's production infra
            cursor.execute(
                'SELECT name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps FROM infra WHERE name = ?',
                (name,))
            infra_result = cursor.fetchone()

            # fetch user's population stats.
            cursor.execute(
                'SELECT name, nation_score, gdp, adult, balance FROM user_stats WHERE name = ?',
                (name,))
            pop_result = cursor.fetchone()

            if infra_result:
                name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps = infra_result
                name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result
                name, nation_score, gdp, adult, balance = pop_result

                # Population Housing
                basic_house_housing = basic_house * 4
                small_flat_housing = small_flat * 25
                apt_complex_housing = apt_complex * 30
                skyscraper_housing = skyscraper * 100

                total_housing = basic_house_housing + small_flat_housing + apt_complex_housing + skyscraper_housing

                # For food check
                pop_food_req = round(adult//50)

                embed = discord.Embed(title=f"Overview of {name}", type='rich', 
                                    description=f"An overview of {name}'s nation.",
                                    color=discord.Color.blue())
                
                if adult > total_housing:
                    embed.add_field(name="Housing", value=f"The population is not housed.\n{adult-total_housing:,} need to be housed.",
                                    inline=False)
                else:
                    embed.add_field(name="Housing", value=f"The population is fully housed.", inline=False)

                if pop_food_req > food:
                    embed.add_field(name="Food stock", value="The population is not fed.\n"
                                                             f"You need {pop_food_req-food:,} to feed your population.", inline=False)
                else:
                    embed.add_field(name="Food stock", value="The population is fed.\n",
                                                             inline=False)

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
    await bot.add_cog(Overview(bot))