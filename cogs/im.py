import sqlite3
import asyncio
import discord
from discord.ext import commands

new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = sqlite3.connect('player_info.db')
cursor = conn.cursor()

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

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness, corp_tax = result

            # fetch user's resources
            cursor.execute(
                'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                (name,))
            res_result = cursor.fetchone()

            # fetch user stats
            cursor.execute('SELECT * FROM user_stats WHERE name = ?', (name,))
            stats_result = cursor.fetchone()

            if res_result and stats_result:
                name, nation_score, gdp, adult, balance = stats_result
                name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

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
                                                              f"🛒 25 🚚 18{new_line}"
                                                              f"**Manufactured Resources**{new_line}"
                                                              f"Steel {new_line}"
                                                              f"🛒 1875 🚚 1498{new_line}"
                                                              f"Aluminium{new_line}"
                                                              f"🛒 1250 🚚 998{new_line}"
                                                              f"Gasoline {new_line}"
                                                              f"🛒 2125 🚚 1698{new_line}"
                                                              f"Munitions{new_line}"
                                                              f"🛒 1250 🚚 998{new_line}"
                                                              f"Concrete{new_line}"
                                                              f"🛒 1000 🚚 798{new_line}", inline=False)
                await ctx.send(embed=embed)


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def order(self, ctx, material: str, amount: int):
        user_id = ctx.author.id
        material = material.lower()

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if amount <= 0:
            await ctx.send("Please try a positive number.")
            return

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness, corp_tax = result

            # fetch user's resources
            cursor.execute(
                'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                (name,))
            res_result = cursor.fetchone()

            # fetch user stats
            cursor.execute('SELECT * FROM user_stats WHERE name = ?', (name,))
            stats_result = cursor.fetchone()

            if res_result and stats_result:
                name, nation_score, gdp, adult, balance = stats_result
                name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                match material:
                    case "wood":
                        price = round(resources_prices[0][1] * amount)
                        embed = discord.Embed(title="Market Order", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Order", value=f"Price of Wood {price:,}{new_line}", inline=False)
                        if price > balance:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                ordering = discord.Embed(colour=0xdd7878, title='Market Order', type='rich',
                                                                    description='Ordering...')
                                order_msg = await ctx.send(embed=ordering)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance - ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET wood = wood + ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Order", type='rich', description="Order fulfilled!", color=discord.Color.green())
                                await order_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "coal":
                        price = round(resources_prices[1][1] * amount)
                        embed = discord.Embed(title="Market Order", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Order", value=f"Price of Coal {price}{new_line}", inline=False)
                        if price > balance:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                ordering = discord.Embed(colour=0xdd7878, title='Market Order', type='rich',
                                                                    description='Ordering...')
                                order_msg = await ctx.send(embed=ordering)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance - ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET coal = coal + ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Order", type='rich', description="Order fulfilled!", color=discord.Color.green())
                                await order_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "iron":
                        price = round(resources_prices[2][1] * amount)
                        embed = discord.Embed(title="Market Order", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Order", value=f"Price of Iron {price}{new_line}", inline=False)
                        if price > balance:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                ordering = discord.Embed(colour=0xdd7878, title='Market Order', type='rich',
                                                                    description='Ordering...')
                                order_msg = await ctx.send(embed=ordering)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance - ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET iron = iron + ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Order", type='rich', description="Order fulfilled!", color=discord.Color.green())
                                await order_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "lead":
                        price = round(resources_prices[3][1] * amount)
                        embed = discord.Embed(title="Market Order", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Order", value=f"Price of Lead {price}{new_line}", inline=False)
                        if price > balance:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                ordering = discord.Embed(colour=0xdd7878, title='Market Order', type='rich',
                                                                    description='Ordering...')
                                order_msg = await ctx.send(embed=ordering)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance - ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET lead = lead + ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Order", type='rich', description="Order fulfilled!", color=discord.Color.green())
                                await order_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "bauxite":
                        price = round(resources_prices[4][1] * amount)
                        embed = discord.Embed(title="Market Order", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Order", value=f"Price of Bauxite {price}{new_line}", inline=False)
                        if price > balance:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                ordering = discord.Embed(colour=0xdd7878, title='Market Order', type='rich',
                                                                    description='Ordering...')
                                order_msg = await ctx.send(embed=ordering)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance - ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET bauxite = bauxite + ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Order", type='rich', description="Order fulfilled!", color=discord.Color.green())
                                await order_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "oil":
                        price = round(resources_prices[5][1] * amount)
                        embed = discord.Embed(title="Market Order", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Order", value=f"Price of Oil {price}{new_line}", inline=False)
                        if price > balance:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                ordering = discord.Embed(colour=0xdd7878, title='Market Order', type='rich',
                                                                    description='Ordering...')
                                order_msg = await ctx.send(embed=ordering)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance - ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET oil = oil + ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Order", type='rich', description="Order fulfilled!", color=discord.Color.green())
                                await order_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "uranium":
                        price = round(resources_prices[6][1] * amount)
                        embed = discord.Embed(title="Market Order", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Order", value=f"Price of Uranium {price}{new_line}", inline=False)
                        if price > balance:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                ordering = discord.Embed(colour=0xdd7878, title='Market Order', type='rich',
                                                                    description='Ordering...')
                                order_msg = await ctx.send(embed=ordering)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance - ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET uranium = uranium + ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Order", type='rich', description="Order fulfilled!", color=discord.Color.green())
                                await order_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "food":
                        price = round(resources_prices[7][1] * amount)
                        embed = discord.Embed(title="Market Order", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Order", value=f"Price of Food {price}{new_line}", inline=False)
                        if price > balance:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                ordering = discord.Embed(colour=0xdd7878, title='Market Order', type='rich',
                                                                    description='Ordering...')
                                order_msg = await ctx.send(embed=ordering)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance - ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET food = food + ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Order", type='rich', description="Order fulfilled!", color=discord.Color.green())
                                await order_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "steel":
                        price = round(resources_prices[8][1] * amount)
                        embed = discord.Embed(title="Market Order", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Order", value=f"Price of Steel {price}{new_line}", inline=False)
                        if price > balance:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                ordering = discord.Embed(colour=0xdd7878, title='Market Order', type='rich',
                                                                    description='Ordering...')
                                order_msg = await ctx.send(embed=ordering)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance - ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET steel = steel + ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Order", type='rich', description="Order fulfilled!", color=discord.Color.green())
                                await order_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "aluminium":
                        price = round(resources_prices[9][1] * amount)
                        embed = discord.Embed(title="Market Order", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Order", value=f"Price of Aluminium {price}{new_line}", inline=False)
                        if price > balance:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                ordering = discord.Embed(colour=0xdd7878, title='Market Order', type='rich',
                                                                    description='Ordering...')
                                order_msg = await ctx.send(embed=ordering)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance - ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET aluminium = aluminium + ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Order", type='rich', description="Order fulfilled!", color=discord.Color.green())
                                await order_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "gas" | "gasoline":
                        price = round(resources_prices[10][1] * amount)
                        embed = discord.Embed(title="Market Order", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Order", value=f"Price of Gasoline {price}{new_line}", inline=False)
                        if price > balance:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                ordering = discord.Embed(colour=0xdd7878, title='Market Order', type='rich',
                                                                    description='Ordering...')
                                order_msg = await ctx.send(embed=ordering)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance - ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET gasoline = gasoline + ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Order", type='rich', description="Order fulfilled!", color=discord.Color.green())
                                await order_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "ammo" | "munitions":
                        price = round(resources_prices[11][1] * amount)
                        embed = discord.Embed(title="Market Order", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Order", value=f"Price of Munitions {price}{new_line}", inline=False)
                        if price > balance:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                ordering = discord.Embed(colour=0xdd7878, title='Market Order', type='rich',
                                                                    description='Ordering...')
                                order_msg = await ctx.send(embed=ordering)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance - ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET ammo = ammo + ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Order", type='rich', description="Order fulfilled!", color=discord.Color.green())
                                await order_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "concrete":
                        price = round(resources_prices[12][1] * amount)
                        embed = discord.Embed(title="Market Order", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Order", value=f"Price of Concrete {price}{new_line}", inline=False)
                        if price > balance:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Balance", value=f"Balance: {balance:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                ordering = discord.Embed(colour=0xdd7878, title='Market Order', type='rich',
                                                                    description='Ordering...')
                                order_msg = await ctx.send(embed=ordering)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance - ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET concrete = concrete + ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Order", type='rich', description="Order fulfilled!", color=discord.Color.green())
                                await order_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")
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

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sell(self, ctx, material: str, amount: int):
        user_id = ctx.author.id
        material = material.lower()

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if amount <= 0:
            await ctx.send("Please try a positive number.")
            return

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness, corp_tax = result

            # fetch user's resources
            cursor.execute(
                'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                (name,))
            res_result = cursor.fetchone()

            # fetch user stats
            cursor.execute('SELECT * FROM user_stats WHERE name = ?', (name,))
            stats_result = cursor.fetchone()

            if res_result and stats_result:
                name, nation_score, gdp, adult, balance = stats_result
                name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                match material:
                    case "wood":
                        price = round(resources_prices[0][2] * amount)
                        embed = discord.Embed(title="Market Sell", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Sell", value=f"Sell Price of Wood {price:,}{new_line}", inline=False)
                        if amount > wood:
                            embed.add_field(name="Reserve", value=f"Wood: {wood:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Reserve", value=f"Wood: {wood:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                selling = discord.Embed(colour=0xdd7878, title='Market Sell', type='rich',
                                                                    description='Selling...')
                                sell_msg = await ctx.send(embed=selling)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET wood = wood - ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Sell", type='rich',description="Sale fulfilled!", color=discord.Color.green())
                                await sell_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "coal":
                        price = round(resources_prices[1][2] * amount)
                        embed = discord.Embed(title="Market Sell", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Sell", value=f"Price of Coal {price:,}{new_line}", inline=False)
                        if amount > coal:
                            embed.add_field(name="Reserve", value=f"Coal: {coal:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Reserve", value=f"Coal: {coal:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                selling = discord.Embed(colour=0xdd7878, title='Market Sell', type='rich',
                                                                    description='Selling...')
                                sell_msg = await ctx.send(embed=selling)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET coal = coal - ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Sell", type='rich',description="Sale fulfilled!", color=discord.Color.green())
                                await sell_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "iron":
                        price = round(resources_prices[2][2] * amount)
                        embed = discord.Embed(title="Market Sell", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Sell", value=f"Price of Iron {price:,}{new_line}", inline=False)
                        if amount > iron:
                            embed.add_field(name="Reserve", value=f"Iron: {iron:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Reserve", value=f"Iron: {iron:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                selling = discord.Embed(colour=0xdd7878, title='Market Sell', type='rich',
                                                                    description='Selling...')
                                sell_msg = await ctx.send(embed=selling)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET iron = iron - ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Sell", type='rich',description="Sale fulfilled!", color=discord.Color.green())
                                await sell_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "lead":
                        price = round(resources_prices[3][2] * amount)
                        embed = discord.Embed(title="Market Sell", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Sell", value=f"Price of Lead {price:,}{new_line}", inline=False)
                        if amount > lead:
                            embed.add_field(name="Reserve", value=f"Lead: {lead:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Reserve", value=f"Lead: {lead:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                selling = discord.Embed(colour=0xdd7878, title='Market Sell', type='rich',
                                                                    description='Selling...')
                                sell_msg = await ctx.send(embed=selling)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET lead = lead - ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Sell", type='rich',description="Sale fulfilled!", color=discord.Color.green())
                                await sell_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "bauxite":
                        price = round(resources_prices[4][2] * amount)
                        embed = discord.Embed(title="Market Sell", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Sell", value=f"Price of Bauxite {price:,}{new_line}", inline=False)
                        if amount > bauxite:
                            embed.add_field(name="Reserve", value=f"Bauxite: {bauxite:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Reserve", value=f"Bauxite: {bauxite:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                selling = discord.Embed(colour=0xdd7878, title='Market Sell', type='rich',
                                                                    description='Selling...')
                                sell_msg = await ctx.send(embed=selling)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET bauxite = bauxite - ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Sell", type='rich',description="Sale fulfilled!", color=discord.Color.green())
                                await sell_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "oil":
                        price = round(resources_prices[5][2] * amount)
                        embed = discord.Embed(title="Market Sell", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Sell", value=f"Price of Oil {price:,}{new_line}", inline=False)
                        if amount > oil:
                            embed.add_field(name="Reserve", value=f"Oil: {oil:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Reserve", value=f"Oil: {oil:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                selling = discord.Embed(colour=0xdd7878, title='Market Sell', type='rich',
                                                                    description='Selling...')
                                sell_msg = await ctx.send(embed=selling)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET oil = oil - ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Sell", type='rich',description="Sale fulfilled!", color=discord.Color.green())
                                await sell_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "uranium":
                        price = round(resources_prices[6][2] * amount)
                        embed = discord.Embed(title="Market Sell", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Sell", value=f"Price of Uranium {price:,}{new_line}", inline=False)
                        if amount > uranium:
                            embed.add_field(name="Reserve", value=f"Uranium: {uranium:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Reserve", value=f"Uranium: {uranium:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                selling = discord.Embed(colour=0xdd7878, title='Market Sell', type='rich',
                                                                    description='Selling...')
                                sell_msg = await ctx.send(embed=selling)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET uranium = uranium - ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Sell", type='rich',description="Sale fulfilled!", color=discord.Color.green())
                                await sell_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "food":
                        price = round(resources_prices[7][2] * amount)
                        embed = discord.Embed(title="Market Sell", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Sell", value=f"Price of Food {price:,}{new_line}", inline=False)
                        if amount > food:
                            embed.add_field(name="Reserve", value=f"Food: {food:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Reserve", value=f"Food: {food:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                selling = discord.Embed(colour=0xdd7878, title='Market Sell', type='rich',
                                                                    description='Selling...')
                                sell_msg = await ctx.send(embed=selling)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET food = food - ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Sell", type='rich',description="Sale fulfilled!", color=discord.Color.green())
                                await sell_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "steel":
                        price = round(resources_prices[8][2] * amount)
                        embed = discord.Embed(title="Market Sell", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Sell", value=f"Price of Steel {price:,}{new_line}", inline=False)
                        if amount > steel:
                            embed.add_field(name="Reserve", value=f"Steel: {steel:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Reserve", value=f"Steel: {steel:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                selling = discord.Embed(colour=0xdd7878, title='Market Sell', type='rich',
                                                                    description='Selling...')
                                sell_msg = await ctx.send(embed=selling)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET steel = steel - ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Sell", type='rich',description="Sale fulfilled!", color=discord.Color.green())
                                await sell_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "aluminium":
                        price = round(resources_prices[9][2] * amount)
                        embed = discord.Embed(title="Market Sell", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Sell", value=f"Price of Aluminium {price:,}{new_line}", inline=False)
                        if amount > aluminium:
                            embed.add_field(name="Reserve", value=f"Aluminium: {aluminium:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Reserve", value=f"Aluminium: {aluminium:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                selling = discord.Embed(colour=0xdd7878, title='Market Sell', type='rich',
                                                                    description='Selling...')
                                sell_msg = await ctx.send(embed=selling)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET aluminium = aluminium - ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Sell", type='rich',description="Sale fulfilled!", color=discord.Color.green())
                                await sell_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "gas" | "gasoline":
                        price = round(resources_prices[10][2] * amount)
                        embed = discord.Embed(title="Market Sell", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Sell", value=f"Price of Gasoline {price:,}{new_line}", inline=False)
                        if amount > gasoline:
                            embed.add_field(name="Reserve", value=f"Gasoline: {gasoline:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Reserve", value=f"Gasoline: {gasoline:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                selling = discord.Embed(colour=0xdd7878, title='Market Sell', type='rich',
                                                                    description='Selling...')
                                sell_msg = await ctx.send(embed=selling)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET gasoline = gasoline - ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Sell", type='rich',description="Sale fulfilled!", color=discord.Color.green())
                                await sell_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "ammo" | "munitions":
                        price = round(resources_prices[11][2] * amount)
                        embed = discord.Embed(title="Market Sell", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Sell", value=f"Price of Munitions {price:,}{new_line}", inline=False)
                        if amount > ammo:
                            embed.add_field(name="Reserve", value=f"Ammo: {ammo:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Reserve", value=f"Ammo: {ammo:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                selling = discord.Embed(colour=0xdd7878, title='Market Sell', type='rich',
                                                                    description='Selling...')
                                sell_msg = await ctx.send(embed=selling)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET ammo = ammo - ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Sell", type='rich',description="Sale fulfilled!", color=discord.Color.green())
                                await sell_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    case "concrete":
                        price = round(resources_prices[12][2] * amount)
                        embed = discord.Embed(title="Market Sell", type='rich',
                                             description="Purchase resources from the market.", color=discord.Color.blue())
                        embed.add_field(name="Market Sell", value=f"Price of Concrete {price:,}{new_line}", inline=False)
                        if amount > concrete:
                            embed.add_field(name="Reserve", value=f"Concrete: {concrete:,}{new_line}"
                                                                  f"You __cannot__ afford this sale.", inline=True)
                            await ctx.send(embed=embed)
                            return
                        else:
                            embed.add_field(name="Reserve", value=f"Concrete: {concrete:,}{new_line}"
                                                                  f"You __can__ afford this sale.{new_line}"
                                                                  f"Type **CONFIRM** to complete this sale.{new_line}", inline=True)
                            await ctx.send(embed=embed)

                        try:
                            def check(message):
                                return message.author == ctx.author and message.channel == ctx.channel and message.content in ['CONFIRM']

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)

                            if response_message.content == 'CONFIRM':
                                selling = discord.Embed(colour=0xdd7878, title='Market Sell', type='rich',
                                                                    description='Selling...')
                                sell_msg = await ctx.send(embed=selling)
                                
                                # Update user's balance
                                cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (price, name))
                                conn.commit()

                                # Update user's resource
                                cursor.execute('UPDATE resources SET concrete = concrete - ? WHERE name = ?', (amount, name))
                                conn.commit()

                                order_done = discord.Embed(title="Market Sell", type='rich',description="Sale fulfilled!", color=discord.Color.green())
                                await sell_msg.edit(embed=order_done)
                            else:
                                await ctx.send("Aborting...")
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")
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
    await bot.add_cog(IM(bot))
