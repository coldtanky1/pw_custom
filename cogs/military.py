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


class Military(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Recruit Command
    @commands.command()
    async def recruit(self, ctx, amount: int):
        user_id = ctx.author.id

        if amount <= 0:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description="Invalid amount, please try a positive number.")
            await ctx.send(embed=embed)
            return

        # fetch username
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness, corp_tax = result

            # fetch user's resources
            cursor.execute(
                'SELECT wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                (name,))
            res_result = cursor.fetchone()

            # fetch user's military stats
            cursor.execute(
                'SELECT troops, planes, weapon, tanks, artillery, anti_air, barracks FROM user_mil WHERE name = ?',
                (name,))
            mil_result = cursor.fetchone()

            if res_result:
                wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result
                bonus = 1
                if gov_type == "Fascism":
                    bonus /= 2

                inf_ammo = round((amount * 0.2) * bonus)
                inf_food = round((amount * 0.03) * bonus)
                inf_turns = round(amount * 0.00003 + 1)
                inf_time = int(inf_turns)
                time_turns = inf_time * 3600

                if (ammo <= inf_ammo) and (food <= inf_food):
                    embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                          description="You do not have enough resources to recruit.")
                    await ctx.send(embed=embed)
                    return

                else:
                    emb = discord.Embed(title='Recruitment', type='rich', colour=0xDD7878,
                                        description=f'{amount:,} will be recruited into {name}\'s military.{new_line}'
                                                    f'They will be ready within {inf_time} turns.')
                    await ctx.send(embed=emb)

                    await asyncio.sleep(time_turns)

                    cursor.execute('UDPATE user_stats SET adult = adult - ? WHERE name = ?', (amount, name))
                    conn.commit()

                    cursor.execute('UPDATE user_mil SET troops = troops + ? WHERE name = ?', (amount, name))
                    conn.commit()
            else:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description=f'Cannot find stats.')
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    # LIST OF MIL COMMANDS (tank, artillery, plane, anti-air)

    # Tank Production Command
    @commands.command()
    async def allocate(self, ctx, mil_type: str, amount: int):
        mil_type = mil_type.lower()
        user_id = ctx.author.id

        if amount <= 0:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description="Invalid amount, please try a positive number.")
            await ctx.send(embed=embed)
            return

        # fetch username
        cursor.execute('SELECT name FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            name = result[0]

            # fetch user's resources
            cursor.execute(
                'SELECT wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                (name,))
            res_result = cursor.fetchone()

            # fetch user's production infra
            cursor.execute(
                'SELECT basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps FROM infra WHERE name = ?',
                (name,))
            infra_result = cursor.fetchone()

            # fetch user's military stats
            cursor.execute(
                'SELECT troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory FROM user_mil WHERE name = ?',
                (name,))
            mil_result = cursor.fetchone()

            if mil_result and res_result and infra_result:
                troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result
                wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result
                basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps = infra_result

                match mil_type:
                    case "tank":
                        if amount > militaryfactory:  # If user doesn't have enough mil factories, the command exits.
                            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                                  description="You do not have enough military factories.")
                            await ctx.send(embed=embed)
                            return

                        else:
                            allocating = discord.Embed(title='Allocation | Tank', type='rich', colour=0xDD7878,
                                                       description=f'Allocating {amount:,} to {mil_type}...')
                            allo_emb = await ctx.send(embed=allocating)

                            prod_tank = amount * militaryfactory // 42
                            usage_tank_steel = amount * 5
                            usage_tank_gas = amount * 1.25

                            # Update military factory count.
                            cursor.execute('UPDATE infra SET militaryfactory = militaryfactory - ? WHERE name = ?', (amount, name))
                            conn.commit()

                            # Update factory count.
                            cursor.execute('UPDATE user_mil SET tank_factory = tank_factory + ? WHERE name = ?', (amount, name))
                            conn.commit()

                            # Update resources.
                            cursor.execute('UPDATE resources SET steel = steel - ?, gasoline = gasoline - ? WHERE name = ? ', (usage_tank_steel, usage_tank_gas, name))
                            conn.commit()

                            # Update tank count.
                            cursor.execute('UPDATE user_mil SET tanks = tanks + ? WHERE name = ?', (prod_tank, name))
                            conn.commit()

                            allo_done = discord.Embed(title='Allocation | Tank', type='rich', colour=0xDD7878,
                                                      description=f'Allocation Complete! {amount:,} military factories have been allocated.')
                            await allo_emb.edit(embed=allo_done)

                    case "plane":
                        if amount > militaryfactory:  # If user doesn't have enough mil factories, the command exits.
                            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                                  description="You do not have enough military factories.")
                            await ctx.send(embed=embed)
                            return

                        else:
                            allocating = discord.Embed(title='Allocation | Plane', type='rich', colour=0xDD7878,
                                                       description=f'Allocating {amount:,} to {mil_type}...')
                            allo_emb = await ctx.send(embed=allocating)

                            prod_plane = amount * militaryfactory // 45
                            usage_plane_steel = amount * 5.75
                            usage_plane_gas = amount * 2

                            # Update military factory count.
                            cursor.execute('UPDATE infra SET militaryfactory = militaryfactory - ? WHERE name = ?', (amount, name))
                            conn.commit()

                            # Update factory count.
                            cursor.execute('UPDATE user_mil SET plane_factory = plane_factory + ? WHERE name = ?', (amount, name))
                            conn.commit()

                            # Update resources.
                            cursor.execute('UPDATE resources SET steel = steel - ?, gasoline = gasoline - ? WHERE name = ? ', (usage_plane_steel, usage_plane_gas, name))
                            conn.commit()

                            # Update tank count.
                            cursor.execute('UPDATE user_mil SET planes = planes + ? WHERE name = ?', (prod_plane, name))
                            conn.commit()

                            allo_done = discord.Embed(title='Allocation | Plane', type='rich', colour=0xDD7878,
                                                      description=f'Allocation Complete! {amount:,} military factories have been allocated.')
                            await allo_emb.edit(embed=allo_done)

                    case "artillery":
                        if amount > militaryfactory:  # If user doesn't have enough mil factories, the command exits.
                            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                                  description="You do not have enough military factories.")
                            await ctx.send(embed=embed)
                            return

                        else:
                            allocating = discord.Embed(title='Allocation | Artillery', type='rich', colour=0xDD7878,
                                                       description=f'Allocating {amount:,} to {mil_type}...')
                            allo_emb = await ctx.send(embed=allocating)

                            prod_arty = amount * militaryfactory // 42
                            usage_arty_steel = amount * 3
                            usage_arty_gas = amount * 0.75

                            # Update military factory count.
                            cursor.execute('UPDATE infra SET militaryfactory = militaryfactory - ? WHERE name = ?', (amount, name))
                            conn.commit()

                            # Update factory count.
                            cursor.execute('UPDATE user_mil SET artillery_factory = artillery_factory + ? WHERE name = ?', (amount, name))
                            conn.commit()

                            # Update resources.
                            cursor.execute('UPDATE resources SET steel = steel - ?, gasoline = gasoline - ? WHERE name = ? ', (usage_arty_steel, usage_arty_gas, name))
                            conn.commit()

                            # Update tank count.
                            cursor.execute('UPDATE user_mil SET artillery = artillery + ? WHERE name = ?', (prod_arty, name))
                            conn.commit()

                            allo_done = discord.Embed(title='Allocation | Artillery', type='rich', colour=0xDD7878,
                                                      description=f'Allocation Complete! {amount:,} military factories have been allocated.')
                            await allo_emb.edit(embed=allo_done)

                    case "anti-air":
                        if amount > militaryfactory:  # If user doesn't have enough mil factories, the command exits.
                            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                                  description="You do not have enough military factories.")
                            await ctx.send(embed=embed)
                            return

                        else:
                            allocating = discord.Embed(title='Allocation | Anti-air', type='rich', colour=0xDD7878,
                                                       description=f'Allocating {amount:,} to {mil_type}...')
                            allo_emb = await ctx.send(embed=allocating)

                            prod_aa = amount * militaryfactory // 42
                            usage_aa_steel = amount * 4
                            usage_aa_gas = amount * 1

                            # Update military factory count.
                            cursor.execute('UPDATE infra SET militaryfactory = militaryfactory - ? WHERE name = ?', (amount, name))
                            conn.commit()

                            # Update factory count.
                            cursor.execute('UPDATE user_mil SET anti_air_factory = anti_air_factory + ? WHERE name = ?', (amount, name))
                            conn.commit()

                            # Update resources.
                            cursor.execute('UPDATE resources SET steel = steel - ?, gasoline = gasoline - ? WHERE name = ? ', (usage_aa_steel, usage_aa_gas, name))
                            conn.commit()

                            # Update tank count.
                            cursor.execute('UPDATE user_mil SET anti_air = anti_air + ? WHERE name = ?', (prod_aa, name))
                            conn.commit()

                            allo_done = discord.Embed(title='Allocation | Anti-air', type='rich', colour=0xDD7878,
                                                      description=f'Allocation Complete! {amount:,} military factories have been allocated.')
                            await allo_emb.edit(embed=allo_done)
            else:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description=f'Cannot find stats.')
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    # Deallocate Command.
    @commands.command()
    async def deallocate(self, ctx, mil_type: str, amount: int):
        mil_type = mil_type.lower()
        user_id = ctx.author.id

        if amount <= 0:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description="Invalid amount, please try a positive number.")
            await ctx.send(embed=embed)
            return

        # fetch username
        cursor.execute('SELECT name FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            name = result[0]

            # fetch user's resources
            cursor.execute(
                'SELECT wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                (name,))
            res_result = cursor.fetchone()

            # fetch user's production infra
            cursor.execute(
                'SELECT basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps FROM infra WHERE name = ?',
                (name,))
            infra_result = cursor.fetchone()

            # fetch user's military stats
            cursor.execute(
                'SELECT troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory FROM user_mil WHERE name = ?',
                (name,))
            mil_result = cursor.fetchone()

            if mil_result and res_result and infra_result:
                troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result
                wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result
                basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps = infra_result

                match mil_type:
                    case "tank":
                        if amount > tank_factory:  # If user doesn't have enough mil factories, the command exits.
                            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                                  description="You cannot deallocate more than you have.")
                            await ctx.send(embed=embed)
                            return

                        else:
                            deallocating = discord.Embed(title='Deallocation | Tank', type='rich', colour=0xDD7878,
                                                         description=f'Deallocating {amount:,} tank factories back to Military factories...')
                            deallo_emb = await ctx.send(embed=deallocating)

                            # Update military factory count.
                            cursor.execute('UPDATE infra SET militaryfactory = militaryfactory + ? WHERE name = ?', (amount, name))
                            conn.commit()

                            # Update factory count.
                            cursor.execute('UPDATE user_mil SET tank_factory = tank_factory - ? WHERE name = ?', (amount, name))
                            conn.commit()

                            deallo_done = discord.Embed(title='Deallocation | Tank', type='rich', colour=0xDD7878,
                                                        description=f'Deallocation Complete! {amount:,} military factories have been deallocated.')
                            await deallo_emb.edit(embed=deallo_done)

                    case "plane":
                        if amount > plane_factory:  # If user doesn't have enough mil factories, the command exits.
                            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                                  description="You cannot deallocate more than you have.")
                            await ctx.send(embed=embed)
                            return

                        else:
                            deallocating = discord.Embed(title='Deallocation | Plane', type='rich', colour=0xDD7878,
                                                         description=f'Deallocating {amount:,} plane factories back to Military factories...')
                            deallo_emb = await ctx.send(embed=deallocating)

                            # Update military factory count.
                            cursor.execute('UPDATE infra SET militaryfactory = militaryfactory + ? WHERE name = ?', (amount, name))
                            conn.commit()

                            # Update factory count.
                            cursor.execute('UPDATE user_mil SET plane_factory = plane_factory - ? WHERE name = ?', (amount, name))
                            conn.commit()

                            deallo_done = discord.Embed(title='Deallocation | Plane', type='rich', colour=0xDD7878,
                                                        description=f'Deallocation Complete! {amount:,} military factories have been deallocated.')
                            await deallo_emb.edit(embed=deallo_done)

                    case "artillery":
                        if amount > artillery_factory:  # If user doesn't have enough mil factories, the command exits.
                            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                                  description="You cannot deallocate more than you have.")
                            await ctx.send(embed=embed)
                            return

                        else:
                            deallocating = discord.Embed(title='Deallocation | Artillery', type='rich', colour=0xDD7878,
                                                         description=f'Deallocating {amount:,} artillery factories back to Military factories...')
                            deallo_emb = await ctx.send(embed=deallocating)

                            # Update military factory count.
                            cursor.execute('UPDATE infra SET militaryfactory = militaryfactory + ? WHERE name = ?', (amount, name))
                            conn.commit()

                            # Update factory count.
                            cursor.execute('UPDATE user_mil SET artillery_factory = artillery_factory - ? WHERE name = ?', (amount, name))
                            conn.commit()

                            deallo_done = discord.Embed(title='Deallocation | Artillery', type='rich', colour=0xDD7878,
                                                        description=f'Deallocation Complete! {amount:,} military factories have been deallocated.')
                            await deallo_emb.edit(embed=deallo_done)

                    case "anti-air":
                        if amount > anti_air_factory:  # If user doesn't have enough mil factories, the command exits.
                            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                                  description="You cannot deallocate more than you have.")
                            await ctx.send(embed=embed)
                            return

                        else:
                            deallocating = discord.Embed(title='Deallocation | Anti-air', type='rich', colour=0xDD7878,
                                                         description=f'Deallocating {amount:,} anti-air factories back to Military factories...')
                            deallo_emb = await ctx.send(embed=deallocating)

                            # Update military factory count.
                            cursor.execute('UPDATE infra SET militaryfactory = militaryfactory + ? WHERE name = ?', (amount, name))
                            conn.commit()

                            # Update factory count.
                            cursor.execute('UPDATE user_mil SET anti_air_factory = anti_air_factory - ? WHERE name = ?', (amount, name))
                            conn.commit()

                            deallo_done = discord.Embed(title='Deallocation | Anti-air', type='rich', colour=0xDD7878,
                                                        description=f'Deallocation Complete! {amount:,} military factories have been deallocated.')
                            await deallo_emb.edit(embed=deallo_done)
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
    await bot.add_cog(Military(bot))
