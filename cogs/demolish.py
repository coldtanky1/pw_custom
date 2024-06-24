import sqlite3
import discord
from discord.ext import commands
import globals

new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = globals.conn
cursor = globals.cursor


class Demolish(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def demolish(self, ctx, building: str = None, amount: int = 0):
        user_id = ctx.author.id

        if building is None:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Please specify a building.')
            await ctx.send(embed=embed)
            return

        building = building.lower()

        if amount <= 0:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f"Amount must be a value that is greater than 0!")
            await ctx.send(embed=embed)
            return

        # fetch username
        cursor.execute('SELECT name FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            name = result[0]

            # fetch user's production infra
            cursor.execute(
                'SELECT basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps FROM infra WHERE name = ?',
                (name,))
            buildings = cursor.fetchone()

            cursor.execute('SELECT barracks FROM user_mil WHERE name = ?', (name, ))
            barracks = cursor.fetchone()
            buildings = list(buildings)

            if buildings and barracks:
                buildings.append(barracks[0])
                building_list = ["Basic House", "Small Flat", "Apartment Complex", "Skyscraper", "Lumbermill", "Coal Mine", "Iron Mine", "Lead Mine", "Bauxite Mine", "Oil Derrick", "Uranium Mine", "Farm", "Aluminium Factory", "Steel Factory", "Oil Refinery", "Munitions Factory", "Concrete Factory", "Military Factory", "Corporation", "Barrack"]
                build_list_code = ["basic_house", "small_flat", "apt_complex", "skyscraper", "lumber_mill", "coal_mine", "iron_mine", "lead_mine", "bauxite_mine", "oil_derrick", "uranium_mine", "farm", "aluminium_factory", "steel_factory", "oil_refinery", "ammo_factory", "concrete_factory", "militaryfactory", "corp", "barracks"]
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
                    case "corp" | "corporation":
                        # CT leaving this empty because I'm unsure of how you want to deal with corporations, but if you intend for it to be similar to buildings, the build_id is 18
                        return
                    case "barrack" | "barracks":
                        build_id = 19
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
                    if build_id != 19:
                        query = '''UPDATE infra SET {0} = {0} - {1} WHERE name = "{2}"'''.format(build_list_code[build_id], amount, name)
                    else:
                        query = '''UPDATE user_mil SET {0} = {0} - {1} WHERE name = "{2}"'''.format(build_list_code[build_id], amount, name)
                    cursor.execute(query)
                    conn.commit()

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
