import sqlite3
import asyncio
import discord
from discord.ext import commands
import globals

new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = globals.conn
cursor = globals.cursor

# Structure: name, wood cost, concrete cost, steel cost
structures = [
    ("Basic House",       2,   0.6, 0),
    ("Small Flat",        1,   6,   0.5),
    ("Apartment Complex", 1,   7,   0.6),
    ("Skyscraper",        0,   10,  2),
    ("Lumbermill",        0.4, 0,   0),
    ("Coal Mine",         2,   0,   0),
    ("Iron Mine",         2,   0,   0),
    ("Lead Mine",         2,   0,   0),
    ("Bauxite Mine",      2,   0,   0),
    ("Oil Derrick",       0,   1,   3),
    ("Uranium Mine",      5,   0.5, 0.3),
    ("Farm",              5,   0.5, 0.2),
    ("Aluminium Factory", 0,   4,   3),
    ("Steel Factory",     0,   6,   4),
    ("Oil Refinery",      2,   4,   4),
    ("Munition Factory",  0,   1.2, 0.6),
    ("Concrete Factory",  2,   6,   2),
    ("Military Factory",  0,   5, 2.75),
    ("Barrack",           0,   2,   3),
    ("Park",              1,   2,   1),
    ("Cinema",            2,   4,   2),
    ("Museum",            0.5,   5,   1),
    ("Concert Hall",       2,   6,   3)
]

build_list_code = ["basic_house", "small_flat", "apt_complex", "skyscraper", "lumber_mill", "coal_mine", "iron_mine", "lead_mine", "bauxite_mine", "oil_derrick", "uranium_mine", "farm", "aluminium_factory", "steel_factory", "oil_refinery", "ammo_factory", "concrete_factory", "militaryfactory", "barracks", "park", "cinema", "museum", "concert_hall"]

