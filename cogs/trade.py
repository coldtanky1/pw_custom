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


class Trade(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trade(self, ctx, target_user: discord.User = None, material: str = 'chikn wings', amount: int = 0):
        # Check if the target_user was specified
        if target_user is None:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f"You can't trade with the void! Please specify an user.")
            embed.set_footer(text="Dummy")
            await ctx.send(embed=embed)
            return

        # Access the user who invoked the command
        sender_id = ctx.author.id
        receiver_id = target_user.id
        material = material.lower()

        # fetch sender name
        cursor.execute('SELECT name FROM user_info WHERE user_id = ?', (sender_id,))
        sender_result = cursor.fetchone()

        # fetch target user name
        cursor.execute('SELECT name FROM user_info WHERE user_id = ?', (receiver_id,))
        target_result = cursor.fetchone()

        if sender_result:
            sender_name = sender_result[0]

            if target_result:
                target_name = target_result[0]

                # Check if the user is not the sender
                if receiver_id != sender_id:
                    # fetch sender's resources
                    cursor.execute(
                        'SELECT wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                        (sender_name,))
                    sender_res_result = cursor.fetchone()

                    # fetch sender's mil stats
                    cursor.execute(
                        'SELECT troops, planes, tanks, artillery, anti_air FROM user_mil WHERE name = ?',
                        (sender_name,))
                    sender_mil_result = cursor.fetchone()

                    # fetch target user's resources
                    cursor.execute(
                        'SELECT wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                        (target_name,))
                    target_res_result = cursor.fetchone()

                    # fetch target user's mil stats
                    cursor.execute(
                        'SELECT troops, planes, tanks, artillery, anti_air FROM user_mil WHERE name = ?',
                        (target_name,))
                    target_mil_result = cursor.fetchone()

                    mat_list = ["wood", "coal", "iron", "lead", "bauxite", "oil", "uranium", "food", "steel", "aluminium", "gasoline", "ammo", "concrete", "troops", "planes", "tanks", "artillery", "anti_air"]

                    if not (sender_res_result and target_res_result and target_mil_result and sender_mil_result):
                        embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                              description=f'Cannot find stats.')
                        await ctx.send(embed=embed)
                        return

                    # check what material was specified and give it the number of the location of the value within the lists
                    match material:
                        case "wood":
                            mat_number = 0
                        case "coal":
                            mat_number = 1
                        case "iron":
                            mat_number = 2
                        case "lead":
                            mat_number = 3
                        case "bauxite":
                            mat_number = 4
                        case "oil":
                            mat_number = 5
                        case "uranium":
                            mat_number = 6
                        case "food":
                            mat_number = 7
                        case "steel":
                            mat_number = 8
                        case "aluminium":
                            mat_number = 9
                        case "gasoline":
                            mat_number = 10
                        case "ammo":
                            mat_number = 11
                        case "concrete":
                            mat_number = 12
                        case "troops" | "troop":
                            mat_number = 13
                        case "planes" | "plane":
                            mat_number = 14
                        case "tanks" | "tank":
                            mat_number = 15
                        case "artillery":
                            mat_number = 16
                        case "anti_air":
                            mat_number = 17
                        case _default:
                            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                                  description=f"You can't trade air!{new_line}Please specify a material, product or military equipment type.")
                            await ctx.send(embed=embed)
                            return
                    if amount <= 0:
                        embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                              description=f"Amount must be a value that is greater than 0!")
                        await ctx.send(embed=embed)
                        return
                    if mat_number < 13:
                        if amount > int(sender_res_result[mat_number]):
                            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                                  description=f"You can't trade more {mat_list[mat_number]} than you have!")
                            await ctx.send(embed=embed)
                            return
                        sender_resource_query = '''UPDATE resources SET {0} = {0} - {1} WHERE name == "{2}"'''.format(mat_list[mat_number], amount, sender_name)
                        target_resource_query = '''UPDATE resources SET {0} = {0} + {1} WHERE name == "{2}"'''.format(mat_list[mat_number], amount, target_name)
                    else:
                        if amount > int(sender_mil_result[mat_number - 13]):
                            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                                  description=f"You can't trade more {mat_list[mat_number]} than you have!")
                            await ctx.send(embed=embed)
                            return
                        sender_resource_query = '''UPDATE user_mil SET {0} = {0} - {1} WHERE name == "{2}"'''.format(mat_list[mat_number], amount, sender_name)
                        target_resource_query = '''UPDATE user_mil SET {0} = {0} + {1} WHERE name == "{2}"'''.format(mat_list[mat_number], amount, target_name)
                    print(sender_resource_query)
                    print(target_resource_query)
                    cursor.execute(sender_resource_query)
                    cursor.execute(target_resource_query)
                    conn.commit()
                    embed = discord.Embed(colour=0x5BF9A0, title="Success", type='rich',
                                          description=f'Trade completed!')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                          description=f"You can't trade with yourself!")
                    embed.set_footer(text="Dummy")
                    await ctx.send(embed=embed)
                    return
            else:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description=f'@<{receiver_id}> does not have a nation, as such you cannot trade with them.')
                embed.set_footer(text="Ask them kindly to create one :3")
                await ctx.send(embed=embed)
                return
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)
            return

async def setup(bot):
    await bot.add_cog(Trade(bot))
