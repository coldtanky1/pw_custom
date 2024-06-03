import sqlite3
import asyncio
import discord
from discord.ext import commands
from discord.utils import get

new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = sqlite3.connect('player_info.db')
cursor = conn.cursor()


class Infra(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def infra(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            # fetch user's military stats
            cursor.execute(
                'SELECT name, troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory FROM user_mil WHERE name = ?',
                (name,))
            mil_result = cursor.fetchone()

            # fetch user's infra
            cursor.execute(
                'SELECT name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory FROM infra WHERE name = ?',
                (name,))
            infra_result = cursor.fetchone()

            if infra_result and mil_result:
                name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory = infra_result
                name, troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result

                main_emb = discord.Embed(title='Infrastructure', type='rich',
                                            description=f'Displays {name}\'s infrastructure.\n'
                                                        'React with "1️⃣" for Housing infrastructure.\n'
                                                        'React with "2️⃣" for Production infrastructure.\n'
                                                        'React with "3️⃣" for Military infrastructure.',
                                            color=discord.Color.blue()
                                            )

                page_one = discord.Embed(title=f"{name}'s Infrastructure.", type='rich',
                                        description=f"Displays {name}'s housing infrastructure.", color=discord.Color.blue())
                page_one.add_field(name="Page 1", value=f"{new_line}{new_line}"
                                                        f"Basic House: {basic_house}{new_line}"
                                                        f"Small Flat: {small_flat}{new_line}"
                                                        f"Apartment Complex: {apt_complex}{new_line}"
                                                        f"Skyscraper: {skyscraper}{new_line}", inline=False)

                page_two = discord.Embed(title=f"{name}'s Infrastructure.", type='rich',
                                        description=f"Displays {name}'s production infrastructure.", color=discord.Color.blue())
                page_two.add_field(name="Page 2", value=f"{new_line}{new_line}"
                                                        f"Lumber Mill: {lumber_mill}{new_line}"
                                                        f"Coal Mine: {coal_mine}{new_line}"
                                                        f"Iron Mine: {iron_mine}{new_line}"
                                                        f"Lead Mine: {lead_mine}{new_line}"
                                                        f"Bauxite Mine: {bauxite_mine}{new_line}"
                                                        f"Oil Derrick: {oil_derrick}{new_line}"
                                                        f"Uranium Mine: {uranium_mine}{new_line}"
                                                        f"Farm: {farm}{new_line}"
                                                        f"Aluminium Factory: {aluminium_factory}{new_line}"
                                                        f"Steel Factory: {steel_factory}{new_line}"
                                                        f"Oil Refinery: {oil_refinery}{new_line}"
                                                        f"Munitions Factory: {ammo_factory}{new_line}"
                                                        f"Concrete Factory: {concrete_factory}{new_line}", inline=False)

                page_three = discord.Embed(title=f"{name}'s Infrastructure.", type='rich',
                                        description=f"Displays {name}'s military infrastructure.", color=discord.Color.blue())
                page_three.add_field(name='Page 3', value=f"{new_line}{new_line}"
                                                          f"Military Factory: {militaryfactory}{new_line}"
                                                          f"Tank Factory: {tank_factory}{new_line}"
                                                          f"Plane Factory: {plane_factory}{new_line}"
                                                          f"Artillery Factory: {artillery_factory}{new_line}"
                                                          f"Anti-Air Factory: {anti_air_factory}{new_line}", inline=False)

                infra_emb = await ctx.send(embed=main_emb)
                await infra_emb.add_reaction('1️⃣')
                await infra_emb.add_reaction('2️⃣')
                await infra_emb.add_reaction('3️⃣')

                def chk(rec, usr):
                    return usr == ctx.author and str(rec.emoji) in ['1️⃣', '2️⃣', '3️⃣']

                while True:
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=chk)
                    except TimeoutError:
                        break
                    match(str(reaction.emoji)):   # Choosing Tab based on emoji
                        case '1️⃣':
                            await infra_emb.edit(embed=page_one)
                        case '2️⃣':
                            await infra_emb.edit(embed=page_two)
                        case '3️⃣':
                            await infra_emb.edit(embed=page_three)
                        case _:
                            break
                    await infra_emb.remove_reaction(reaction.emoji, user)

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
    await bot.add_cog(Infra(bot))