class Construct(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def construct(self, ctx, building: str = None, amount: int = 0):
        user_id = ctx.author.id

        if building is None:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Please specify a building.')
            await ctx.send(embed=embed)
            return

        building = building.lower()

        if amount <= 0:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f"Amount must be positive.")
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
                'SELECT basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps, park, cinema, museum, concert_hall FROM infra WHERE name = ?',
                (name,))
            infra_result = cursor.fetchone()

            cursor.execute('SELECT balance FROM user_stats WHERE name = ?', (name,))
            bal = cursor.fetchone()

            if infra_result:
                basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps, park, cinema, museum, concert_hall = infra_result
                match building:
                    case "basichouse" | "basic_house":
                        build_id = 0
                    case "small_flat" | "smallflat":
                        build_id = 1
                    case "apt_complex" | "apartment" | "aptcomplex" | "complex":
                        build_id = 2
                    case "skyscraper" | "sky_scraper":
                        build_id = 3
                    case "lumbermill" | "wood":
                        build_id = 4
                    case "coalmine" | "coal":
                        build_id = 5
                    case "ironmine" | "iron":
                        build_id = 6
                    case "leadmine" | "lead":
                        build_id = 7
                    case "bauxitemine" | "bauxite":
                        build_id = 8
                    case "oilderrick" | "oil":
                        build_id = 9
                    case "uraniummine" | "uranium":
                        build_id = 10
                    case "farm" | "food":
                        build_id = 11
                    case "aluminiumfactory" | "aluminium":
                        build_id = 12
                    case "steelfactory" | "steel":
                        build_id = 13
                    case "oilrefinery" | "gas":
                        build_id = 14
                    case "munitionfactory" | "ammo" | "ammofactory":
                        build_id = 15
                    case "concretefactory" | "concrete":
                        build_id = 16
                    case "militaryfactory" | "mil":
                        build_id = 17
                    case "barrack" | "barracks":
                        build_id = 18
                    case "park":
                        build_id = 19
                    case "cinema":
                        build_id = 20
                    case "museum":
                        build_id = 21
                    case "concerthall" | "concert":
                        build_id = 22
                    case _:
                        embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                              description=f'Building not found.')
                        await ctx.send(embed=embed)
                        return

                wood_cost = amount * structures[build_id][1]
                concrete_cost = amount * structures[build_id][2]
                steel_cost = amount * structures[build_id][3]

                if build_id == 19:
                    if amount > 19 or park >= 19:
                        over_limit = discord.Embed(colour=0xEF2F73, title='Error', type='rich',
                                                                description='You cannot build more than 19 entertainment buildings!')
                        await ctx.send(embed=over_limit)
                        return
                elif build_id == 20:
                    if amount > 19 or cinema >= 19:
                        over_limit = discord.Embed(colour=0xEF2F73, title='Error', type='rich',
                                                                description='You cannot build more than 19 entertainment buildings!')
                        await ctx.send(embed=over_limit)
                        return
                elif build_id == 21:
                    if amount > 19 or museum >= 19:
                        over_limit = discord.Embed(colour=0xEF2F73, title='Error', type='rich',
                                                                description='You cannot build more than 19 entertainment buildings!')
                        await ctx.send(embed=over_limit)
                        return
                elif build_id == 22:
                    if amount > 19 or concert_hall >= 19:
                        over_limit = discord.Embed(colour=0xEF2F73, title='Error', type='rich',
                                                                description='You cannot build more than 19 entertainment buildings!')
                        await ctx.send(embed=over_limit)
                        return

                embed = discord.Embed(colour=0xdd7878, title=f"Construct: {structures[build_id][0]}", type='rich',
                                      description=f'{amount:,} will be constructed.{new_line}{new_line}'
                                                  f'This will cost: {new_line}{new_line}'
                                                  f'{wood_cost:,} Wood{new_line}'
                                                  f'{concrete_cost:,} Concrete{new_line}'
                                                  f'{steel_cost:,} Steel')
                await ctx.send(embed=embed)

                try:
                    await ctx.send("Would you like to proceed? Respond with y/n.")

                    def check(message):
                        return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() in [
                            'y', 'n']

                    response_message = await self.bot.wait_for('message', timeout=30, check=check)

                    if response_message.content.lower() == 'y':
                        constructing = discord.Embed(colour=0xdd7878, title='Construct', type='rich',
                                                     description='Constructing...')
                        construct_msg = await ctx.send(embed=constructing)

                        if res_result:
                            wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                            # Check if user has enough resources
                            if (wood >= wood_cost) and (concrete >= concrete_cost) and (steel >= steel_cost):

                                # If user has enough resources then it proceeds normally.
                                # Update the resources table
                                cursor.execute('''
                                                UPDATE resources SET
                                                wood = wood - ?,
                                                concrete = concrete - ?,
                                                steel = steel - ?
                                                WHERE name = ?
                                            ''', (wood_cost, concrete_cost, steel_cost, name))

                                if build_id != 18:
                                    query = '''UPDATE infra SET {0} = {0} + {1} WHERE name = "{2}"'''.format(
                                        build_list_code[build_id], amount, name)
                                else:
                                    query = '''UPDATE user_mil SET {0} = {0} + {1} WHERE name = "{2}"'''.format(
                                        build_list_code[build_id], amount, name)
                                cursor.execute(query)
                                conn.commit()

                                cons_done = discord.Embed(colour=0xdd7878, title='Contruct', type='rich',
                                                          description='Construction complete!')
                                await construct_msg.edit(embed=cons_done)

                            else:
                                wood_req = wood_cost - wood
                                concrete_req = concrete_cost - concrete
                                steel_req = steel_cost - steel
                                required = ""

                                cons_error = discord.Embed(colour=0xEF2F73, title='Error', type='rich',
                                                           description='You do not have enough resources.')
                                if wood_req > 0:
                                    required += f"Wood: {wood_req:,}{new_line}"
                                if concrete_req > 0:
                                    required += f"Concrete: {concrete_req:,}{new_line}"
                                if steel_req > 0:
                                    required += f"Steel: {steel_req:,}{new_line}"
                                if required.endswith('\n'):
                                    required = required[:-1]
                                    cons_error.add_field(name="", value=f"Resources missing:{new_line}{new_line}"
                                                                        f"{required}")

                                cons_error.set_footer(text="If you want to use auto-complete reply with `Y`")
                                await construct_msg.edit(embed=cons_error)

                                try:
                                    def check(message):
                                        return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() in [
                                            'y', 'n']
                                    
                                    response_message = await self.bot.wait_for('message', timeout=30, check=check)

                                    if response_message.content.lower() == 'y':
                                        total_price = (wood_req * 12) + (concrete_req * 1000) + (steel_req * 1875)

                                        if bal:
                                            balance = bal[0]

                                            # if the user doesn't have enough money.
                                            if balance < total_price:
                                                embed = discord.Embed(colour=0xEF2F73, title='Error', type='rich',
                                                           description='You do not have enough money for auto-complete.')
                                                await ctx.send(embed=embed)
                                                return
                                            
                                            else:
                                                cursor.execute('UPDATE user_stats SET balance = balance - ? WHERE name = ?', (total_price, name))
                                                conn.commit()

                                                if build_id != 18:
                                                    query = '''UPDATE infra SET {0} = {0} + {1} WHERE name = "{2}"'''.format(
                                                        build_list_code[build_id], amount, name)
                                                else:
                                                    query = '''UPDATE user_mil SET {0} = {0} + {1} WHERE name = "{2}"'''.format(
                                                        build_list_code[build_id], amount, name)
                                                cursor.execute(query)
                                                conn.commit()

                                                cons_done = discord.Embed(colour=0xdd7878, title='Contruct', type='rich',
                                                          description='Construction complete!')
                                                await construct_msg.edit(embed=cons_done)
                    
                                except asyncio.TimeoutError:
                                    return await ctx.send("You took too long to respond.")
                    else:
                        await ctx.send("Aborting.")
                        return
                except asyncio.TimeoutError:
                    return await ctx.send("You took too long to respond.")

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
    await bot.add_cog(Construct(bot))
