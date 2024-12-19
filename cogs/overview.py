import asyncio
import discord
from discord.ext import commands

from sim_funcs.NAI_func import NAI_Determiner
from cogs.update import HappinessCalculator

from schema import *


new_line = '\n'


class Overview(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def overview(self, ctx):
        user_id = ctx.author.id

        # fetch username
        result = UserInfo.select().where(UserInfo.user_id == user_id).first()

        if result:
            name = result.name

            # fetch user's resources
            res_result = Resources.select().where(Resources.name == name).first()

            # fetch user's production infra
            infra_result = Infra.select(Infra.basic_house, Infra.small_flat, Infra.apt_complex, Infra.skyscraper).where(Infra.name == name).tuples().first()

            # fetch user's population stats.
            pop_result = UserStats.select().where(UserStats.name == name).first()

            if infra_result:
                basic_house, small_flat, apt_complex, skyscraper = infra_result
                food = res_result.food
                adult = pop_result.adult

                # Population Housing
                basic_house_housing = basic_house * 4
                small_flat_housing = small_flat * 25
                apt_complex_housing = apt_complex * 30
                skyscraper_housing = skyscraper * 100

                total_housing = basic_house_housing + small_flat_housing + apt_complex_housing + skyscraper_housing

                # For food check
                pop_food_req = round(adult//50)

                # NAI
                NAI = NAI_Determiner(user_id)

                happiness_bonus = await HappinessCalculator()

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
                                                             f"You need {pop_food_req-food:,} food to feed your population.", inline=False)
                else:
                    embed.add_field(name="Food stock", value="The population is fed.\n",
                                                             inline=False)
                    
                embed.add_field(name="Income", value=f"The national average wage for {name} is ${NAI:,}.", inline=False)
                embed.add_field(name="Happiness", value=f"The happiness bonus from entertainment buildings is {happiness_bonus}", inline=False)

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
