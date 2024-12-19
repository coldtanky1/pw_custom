import asyncio
import discord
from discord.ext import commands
from discord.ext.commands.hybrid import required_pos_arguments
import globals
from schema import *

new_line = '\n'

resources_prices = [
    ("Wood", 12, 8),
    ("Coal", 38, 28),
    ("Iron", 25, 18),
    ("Lead", 63, 48),
    ("Bauxite", 100, 78),
    ("Oil", 250, 198),
    ("Uranium", 1250, 998),
    ("Food", 25, 18),
    ("Steel", 1875, 1498),
    ("Aluminium", 1250, 998),
    ("Gasoline", 2125, 1698),
    ("Munitions", 1250, 998),
    ("Concrete", 1000, 798)
]

resource_list = ["Wood", "Coal", "Iron", "Lead", "Bauxite", "Oil", "Uranium", "Food", "Steel", "Aluminium", "Gasoline", "Ammo", "Concrete"]
resource_list_code = ["wood", "coal", "iron", "lead", "bauxite", "oil", "uranium", "food", "steel", "aluminium", "gasoline", "ammo", "concrete"]

class IM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    resources_prices = [
        ("Wood", 12, 8),
        ("Coal", 38, 28),
        ("Iron", 25, 18),
        ("Lead", 63, 48),
        ("Bauxite", 100, 78),
        ("Oil", 250, 198),
        ("Uranium", 1250, 998),
        ("Food", 25, 18),
        ("Steel", 1875, 1498),
        ("Aluminium", 1250, 998),
        ("Gasoline", 2125, 1698),
        ("Munitions", 1250, 998),
        ("Concrete", 1000, 798)
    ]

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def im(self, ctx):
        user_id = ctx.author.id

        # fetch username
        result = UserInfo.select(UserInfo.name).where(UserInfo.user_id == user_id).first()

        if result:
            name = result.name

            # fetch user's resources. NOTE: This isn't actually needed for anything it's merely just a check to see if the user
            # has stats.
            res_result = Resources.select().where(Resources.name == name).first()

            if res_result:

                embed = discord.Embed(title="International Market", type='rich',
                                      description="Displays the International Market", color=discord.Color.green())
                embed.add_field(name='Keys', value=f'🛒 - Buy Price{new_line}'
                                                   f'🚚 - Sell Price{new_line}', inline=False)
                embed.add_field(name="", value="", inline=False)
                embed.add_field(name="Mined Resources", value=f"Wood {new_line}"
                                                              f"🛒 12 🚚 8{new_line}"
                                                              f"Coal {new_line}"
                                                              f"🛒 38 🚚 28{new_line}"
                                                              f"Iron {new_line}"
                                                              f"🛒 25 🚚 18{new_line}"
                                                              f"Lead {new_line}"
                                                              f"🛒 63 🚚 48{new_line}"
                                                              f"Bauxite {new_line}"
                                                              f"🛒 100 🚚 78{new_line}"
                                                              f"Oil {new_line}"
                                                              f"🛒 250 🚚 198{new_line}"
                                                              f"Uranium{new_line}"
                                                              f"🛒 1250 🚚 998{new_line}"
                                                              f"Food {new_line}"
                                                              f"🛒 25 🚚 18{new_line}", inline=True)
                embed.add_field(name="Manufactured Resources", value=f"Steel {new_line}"
                                                                     f"🛒 1875 🚚 1498{new_line}"
                                                                     f"Aluminium{new_line}"
                                                                     f"🛒 1250 🚚 998{new_line}"
                                                                     f"Gasoline {new_line}"
                                                                     f"🛒 2125 🚚 1698{new_line}"
                                                                     f"Munitions{new_line}"
                                                                     f"🛒 1250 🚚 998{new_line}"
                                                                     f"Concrete{new_line}"
                                                                     f"🛒 1000 🚚 798{new_line}", inline=True)
                await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def order(self, ctx, material: str = '', amount: int = 0):

        # Checks if user specified a material
        if material == '':
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Please specify a material to order.')
            await ctx.send(embed=embed)
            return

        user_id = ctx.author.id
        material = material.lower()

        # fetch username
        result = UserInfo.select().where(UserInfo.user_id == user_id).first()

        if amount <= 0:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Please try a positive number.')
            await ctx.send(embed=embed)
            return

        if result:
            name = result.name

            # fetch user stats. NOTE: check note above.
            stats_result = UserStats.select().where(UserStats.name == name).first()

            if stats_result:
                balance = stats_result.balance

                match material:
                    case "wood":
                        res_id = 0
                    case "coal":
                        res_id = 1
                    case "iron":
                        res_id = 2
                    case "lead":
                        res_id = 3
                    case "bauxite":
                        res_id = 4
                    case "oil":
                        res_id = 5
                    case "uranium":
                        res_id = 6
                    case "food":
                        res_id = 7
                    case "steel":
                        res_id = 8
                    case "aluminium":
                        res_id = 9
                    case "gas" | "gasoline":
                        res_id = 10
                    case "ammo" | "munitions":
                        res_id = 11
                    case "concrete":
                        res_id = 12
                    case _:
                        embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                              description=f"Specified material doesn't exit.")
                        await ctx.send(embed=embed)
                        return
                price = round(resources_prices[res_id][1] * amount)
                embed = discord.Embed(title="Market Order", type='rich',
                                      description="Purchase resources from the market.", color=0x1E66F5)
                embed.add_field(name="Market Order",
                                value=f"Price of {resources_prices[res_id][0]}: {resources_prices[res_id][1]:,}{new_line}"
                                      f"Units of {resources_prices[res_id][0]}: {amount:,}{new_line}"
                                      f"**Total Price: {price:,}**", inline=False)
                if price > balance:
                    embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                          f"You __cannot__ afford this sale.", inline=True)
                    await ctx.send(embed=embed)
                    return
                else:
                    embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                          f"You __can__ afford this sale.{new_line}"
                                                          f"Type **CONFIRM** to complete this sale.{new_line}",
                                    inline=True)
                    await ctx.send(embed=embed)

                try:
                    def check(message):
                        return message.author == ctx.author and message.channel == ctx.channel and message.content in [
                            'CONFIRM']

                    response_message = await self.bot.wait_for('message', timeout=30, check=check)

                    if response_message.content == 'CONFIRM':
                        ordering = discord.Embed(colour=0xdd7878, title='Market Order', type='rich',
                                                 description='Ordering...')
                        order_msg = await ctx.send(embed=ordering)

                        # Update user's balance
                        UserStats.update(balance=UserStats.balance - price).where(UserStats.name == name).execute()

                        # Update user's resource
                        field_name = resource_list_code[res_id]
                        field = getattr(Resources, field_name)
                        Resources.update({field: field + amount}).where(
                            Resources.name == name).execute()

                        order_done = discord.Embed(title="Market Order", type='rich', description="Order fulfilled!",
                                                   color=0x5BF9A0)
                        await order_msg.edit(embed=order_done)
                    else:
                        await ctx.send("Aborting...")
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

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sell(self, ctx, material: str = '', amount: int = 0):

        # Checks if user specified a material
        if material == '':
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Please specify a material to sell.')
            await ctx.send(embed=embed)
            return

        user_id = ctx.author.id
        material = material.lower()

        # fetch username
        result = UserInfo.select().where(UserInfo.user_id == user_id).first()

        if amount <= 0:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Please try a positive number.')
            await ctx.send(embed=embed)
            return

        if result:
            name = result.name

            # fetch user's resources
            res_result = Resources.select(
                Resources.wood, Resources.coal, Resources.iron,
                Resources.lead, Resources.bauxite, Resources.oil,
                Resources.uranium, Resources.food, Resources.steel,
                Resources.aluminium, Resources.gasoline, Resources.ammo,
                Resources.concrete).where(Resources.name == name).tuples().first()

            # fetch user stats
            stats_result = UserStats.select().where(UserStats.name == name).first()

            if res_result and stats_result:

                match material:
                    case "wood":
                        res_id = 0
                    case "coal":
                        res_id = 1
                    case "iron":
                        res_id = 2
                    case "lead":
                        res_id = 3
                    case "bauxite":
                        res_id = 4
                    case "oil":
                        res_id = 5
                    case "uranium":
                        res_id = 6
                    case "food":
                        res_id = 7
                    case "steel":
                        res_id = 8
                    case "aluminium":
                        res_id = 9
                    case "gas" | "gasoline":
                        res_id = 10
                    case "ammo" | "munitions":
                        res_id = 11
                    case "concrete":
                        res_id = 12
                    case _:
                        embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                              description=f"Specified material doesn't exit.")
                        await ctx.send(embed=embed)
                        return
                price = round(resources_prices[res_id][2] * amount)
                embed = discord.Embed(title="Market Sell", type='rich',
                                      description="Purchase resources from the market.", color=discord.Color.blue())
                embed.add_field(name="Market Sell",
                                value=f"Sell Price of {resources_prices[res_id][0]} {price:,}{new_line}", inline=False)

                if amount > res_result[res_id]:
                    embed.add_field(name="Reserve",
                                    value=f"{resources_prices[res_id][0]}: {res_result[res_id]:,}{new_line}"
                                          f"You __cannot__ afford this sale.", inline=True)
                    await ctx.send(embed=embed)
                    return
                else:
                    embed.add_field(name="Reserve",
                                    value=f"{resources_prices[res_id][0]}: {res_result[res_id]:,}{new_line}"
                                          f"You __can__ afford this sale.{new_line}"
                                          f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                    await ctx.send(embed=embed)

                try:
                    def check(message):
                        return message.author == ctx.author and message.channel == ctx.channel and message.content in [
                            'CONFIRM']

                    response_message = await self.bot.wait_for('message', timeout=30, check=check)

                    if response_message.content == 'CONFIRM':
                        selling = discord.Embed(colour=0xdd7878, title='Market Sell', type='rich',
                                                description='Selling...')
                        sell_msg = await ctx.send(embed=selling)

                        # Update user's balance
                        UserStats.update(balance=UserStats.balance + price).where(UserStats.name == name).execute()

                        # Update user's resource
                        field_name = resource_list_code[res_id]
                        field = getattr(Resources, field_name)
                        Resources.update({field: field - amount}).where(
                            Resources.name == name).execute()

                        order_done = discord.Embed(title="Market Sell", type='rich', description="Sale fulfilled!",
                                                   color=0x5BF9A0)
                        await sell_msg.edit(embed=order_done)
                    else:
                        await ctx.send("Aborting...")
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
    await bot.add_cog(IM(bot))
