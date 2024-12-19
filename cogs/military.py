import asyncio
import discord
from discord.ext import commands
from discord.utils import get
from schema import *

new_line = '\n'


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
        result = UserInfo.select(UserInfo.name, UserInfo.gov_type).where(UserInfo.user_id == user_id).tuples().first()

        if result:
            name, gov_type = result

            # fetch user's resources
            res_result = Resources.select(Resources.food, Resources.ammo).where(Resources.name == name).tuples().first()

            if res_result:
                food, ammo = res_result
                
                bonus = 1
                if gov_type == "Fascism":
                    bonus /= 2

                inf_ammo = round((amount * 0.2) * bonus)
                inf_food = round((amount * 0.03) * bonus)
                inf_turns = round(amount * 0.00003 + 1)
                inf_time = int(inf_turns)
                time_turns = inf_time * 3600

                if (ammo < inf_ammo) and (food < inf_food):
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

                    UserStats.update(adult=UserStats.adult - amount).where(UserStats.name == name).execute()

                    UserMil.update(troops=UserMil.troops + amount).where(UserMil.name == name).execute()
            else:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description=f'Cannot find stats.')
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command()
    async def allocate(self, ctx, mil_type: str = '', amount: int = 0):
        mil_type = mil_type.lower()
        user_id = ctx.author.id

        if amount <= 0 or mil_type == '':
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description="Invalid amount/mil_type, please try again.")
            await ctx.send(embed=embed)
            return

        # fetch username
        result = UserInfo.select().where(UserInfo.user_id == user_id).first()

        if result:
            name = result.name

            # fetch user's production infra
            infra_result = Infra.select(Infra.militaryfactory).where(Infra.name == name).first()

            if infra_result:
                militaryfactory = infra_result.militaryfactory

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
                            Infra.update(militaryfactory=Infra.militaryfactory - amount).where(Infra.name == name).execute()

                            # Update factory count.
                            UserMil.update(tank_factory=UserMil.tank_factory + amount,
                                tanks=UserMil.tanks + prod_tank).where(UserMil.name == name).execute()

                            # Update resources.
                            Resources.update(
                                steel=Resources.steel - usage_tank_steel,
                                gasoline=Resources.gasoline - usage_tank_gas).where(Resources.name == name).execute()

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
                            Infra.update(militaryfactory=Infra.militaryfactory - amount).where(Infra.name == name).execute()

                            # Update factory count.
                            UserMil.update(plane_factory=UserMil.plane_factory + amount,
                                planes=UserMil.planes + prod_plane).where(UserMil.name == name).execute()

                            # Update resources.
                            Resources.update(
                                steel=Resources.steel - usage_plane_steel,
                                gasoline=Resources.gasoline - usage_plane_gas).where(Resources.name == name).execute()

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
                            Infra.update(militaryfactory=Infra.militaryfactory - amount).where(Infra.name == name).execute()

                            # Update factory count.
                            UserMil.update(
                                artillery=UserMil.artillery + prod_arty,
                                artillery_factory=UserMil.artillery_factory + amount).where(UserMil.name == name).execute()

                            # Update resources.
                            Resources.update(
                                steel=Resources.steel - usage_arty_steel,
                                gasoline=Resources.gasoline - usage_arty_gas).where(Resources.name == name).execute()

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
                            Infra.update(militaryfactory=Infra.militaryfactory - amount).where(Infra.name == name).execute()

                            # Update factory count.
                            UserMil.update(anti_air=UserMil.anti_air + prod_aa, anti_air_factory=UserMil.anti_air_factory + amount).where(
                                UserMil.name == name).execute()

                            # Update resources.
                            Resources.update(steel=Resources.steel - usage_aa_steel, gasoline=Resources.gasoline - usage_aa_gas).where(
                             Resources.name == name).execute()

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
    async def deallocate(self, ctx, mil_type: str = "", amount: int = 0):
        mil_type = mil_type.lower()
        user_id = ctx.author.id

        if amount <= 0 or mil_type == "":
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description="Invalid amount/mil_type, please try again.")
            await ctx.send(embed=embed)
            return

        # fetch username
        result = UserInfo.select().where(UserInfo.user_id == user_id).first()

        if result:
            name = result.name

            # fetch user's military stats
            mil_result = UserMil.select(UserMil.tank_factory, UserMil.plane_factory,
                UserMil.artillery_factory, UserMil.anti_air_factory).where(UserMil.name == name).tuples().first()

            if mil_result:
                tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result

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
                            Infra.update(militaryfactory=Infra.militaryfactory + amount).where(Infra.name == name).execute()

                            # Update factory count.
                            UserMil.update(tank_factory=UserMil.tank_factory - amount).where(UserMil.name == name).execute()

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
                            Infra.update(militaryfactory=Infra.militaryfactory + amount).where(Infra.name == name).execute()

                            # Update factory count.
                            UserMil.update(plane_factory=UserMil.plane_factory - amount).where(UserMil.name == name).execute()

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
                            Infra.update(militaryfactory=Infra.militaryfactory + amount).where(Infra.name == name).execute()

                            # Update factory count.
                            UserMil.update(artillery_factory=UserMil.artillery_factory - amount).where(UserMil.name == name).execute()

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
                            Infra.update(militaryfactory=Infra.militaryfactory + amount).where(Infra.name == name).execute()

                            # Update factory count.
                            UserMil.update(anti_air_factory=UserMil.anti_air_factory - amount).where(UserMil.name == name).execute()

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
