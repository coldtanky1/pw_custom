import sqlite3
import asyncio
import discord
from discord.ext import commands
from discord.utils import get
import globals

new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = globals.conn
cursor = globals.cursor


class Infra(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def infra(self, ctx):
        user_id = ctx.author.id

        # fetch username
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness, corp_tax = result

            # fetch user's military stats
            cursor.execute(
                'SELECT troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory FROM user_mil WHERE name = ?',
                (name,))
            mil_result = cursor.fetchone()

            # fetch user's infra
            cursor.execute(
                'SELECT basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps, park, cinema, museum, concert_hall FROM infra WHERE name = ?',
                (name,))
            infra_result = cursor.fetchone()

            if infra_result and mil_result:
                basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps, park, cinema, museum, concert_hall = infra_result
                troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result

                main_emb = discord.Embed(title='Infrastructure', type='rich',
                                         description=f'Displays {name}\'s infrastructure.\n'
                                                     f'React with "1️⃣" for Housing infrastructure.\n'
                                                     f'React with "2️⃣" for Production infrastructure.\n'
                                                     f'React with "3️⃣" for Military infrastructure.\n'
                                                     f'React with "4️⃣" for Entertainment infrastructure.',
                                         color=0x1E66F5)

                page_one = discord.Embed(title=f"{name}'s Infrastructure.", type='rich',
                                         description=f"Displays {name}'s housing infrastructure.", color=0x1E66F5)
                page_one.add_field(name="Page 1", value=f"{new_line}{new_line}"
                                                        f"Basic House: {basic_house}{new_line}"
                                                        f"Small Flat: {small_flat}{new_line}"
                                                        f"Apartment Complex: {apt_complex}{new_line}"
                                                        f"Skyscraper: {skyscraper}{new_line}", inline=False)

                page_two = discord.Embed(title=f"{name}'s Infrastructure.", type='rich',
                                         description=f"Displays {name}'s production infrastructure.", color=0x1E66F5)
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
                                                        f"Concrete Factory: {concrete_factory}{new_line}"
                                                        f"Corporations: {corps}{new_line}", inline=False)

                page_three = discord.Embed(title=f"{name}'s Infrastructure.", type='rich',
                                           description=f"Displays {name}'s military infrastructure.", color=0x1E66F5)
                page_three.add_field(name='Page 3', value=f"{new_line}{new_line}"
                                                          f"Military Factory: {militaryfactory}{new_line}"
                                                          f"Tank Factory: {tank_factory}{new_line}"
                                                          f"Plane Factory: {plane_factory}{new_line}"
                                                          f"Artillery Factory: {artillery_factory}{new_line}"
                                                          f"Anti-Air Factory: {anti_air_factory}{new_line}", inline=False)

                page_four = discord.Embed(title=f"{name}'s Infrastructure.", type='rich',
                                           description=f"Displays {name}'s entertainment infrastructure.", color=0x1E66F5)
                page_four.add_field(name='Page 4', value=f"{new_line}{new_line}"
                                                          f"Park: {park}{new_line}"
                                                          f"Cinema: {cinema}{new_line}"
                                                          f"Museum: {museum}{new_line}"
                                                          f"Concert Hall: {concert_hall}{new_line}", inline=False)

                infra_emb = await ctx.send(embed=main_emb)
                await infra_emb.add_reaction('1️⃣')
                await infra_emb.add_reaction('2️⃣')
                await infra_emb.add_reaction('3️⃣')
                await infra_emb.add_reaction('4️⃣')

                def chk(rec, usr):
                    return usr == ctx.author and str(rec.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣']

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
                        case '4️⃣':
                            await infra_emb.edit(embed=page_four)
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
