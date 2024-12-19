import discord
from discord.ext import commands
from schema import *

new_line = '\n'

class Demolish(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def demolish(self, ctx, building: str = '', amount: int = 0):
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

            # fetch user's production infra
            buildings = Infra.select(
                Infra.basic_house, Infra.small_flat, Infra.apt_complex, 
                Infra.skyscraper, Infra.lumber_mill, Infra.coal_mine, 
                Infra.iron_mine, Infra.lead_mine, Infra.bauxite_mine, 
                Infra.oil_derrick, Infra.uranium_mine, Infra.farm, 
                Infra.aluminium_factory, Infra.steel_factory, Infra.oil_refinery, 
                Infra.ammo_factory, Infra.concrete_factory, Infra.militaryfactory, 
                Infra.corps, Infra.park, Infra.cinema, Infra.museum, Infra.concert_hall).where(Infra.name == name).tuples().first()

            mil_barracks = UserMil.select().where(UserMil.name == name).first()

            if buildings and mil_barracks:
                barracks = mil_barracks.barracks
                buildings = list(buildings)

                building_list = ["Basic House", "Small Flat", "Apartment Complex", "Skyscraper", "Lumbermill", "Coal Mine", "Iron Mine", "Lead Mine", "Bauxite Mine", "Oil Derrick", "Uranium Mine", "Farm", "Aluminium Factory", "Steel Factory", "Oil Refinery", "Munitions Factory", "Concrete Factory", "Military Factory", "Barrack", "Park", "Cinema", "Museum", "Concert Hall"]
                build_list_code = ["basic_house", "small_flat", "apt_complex", "skyscraper", "lumber_mill", "coal_mine", "iron_mine", "lead_mine", "bauxite_mine", "oil_derrick", "uranium_mine", "farm", "aluminium_factory", "steel_factory", "oil_refinery", "ammo_factory", "concrete_factory", "militaryfactory", "barracks", "park", "cinema", "museum", "concert_hall"]
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

                if buildings[build_id] >= amount:
                    embed = discord.Embed(title="Demolish", type='rich',
                                          description=f"{amount:,} {building_list[build_id].lower()} will be demolished.",
                                          color=0xE78284)
                    demolish_emb = await ctx.send(embed=embed)

                    # Remove the buildings from user's infra.
                    if build_id != 18:
                        field_name = build_list_code[build_id]
                        field = getattr(Infra, field_name)
                        Infra.update({field: field - amount}).where(Infra.name == name).execute()
                    else:
                        field_name = build_list_code[build_id]
                        field = getattr(UserMil, field_name)
                        UserMil.update({field: field - amount}).where(UserMil.name == name).execute()

                    if amount == 1:
                        description = f"One {building_list[build_id].lower()} has been demolished."
                    else:
                        description = f"{amount:,} {building_list[build_id].lower() + 's'} have been demolished."

                    done_emb = discord.Embed(title="Demolish", type='rich', description=description, color=0xE78284)
                    await demolish_emb.edit(embed=done_emb)
                else:
                    embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                          description=f'Cannot demolish more {build_list_code[build_id].lower() + 's'} than you have.')
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
    await bot.add_cog(Demolish(bot))
