import sqlite3
import discord
from discord.ext import commands

new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = sqlite3.connect('player_info.db')
cursor = conn.cursor()


class Demolish(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def demolish(self, ctx, building: str, amount: int):
        user_id = ctx.author.id
        building = building.lower()

        if amount <= 0:
            await ctx.send("Invalid building amount, try a positive number.")
            return

        # fetch user name
        cursor.execute('SELECT name FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            name = result[0]

            # fetch user's production infra
            cursor.execute(
                'SELECT name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps FROM infra WHERE name = ?',
                (name,))
            infra_result = cursor.fetchone()

            if infra_result:
                name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps = infra_result

                match building:
                    case "basichouse" | "basic_house":
                        embed = discord.Embed(title="Demolish", type='rich',
                                              description=f"{amount:,} Basic houses will be demolished.", color=discord.Color.red())
                        demolish_emb = await ctx.send(embed=embed)

                        # Remove the buildings from user's infra.
                        cursor.execute('UPDATE infra SET basic_house = basic_house - ? WHERE name = ?', (amount, name))
                        conn.commit()

                        done_emb = discord.Embed(title="Demolish", type='rich',
                                                 description="Basic houses have been demolished.", color=discord.Color.red())
                        await demolish_emb.edit(embed=done_emb)
                    case "small_flat" | "smallflat":
                        embed = discord.Embed(title="Demolish", type='rich',
                                              description=f"{amount:,} Small flats will be demolished.",
                                              color=discord.Color.red())
                        demolish_emb = await ctx.send(embed=embed)

                        # Remove the buildings from user's infra.
                        cursor.execute('UPDATE infra SET small_flat = small_flat - ? WHERE name = ?',
                                       (amount, name))
                        conn.commit()

                        done_emb = discord.Embed(title="Demolish", type='rich',
                                                 description="Small flats have been demolished.",
                                                 color=discord.Color.red())
                        await demolish_emb.edit(embed=done_emb)
                    case "apt_complex" | "apartment" | "aptcomplex" | "complex":
                        embed = discord.Embed(title="Demolish", type='rich',
                                              description=f"{amount:,} Apt. complexes will be demolished.",
                                              color=discord.Color.red())
                        demolish_emb = await ctx.send(embed=embed)

                        # Remove the buildings from user's infra.
                        cursor.execute('UPDATE infra SET apt_complex = apt_complex - ? WHERE name = ?',
                                       (amount, name))
                        conn.commit()

                        done_emb = discord.Embed(title="Demolish", type='rich',
                                                 description="Apt. complexes have been demolished.",
                                                 color=discord.Color.red())
                        await demolish_emb.edit(embed=done_emb)
                    case "skyscraper" | "sky_scraper":
                        embed = discord.Embed(title="Demolish", type='rich',
                                              description=f"{amount:,} Skyscrapers will be demolished.", color=discord.Color.red())
                        demolish_emb = await ctx.send(embed=embed)

                        # Remove the buildings from user's infra.
                        cursor.execute('UPDATE infra SET skyscraper = skyscraper - ? WHERE name = ?', (amount, name))
                        conn.commit()

                        done_emb = discord.Embed(title="Demolish", type='rich',
                                                 description="Skyscrapers have been demolished.", color=discord.Color.red())
                        await demolish_emb.edit(embed=done_emb)
                    case "lumbermill" | "wood":
                        embed = discord.Embed(title="Demolish", type='rich',
                                              description=f"{amount:,} Lumber mills will be demolished.",
                                              color=discord.Color.red())
                        demolish_emb = await ctx.send(embed=embed)

                        # Remove the buildings from user's infra.
                        cursor.execute('UPDATE infra SET lumber_mill = lumber_mill - ? WHERE name = ?',
                                       (amount, name))
                        conn.commit()

                        done_emb = discord.Embed(title="Demolish", type='rich',
                                                 description="Lumber mills have been demolished.",
                                                 color=discord.Color.red())
                        await demolish_emb.edit(embed=done_emb)
                    case "coalmine" | "coal":
                        embed = discord.Embed(title="Demolish", type='rich',
                                              description=f"{amount:,} Coal Mines will be demolished.",
                                              color=discord.Color.red())
                        demolish_emb = await ctx.send(embed=embed)

                        # Remove the buildings from user's infra.
                        cursor.execute('UPDATE infra SET coal_mine = coal_mine - ? WHERE name = ?',
                                       (amount, name))
                        conn.commit()

                        done_emb = discord.Embed(title="Demolish", type='rich',
                                                 description="Coal Mines have been demolished.",
                                                 color=discord.Color.red())
                        await demolish_emb.edit(embed=done_emb)
                    case "ironmine" | "iron":
                        embed = discord.Embed(title="Demolish", type='rich',
                                              description=f"{amount:,} Iron Mines will be demolished.",
                                              color=discord.Color.red())
                        demolish_emb = await ctx.send(embed=embed)

                        # Remove the buildings from user's infra.
                        cursor.execute('UPDATE infra SET iron_mine = iron_mine - ? WHERE name = ?',
                                       (amount, name))
                        conn.commit()

                        done_emb = discord.Embed(title="Demolish", type='rich',
                                                 description="Iron Mines have been demolished.",
                                                 color=discord.Color.red())
                        await demolish_emb.edit(embed=done_emb)
                    case "leadmine" | "lead":
                        embed = discord.Embed(title="Demolish", type='rich',
                                              description=f"{amount:,} Lead Mines will be demolished.",
                                              color=discord.Color.red())
                        demolish_emb = await ctx.send(embed=embed)

                        # Remove the buildings from user's infra.
                        cursor.execute('UPDATE infra SET lead_mine = lead_mine - ? WHERE name = ?',
                                       (amount, name))
                        conn.commit()

                        done_emb = discord.Embed(title="Demolish", type='rich',
                                                 description="Lead Mines have been demolished.",
                                                 color=discord.Color.red())
                        await demolish_emb.edit(embed=done_emb)
                    case "bauxitemine" | "bauxite":
                        embed = discord.Embed(title="Demolish", type='rich',
                                              description=f"{amount:,} Bauxite Mines will be demolished.",
                                              color=discord.Color.red())
                        demolish_emb = await ctx.send(embed=embed)

                        # Remove the buildings from user's infra.
                        cursor.execute('UPDATE infra SET bauxite_mine = bauxite_mine - ? WHERE name = ?',
                                       (amount, name))
                        conn.commit()

                        done_emb = discord.Embed(title="Demolish", type='rich',
                                                 description="Bauxite Mines have been demolished.",
                                                 color=discord.Color.red())
                        await demolish_emb.edit(embed=done_emb)
                    case "oilderrick" | "oil":
                        embed = discord.Embed(title="Demolish", type='rich',
                                              description=f"{amount:,} Oil derricks will be demolished.",
                                              color=discord.Color.red())
                        demolish_emb = await ctx.send(embed=embed)

                        # Remove the buildings from user's infra.
                        cursor.execute('UPDATE infra SET oil_derrick = oil_derrick - ? WHERE name = ?',
                                       (amount, name))
                        conn.commit()

                        done_emb = discord.Embed(title="Demolish", type='rich',
                                                 description="Oil derricks have been demolished.",
                                                 color=discord.Color.red())
                        await demolish_emb.edit(embed=done_emb)
                    case "uraniummine" | "uranium":
                        embed = discord.Embed(title="Demolish", type='rich',
                                              description=f"{amount:,} Uranium Mines will be demolished.",
                                              color=discord.Color.red())
                        demolish_emb = await ctx.send(embed=embed)

                        # Remove the buildings from user's infra.
                        cursor.execute('UPDATE infra SET uranium_mine = uranium_mine - ? WHERE name = ?',
                                       (amount, name))
                        conn.commit()

                        done_emb = discord.Embed(title="Demolish", type='rich',
                                                 description="Uranium Mines have been demolished.",
                                                 color=discord.Color.red())
                        await demolish_emb.edit(embed=done_emb)
                    case "farm" | "food":
                        embed = discord.Embed(title="Demolish", type='rich',
                                              description=f"{amount:,} Farms will be demolished.",
                                              color=discord.Color.red())
                        demolish_emb = await ctx.send(embed=embed)

                        # Remove the buildings from user's infra.
                        cursor.execute('UPDATE infra SET farm = farm - ? WHERE name = ?',
                                       (amount, name))
                        conn.commit()

                        done_emb = discord.Embed(title="Demolish", type='rich',
                                                 description="Farms have been demolished.",
                                                 color=discord.Color.red())
                        await demolish_emb.edit(embed=done_emb)
                    case "aluminiumfactory" | "aluminium":
                        embed = discord.Embed(title="Demolish", type='rich',
                                              description=f"{amount:,} Aluminium Factories will be demolished.",
                                              color=discord.Color.red())
                        demolish_emb = await ctx.send(embed=embed)

                        # Remove the buildings from user's infra.
                        cursor.execute('UPDATE infra SET aluminium_factory = aluminium_factory - ? WHERE name = ?',
                                       (amount, name))
                        conn.commit()

                        done_emb = discord.Embed(title="Demolish", type='rich',
                                                 description="Aluminium Factories have been demolished.",
                                                 color=discord.Color.red())
                        await demolish_emb.edit(embed=done_emb)
                    case "steelfactory" | "steel":
                        embed = discord.Embed(title="Demolish", type='rich',
                                              description=f"{amount:,} Steel Factories will be demolished.",
                                              color=discord.Color.red())
                        demolish_emb = await ctx.send(embed=embed)

                        # Remove the buildings from user's infra.
                        cursor.execute('UPDATE infra SET steel_factory = steel_factory - ? WHERE name = ?',
                                       (amount, name))
                        conn.commit()

                        done_emb = discord.Embed(title="Demolish", type='rich',
                                                 description="Steel Factories have been demolished.",
                                                 color=discord.Color.red())
                        await demolish_emb.edit(embed=done_emb)
                    case "oilrefinery" | "gas":
                        embed = discord.Embed(title="Demolish", type='rich',
                                              description=f"{amount:,} Oil Refineries will be demolished.", color=discord.Color.red())
                        demolish_emb = await ctx.send(embed=embed)

                        # Remove the buildings from user's infra.
                        cursor.execute('UPDATE infra SET oil_refinery = oil_refinery - ? WHERE name = ?', (amount, name))
                        conn.commit()

                        done_emb = discord.Embed(title="Demolish", type='rich',
                                                 description="Oil Refineries have been demolished.", color=discord.Color.red())
                        await demolish_emb.edit(embed=done_emb)
                    case "munitionfactory" | "ammo" | "ammofactory":
                        embed = discord.Embed(title="Demolish", type='rich',
                                              description=f"{amount:,} Munition Factories will be demolished.",
                                              color=discord.Color.red())
                        demolish_emb = await ctx.send(embed=embed)

                        # Remove the buildings from user's infra.
                        cursor.execute('UPDATE infra SET ammo_factory = ammo_factory - ? WHERE name = ?',
                                       (amount, name))
                        conn.commit()

                        done_emb = discord.Embed(title="Demolish", type='rich',
                                                 description="Munition Factories have been demolished.",
                                                 color=discord.Color.red())
                        await demolish_emb.edit(embed=done_emb)
                    case "concretefactory" | "concrete":
                        embed = discord.Embed(title="Demolish", type='rich',
                                              description=f"{amount:,} Concrete Factories will be demolished.",
                                              color=discord.Color.red())
                        demolish_emb = await ctx.send(embed=embed)

                        # Remove the buildings from user's infra.
                        cursor.execute('UPDATE infra SET concrete_factory = concrete_factory - ? WHERE name = ?',
                                       (amount, name))
                        conn.commit()

                        done_emb = discord.Embed(title="Demolish", type='rich',
                                                 description="Concrete Factories have been demolished.",
                                                 color=discord.Color.red())
                        await demolish_emb.edit(embed=done_emb)
                    case "militaryfactory" | "mil":
                        embed = discord.Embed(title="Demolish", type='rich',
                                              description=f"{amount:,} Military Factories will be demolished.",
                                              color=discord.Color.red())
                        demolish_emb = await ctx.send(embed=embed)

                        # Remove the buildings from user's infra.
                        cursor.execute('UPDATE infra SET militaryfactory = militaryfactory - ? WHERE name = ?',
                                       (amount, name))
                        conn.commit()

                        done_emb = discord.Embed(title="Demolish", type='rich',
                                                 description="Military Factories have been demolished.",
                                                 color=discord.Color.red())
                        await demolish_emb.edit(embed=done_emb)
                    case _:
                        return
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