import asyncio
import discord
from discord.ext import commands
from schema import UserMil, UserStats, UserInfo, Resources, Infra

new_line = '\n'

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
    async def construct(self, ctx, building: str = '', amount: int = 0):
        user_id = ctx.author.id

        if building == '':
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
        result = UserInfo.select().where(UserInfo.user_id == user_id).first()

        if result:
            name = result.name

            # fetch user's resources
            res_result = Resources.select(Resources.concrete, Resources.wood, Resources.steel).where(Resources.name == name).tuples().first()

            # fetch user's production infra
            infra_result = Infra.select(Infra.park, Infra.cinema, Infra.museum, Infra.concert_hall).where(Infra.name == name).tuples().first()

            # fetch user's balance
            bal = UserStats.select().where(UserStats.name == name).first()

            if infra_result:
                park, cinema, museum, concert_hall = infra_result
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
                            wood, steel, concrete = res_result

                            # Check if user has enough resources
                            if (wood >= wood_cost) and (concrete >= concrete_cost) and (steel >= steel_cost):

                                # If user has enough resources then it proceeds normally.
                                # Update the resources table
                                Resources.update(wood=Resources.wood - wood_cost, concrete=Resources.concrete - concrete_cost, steel=Resources.steel - steel_cost).where(
                                    Resources.name == name).execute()

                                if build_id != 18:
                                    field_name = build_list_code[build_id]
                                    field = getattr(Infra, field_name)
                                    Infra.update({field: field + amount}).where(Infra.name == name).execute()
                                else:
                                    field_name = build_list_code[build_id]
                                    field = getattr(UserMil, field_name)
                                    UserMil.update({field: field + amount}).where(UserMil.name == name).execute()


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
                                            balance = bal.balance

                                            # if the user doesn't have enough money.
                                            if balance < total_price:
                                                embed = discord.Embed(colour=0xEF2F73, title='Error', type='rich',
                                                           description='You do not have enough money for auto-complete.')
                                                await ctx.send(embed=embed)
                                                return
                                            
                                            else:
                                                UserStats.update(balance=UserStats.balance - total_price).where(UserStats.name == name).execute()

                                                if build_id != 18:
                                                    field_name = build_list_code[build_id]
                                                    field = getattr(Infra, field_name)
                                                    
                                                    Infra.update({field: field + amount}).where(Infra.name == name).execute()
                                                else:
                                                    field_name = build_list_code[build_id]
                                                    field = getattr(UserMil, field_name)

                                                    UserMil.update({field: field + amount}).where(UserMil.name == name).execute()

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
