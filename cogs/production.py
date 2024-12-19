import asyncio
from typing import get_overloads
import discord
from discord.ext import commands
from discord.utils import get

from schema import *

new_line = '\n'


class Production(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def res(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        result = UserInfo.select(UserInfo.user_id, UserInfo.name, UserInfo.gov_type).where(UserInfo.user_id == user_id).tuples().first()

        if result:
            user_id, name, gov_type = result

            # fetch user's resources
            res_result = Resources.select(Resources.iron, Resources.lead, Resources.bauxite, Resources.oil).where(Resources.name == name).tuples().first()

            # fetch user's production infra
            infra_result = Infra.select(
                Infra.lumber_mill, Infra.coal_mine, Infra.iron_mine,
                Infra.lead_mine, Infra.bauxite_mine, Infra.oil_derrick,
                Infra.uranium_mine, Infra.farm, Infra.aluminium_factory,
                Infra.steel_factory, Infra.oil_refinery, Infra.ammo_factory,
                Infra.concrete_factory, Infra.militaryfactory).where(Infra.name == name).tuples().first()

            # fetch user's military stats
            mil_result = UserMil.select(UserMil.tank_factory, UserMil.plane_factory, UserMil.artillery_factory, UserMil.anti_air_factory).where(UserMil.name == name).tuples().first()

            # fetch user's population stats.
            pop_result = UserStats.select().where(UserStats.name == name).first()

            if infra_result and res_result:
                lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory = infra_result
                iron, lead, bauxite, oil = res_result
                tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result
                adult = pop_result.adult

                # production multipliers
                base_output = 2.50
                mil_prod_efficiency = 0.5
                res_prod_multiplier = 1.0
                if gov_type == "Communism":
                    res_prod_multiplier *= 2
                    mil_prod_efficiency = 0.75
                    base_output = 3
                elif gov_type == "Fascism":
                    mil_prod_efficiency = 0.60
                    base_output = 2.75


                # the production of military equipment.
                prod_aa = base_output * anti_air_factory * mil_prod_efficiency
                prod_arty = base_output * artillery_factory * mil_prod_efficiency
                prod_plane = base_output * plane_factory * mil_prod_efficiency
                prod_tank = base_output * tank_factory * mil_prod_efficiency

                # The production of each resource
                prod_wood = lumber_mill * 2 * res_prod_multiplier
                prod_coal = coal_mine * 1.2 * res_prod_multiplier
                prod_iron = iron_mine * 1 * res_prod_multiplier
                prod_lead = lead_mine * 0.8 * res_prod_multiplier
                prod_bauxite = bauxite_mine * 0.6 * res_prod_multiplier
                prod_oil = oil_derrick * 1 * res_prod_multiplier
                prod_uranium = uranium_mine * 0.05 * res_prod_multiplier
                prod_farm = farm * 10 * res_prod_multiplier
                prod_aluminium = aluminium_factory * 0.4 * res_prod_multiplier
                prod_steel = steel_factory * 0.3 * res_prod_multiplier
                prod_gas = oil_refinery * 0.2 * res_prod_multiplier
                prod_ammo = ammo_factory * 0.5 * res_prod_multiplier
                prod_concrete = concrete_factory * 0.6 * res_prod_multiplier

                # The consumption of each resource
                usage_iron_wood = prod_wood * 0
                usage_lead_wood = prod_wood * 0
                usage_bauxite_wood = prod_wood * 0
                usage_iron_coal = prod_coal * 0
                usage_lead_coal = prod_coal * 0
                usage_bauxite_coal = prod_coal * 0
                usage_iron_iron = prod_iron * 0
                usage_lead_iron = prod_iron * 0
                usage_bauxite_iron = prod_iron * 0
                usage_iron_lead = prod_lead * 0
                usage_lead_lead = prod_lead * 0
                usage_bauxite_lead = prod_lead * 0
                usage_iron_bauxite = prod_bauxite * 0
                usage_lead_bauxite = prod_bauxite * 0
                usage_bauxite_bauxite = prod_bauxite * 0
                usage_iron_oil = prod_oil * 0
                usage_lead_oil = prod_oil * 0
                usage_bauxite_oil = prod_oil * 0
                usage_iron_uranium = prod_uranium * 0
                usage_lead_uranium = prod_uranium * 0
                usage_bauxite_uranium = prod_uranium * 0
                usage_iron_food = prod_farm * 0
                usage_lead_food = prod_farm * 0
                usage_bauxite_food = prod_farm * 0
                usage_iron_aluminium = prod_aluminium * 0.2
                usage_lead_aluminium = prod_aluminium * 0.1
                usage_bauxite_aluminium = prod_aluminium * 1.2
                usage_iron_steel = prod_steel * 1.4
                usage_lead_steel = prod_steel * 0.3
                usage_bauxite_steel = prod_steel * 0.3
                usage_oil_gas = prod_gas * 2
                usage_lead_gas = prod_gas * 0
                usage_bauxite_gas = prod_gas * 0
                usage_iron_ammo = prod_ammo * 0.2
                usage_lead_ammo = prod_ammo * 1.1
                usage_bauxite_ammo = prod_ammo * 0
                usage_iron_concrete = prod_concrete * 0.5
                usage_lead_concrete = prod_concrete * 0
                usage_bauxite_concrete = prod_concrete * 0

                final_usage_iron = usage_iron_wood + usage_iron_coal + usage_iron_iron + usage_iron_lead + usage_iron_bauxite + usage_iron_oil + usage_iron_uranium + usage_iron_food + usage_iron_aluminium + usage_iron_steel + usage_iron_ammo + usage_iron_concrete
                final_usage_lead = usage_lead_wood + usage_lead_coal + usage_lead_iron + usage_lead_lead + usage_lead_bauxite + usage_lead_oil + usage_lead_uranium + usage_lead_food + usage_lead_aluminium + usage_lead_steel + usage_lead_ammo + usage_lead_concrete
                final_usage_bauxite = usage_bauxite_wood + usage_bauxite_coal + usage_bauxite_iron + usage_bauxite_lead + usage_bauxite_bauxite + usage_bauxite_oil + usage_bauxite_uranium + usage_bauxite_food + usage_bauxite_aluminium + usage_bauxite_steel + usage_bauxite_ammo + usage_bauxite_concrete

                final_prod_iron = prod_iron - final_usage_iron
                final_prod_lead = prod_lead - final_usage_lead
                final_prod_bauxite = prod_bauxite - final_usage_bauxite
                final_prod_oil = prod_oil - usage_oil_gas

                total_pop = adult
                usage_food = total_pop // 50

                final_prod_food = prod_farm - usage_food

                if (iron < final_usage_iron) or (lead < final_usage_lead) or (bauxite < final_usage_bauxite) or (oil < usage_oil_gas):
                    prod_aluminium = 0
                    prod_steel = 0
                    prod_gas = 0
                    prod_ammo = 0
                    prod_concrete = 0

                main_emb = discord.Embed(title='Production', type='rich',
                                            description=f'Displays {name}\'s production.\n'
                                                        'React with "⛏" for Mined Resources.\n'
                                                        'React with "🏭" for Manufactured Resources.\n'
                                                        'React with "🛡" for Military Equipment.',
                                            color=discord.Color.blurple()
                                            )

                mined_emb = discord.Embed(title="Mined Resources", type='rich',
                                        description=f'Displays {name}\'s Mined Resources Production.',
                                        color=discord.Color.blurple()
                                        )
                mined_emb.add_field(name='Wood', value=f'{round(int(prod_wood), 3):,}', inline=False)
                mined_emb.add_field(name='Coal', value=f'{round(int(prod_coal), 3):,}', inline=False)
                mined_emb.add_field(name='Iron', value=f'{round(int(final_prod_iron), 3):,}', inline=False)
                mined_emb.add_field(name='Lead', value=f'{round(int(final_prod_lead), 3):,}', inline=False)
                mined_emb.add_field(name='Bauxite', value=f'{round(int(final_prod_bauxite), 3):,}', inline=False)
                mined_emb.add_field(name='Oil', value=f'{round(int(final_prod_oil), 3):,}', inline=False)
                mined_emb.add_field(name='Uranium', value=f'{round(int(prod_uranium), 3):,}', inline=False)
                mined_emb.add_field(name='Food', value=f'{round(int(final_prod_food), 3):,}', inline=False)

                manu_emb = discord.Embed(title='Manufactured Resources', type='rich',
                                         description=f'Displays {name}\'s Mined Resources Production.',
                                         color=discord.Color.blue()
                                         )
                manu_emb.add_field(name='Aluminium', value=f'{round(int(prod_aluminium), 3):,}', inline=False)
                manu_emb.add_field(name='Steel', value=f'{round(int(prod_steel), 3):,}', inline=False)
                manu_emb.add_field(name='Gasoline', value=f'{round(int(prod_gas), 3):,}', inline=False)
                manu_emb.add_field(name='Ammo', value=f'{round(int(prod_ammo), 3):,}', inline=False)
                manu_emb.add_field(name='Concrete', value=f'{round(int(prod_concrete), 3):,}', inline=False)

                mil_emb = discord.Embed(title='Military Equipment', type='rich',
                                        description=f'Displays {name}\'s Military Equipment Production.',
                                        color=discord.Color.blue()
                                        )
                mil_emb.add_field(name='Tanks', value=f'{round(int(prod_tank), 3):,}', inline=False)
                mil_emb.add_field(name='Plane', value=f'{round(int(prod_plane), 3):,}', inline=False)
                mil_emb.add_field(name='Artillery', value=f'{round(int(prod_arty), 3):,}', inline=False)
                mil_emb.add_field(name='Anti-Air', value=f'{round(int(prod_aa), 3):,}', inline=False)

                prod_emb = await ctx.send(embed=main_emb)
                await prod_emb.add_reaction("⛏")
                await prod_emb.add_reaction("🏭")
                await prod_emb.add_reaction("🛡")

                def chk(rec, usr):
                    return usr == ctx.author and str(rec.emoji) in ['⛏', '🏭', '🛡']

                while True:
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=chk)
                    except TimeoutError:
                        break
                    match(str(reaction.emoji)):   # Choosing Tab based on emoji
                        case '⛏':
                            await prod_emb.edit(embed=mined_emb)
                        case '🏭':
                            await prod_emb.edit(embed=manu_emb)
                        case '🛡':
                            await prod_emb.edit(embed=mil_emb)
                        case _:
                            break
                    await prod_emb.remove_reaction(reaction.emoji, user)

            else:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description=f'Cannot find stats.')
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    # Reserve Command
    @commands.command()
    async def reserve(self, ctx):
        user_id = ctx.author.id

        # fetch username
        result = UserInfo.select().where(UserInfo.user_id == user_id).first()

        if result:
            name = result.name

            # fetch user's resources
            resource_result = Resources.select().where(Resources.name == name).tuples().first()

            if resource_result:
                name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = resource_result

                embed = discord.Embed(
                    title=f'{name}\'s Reserves',
                    description='Displays nation\'s national reserves.',
                    color=0x4CAF50)
                embed.add_field(name=f'Wood: {int(round(wood)):,}', value='', inline=False)
                embed.add_field(name=f'Coal: {int(round(coal)):,}', value='', inline=False)
                embed.add_field(name=f'Iron: {int(round(iron)):,}', value='', inline=False)
                embed.add_field(name=f'Lead: {int(round(lead)):,}', value='', inline=False)
                embed.add_field(name=f'Bauxite: {int(round(bauxite)):,}', value='', inline=False)
                embed.add_field(name=f'Oil: {int(round(oil)):,}', value='', inline=False)
                embed.add_field(name=f'Uranium: {int(round(uranium)):,}', value='', inline=False)
                embed.add_field(name=f'Food: {int(round(food)):,}', value='', inline=False)
                embed.add_field(name=f'Steel: {int(round(steel)):,}', value='', inline=False)
                embed.add_field(name=f'Aluminium: {int(round(aluminium)):,}', value='', inline=False)
                embed.add_field(name=f'Gasoline: {int(round(gasoline)):,}', value='', inline=False)
                embed.add_field(name=f'Ammo: {int(round(ammo)):,}', value='', inline=False)
                embed.add_field(name=f'Concrete: {int(round(concrete)):,}', value='', inline=False)
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
    await bot.add_cog(Production(bot))