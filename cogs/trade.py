import asyncio
import discord
from discord.ext import commands
from discord.utils import get

from schema import Resources, UserInfo, UserMil

new_line = '\n'


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

        if material == 'chikn wings':
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich')
            embed.set_image(url="https://cdn.discordapp.com/attachments/1167571324659580998/1319255714946089012/image.png?ex=67654c21&is=6763faa1&hm=d81548a0728180ed1916080c89bfd8dd913dac4cfbefc3a30a2d2a2f618d665f&")
            embed.set_footer(text="chikn wings.")
            await ctx.send(embed=embed)
            return

        # Access the user who invoked the command
        sender_id = ctx.author.id
        receiver_id = target_user.id
        material = material.lower()

        # fetch sender name
        sender_result = UserInfo.select().where(UserInfo.user_id == sender_id).first()

        # fetch target user name
        target_result = UserInfo.select().where(UserInfo.user_id == receiver_id).first()

        if sender_result:
            sender_name = sender_result.name

            if target_result:
                target_name = target_result.name

                # Check if the user is not the sender
                if receiver_id != sender_id:
                    # fetch sender's resources
                    sender_res_result = Resources.select(
                        Resources.wood, Resources.coal, Resources.iron,
                        Resources.lead, Resources.bauxite, Resources.oil,
                        Resources.uranium, Resources.food, Resources.steel,
                        Resources.gasoline, Resources.ammo, Resources.concrete).where(Resources.name == sender_name).tuples().first()

                    # fetch sender's mil stats
                    sender_mil_result = UserMil.select(
                        UserMil.troops, UserMil.tanks, UserMil.planes,
                        UserMil.artillery, UserMil.anti_air).where(UserMil.name == sender_name).tuples().first()

                    # fetch target user's resources
                    target_res_result = Resources.select(
                        Resources.wood, Resources.coal, Resources.iron,
                        Resources.lead, Resources.bauxite, Resources.oil,
                        Resources.uranium, Resources.food, Resources.steel,
                        Resources.gasoline, Resources.ammo, Resources.concrete).where(Resources.name == target_name).tuples().first()

                    # fetch target user's mil stats
                    target_mil_result = UserMil.select(
                        UserMil.troops, UserMil.tanks, UserMil.planes,
                        UserMil.artillery, UserMil.anti_air).where(UserMil.name == target_name).tuples().first()

                    print("Target mil: ", target_mil_result)
                    print("Sender mil: ", sender_mil_result)
                    print("Target res: ", target_res_result)
                    print("Sender res: ", sender_res_result)

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
                        case _:
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

                        field_name = mat_list[mat_number]
                        res_field = getattr(Resources, field_name)
                        # update sender's resources 
                        Resources.update({res_field: res_field - amount}).where(Resources.name == sender_name).execute()
                        # update target's resources
                        Resources.update({res_field: res_field + amount}).where(Resources.name == target_name).execute()

                    else:
                        print("mil: ", int(sender_mil_result[mat_number - 13]))
                        if amount > int(sender_mil_result[mat_number - 13]):
                            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                                  description=f"You can't trade more {mat_list[mat_number]} than you have!")
                            await ctx.send(embed=embed)
                            return

                        field_name = mat_list[mat_number]
                        mil_field = getattr(UserMil, field_name)
                        # update sender's mil
                        UserMil.update({mil_field: mil_field - amount}).where(UserMil.name == sender_name).execute()
                        # update target's mil
                        UserMil.update({mil_field: mil_field + amount}).where(UserMil.name == target_name).execute()

                    embed = discord.Embed(colour=0x5BF9A0, title="Success", type='rich',
                                          description=f'Trade completed!')
                    await ctx.send(embed=embed)
                # else:
                #     embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                #                           description=f"You can't trade with yourself!")
                #     embed.set_footer(text="Dummy")
                #     await ctx.send(embed=embed)
                #     return
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
