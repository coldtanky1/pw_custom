import sqlite3
import asyncio
import discord
from discord.ext import commands
from discord.utils import get

new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = sqlite3.connect('player_info.db')
cursor = conn.cursor()


class Politics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gov(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
            
        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            gov_emb = discord.Embed(title="Government Overview", type='rich',
                                    description=f'Displays an overview of {name}\'s government.', color=discord.Color.blue())
            gov_emb.add_field(name='Key: C = Current', value='', inline=False)
            gov_emb.add_field(name=f'🏦 C: {gov_type}', value=f'Government Selection: `$gov-ide`', inline=False)
            gov_emb.add_field(name=f'💵 C: {tax_rate}', value=f'Tax Rate Selection: `$gov-tax <amount>`', inline=False)
            gov_emb.add_field(name=f'💂 C: {conscription}', value=f'Conscription Selection: `$gov-con`', inline=False)
            gov_emb.add_field(name=f'🕊️ C: {freedom}', value=f'Freedom Selection: `$gov-fre`', inline=False)
            gov_emb.add_field(name=f'🚔 C: {police_policy}', value=f'Police Selection: `$gov-pol`', inline=False)
            gov_emb.add_field(name=f'🚒 C: {fire_policy}', value=f'Firefighter Selection: `$gov-fir`', inline=False)
            gov_emb.add_field(name=f'🏥 C: {hospital_policy}', value=f'Healthcare Selection: `$gov-hea`', inline=False)
            await ctx.send(embed=gov_emb)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='gov-ide')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gov_ide(self, ctx):
        user_id = ctx.author.id
        
        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            embed = discord.Embed(title="Government Ideology", type='rich',
                                description="Displays government ideologies.", color=discord.Color.blue())
            embed.add_field(name="🗳️ Democracy", value=f"No less than 300 tax.{new_line}"
                                                       f"+20% tax income.{new_line}"
                                                       f"+20% upkeep costs.{new_line}", inline=False)
            embed.add_field(name="👑 Monarchy", value=f"+10% tax income.{new_line}"
                                                      f"+10% upkeep costs.{new_line}",inline=False)
            embed.add_field(name="☭ Communism", value=f"2x production bonus.{new_line}"
                                                      f"-20% upkeep costs.{new_line}"
                                                      f"-50% tax income.{new_line}",inline=False)
            embed.add_field(name="🏴 Fascism", value=f"-10% tax income.{new_line}"
                                                      f"+50% upkeep costs.{new_line}"
                                                      f"2x cheaper soldiers.{new_line}",inline=False)
            embed.add_field(name="☭ Socialism", value=f"-40% tax income.{new_line}"
                                                      f"-10% upkeep costs.{new_line}"
                                                      f"2x less effect from losing a war.{new_line}",inline=False)
            embed.add_field(name="Ⓐ Anarchy", value=f"-100% tax income.{new_line}"
                                                      f"Literal chaos.{new_line}",inline=False)
            embed.add_field(name='Command Usage', value=f'`ide-X`{new_line}'
                                                        f"X = first 3 letters of the policy.", inline=False)
            await ctx.send(embed=embed)
        
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)


    @commands.command(name='ide-dem')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ide_dem(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if gov_type == "Democracy":
                await ctx.send("You already have Democracy as your ideology.")
                return

            cursor.execute('UPDATE user_info SET gov_type = ? WHERE user_id = ?', ("Democracy", user_id))
            conn.commit()

            embed = discord.Embed(title="Government Ideology", type='rich',
                                description="You have successfully changed your ideology to **Democracy**.", color=discord.Color.blue())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='ide-mon')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ide_mon(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if gov_type == "Monarchy":
                await ctx.send("You already have Monarchy as your ideology.")
                return

            cursor.execute('UPDATE user_info SET gov_type = ? WHERE user_id = ?', ("Monarchy", user_id))
            conn.commit()

            embed = discord.Embed(title="Government Ideology", type='rich',
                                description="You have successfully changed your ideology to **Monarchy**.", color=discord.Color.blue())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='ide-com')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ide_com(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if gov_type == "Communism":
                await ctx.send("You already have Communism as your ideology.")
                return

            cursor.execute('UPDATE user_info SET gov_type = ? WHERE user_id = ?', ("Communism", user_id))
            conn.commit()

            embed = discord.Embed(title="Government Ideology", type='rich',
                                description="You have successfully changed your ideology to **Communism**.", color=discord.Color.blue())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='ide-fas')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ide_fas(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if gov_type == "Fascism":
                await ctx.send("You already have Fascism as your ideology.")
                return

            cursor.execute('UPDATE user_info SET gov_type = ? WHERE user_id = ?', ("Fascism", user_id))
            conn.commit()

            embed = discord.Embed(title="Government Ideology", type='rich',
                                description="You have successfully changed your ideology to **Fascism**.", color=discord.Color.blue())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='ide-soc')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ide_soc(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if gov_type == "Socialism":
                await ctx.send("You already have Socialism as your ideology.")
                return

            cursor.execute('UPDATE user_info SET gov_type = ? WHERE user_id = ?', ("Socialism", user_id))
            conn.commit()

            embed = discord.Embed(title="Government Ideology", type='rich',
                                description="You have successfully changed your ideology to **Socialism**.", color=discord.Color.blue())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='ide-ana')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ide_ana(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if gov_type == "Anarchy":
                await ctx.send("You already have Anarchy as your ideology.")
                return

            cursor.execute('UPDATE user_info SET gov_type = ? WHERE user_id = ?', ("Anarchy", user_id))
            conn.commit()

            embed = discord.Embed(title="Government Ideology", type='rich',
                                description="You have successfully changed your ideology to **Anarchy**.", color=discord.Color.blue())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    
    @commands.command(name='gov-con')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gov_con(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            embed = discord.Embed(title="Conscription", type='rich',
                                description="Displays conscription laws.", color=discord.Color.red())
            embed.add_field(name="Volunteer", value=f"Normal Recruitable population.{new_line}", inline=False)
            embed.add_field(name="Conscription", value=f"2x Recruitable population.{new_line}"
                                                        f"-15 Happiness.{new_line}", inline=False)
            embed.add_field(name="Full Conscription", value=f"4x Recruitable population.{new_line}"
                                                             f"-40% Happiness.{new_line}", inline=False)
            embed.add_field(name='Command Usage', value=f'`con-X`{new_line}'
                                                        f"X = first 3 letters of the policy.", inline=False)
            await ctx.send(embed=embed)
        
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='con-vol')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def con_vol(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if conscription == "Volunteer":
                await ctx.send("You already have Volunteer as your conscription law.")
                return

            cursor.execute('UPDATE user_info SET conscription = ? WHERE user_id = ?', ("Volunteer", user_id))
            conn.commit()

            cursor.execute('UPDATE user_info SET happiness = happiness + 0 WHERE name = ?', (name,))
            conn.commit()

            embed = discord.Embed(title="Conscription", type='rich',
                                description="You have successfully set **Volunteer** as your conscription law.", color=discord.Color.red())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='con-con')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def con_con(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if conscription == "Conscription":
                await ctx.send("You already have Conscription as your conscription law.")
                return

            cursor.execute('UPDATE user_info SET conscription = ? WHERE user_id = ?', ("Conscription", user_id))
            conn.commit()

            cursor.execute('UPDATE user_info SET happiness = happiness - 15 WHERE name = ?', (name,))
            conn.commit()

            embed = discord.Embed(title="Conscription", type='rich',
                                description="You have successfully set **Conscription** as your conscription law.", color=discord.Color.red())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='con-ful')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def con_ful(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if conscription == "Full Conscription":
                await ctx.send("You already have Full Conscription as your conscription law.")
                return

            cursor.execute('UPDATE user_info SET conscription = ? WHERE user_id = ?', ("Full Conscription", user_id))
            conn.commit()

            cursor.execute('UPDATE user_info SET happiness = happiness - 40 WHERE name = ?', (name,))
            conn.commit()

            embed = discord.Embed(title="Conscription", type='rich',
                                description="You have successfully set **Full Conscription** as your conscription law.", color=discord.Color.red())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)


    @commands.command(name='gov-fre')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gov_fre(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            embed = discord.Embed(title="Freedom", type='rich',
                                description="Displays your freedom laws.", color=discord.Color.green())
            embed.add_field(name="Free Speech", value=f"+20 Happiness.{new_line}"
                                                      f"2x More events.{new_line}", inline=False)
            embed.add_field(name="Moderate Freedom", value=f"+10 Happiness.{new_line}"
                                                      f"+20% effects from losing a war.{new_line}", inline=False)
            embed.add_field(name="No Freedom", value=f"-20 Happiness.{new_line}"
                                                      f"-40% effects from losing a war.{new_line}", inline=False)
            embed.add_field(name='Command Usage', value=f'`fre-X`{new_line}'
                                                        f"X = first 3 letters of the policy.", inline=False)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='fre-fre')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fre_fre(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if freedom == "Free Speech":
                await ctx.send("You already have Free Speech as your freedom law.")
                return

            cursor.execute('UPDATE user_info SET freedom = ? WHERE user_id = ?', ("Free Speech", user_id))
            conn.commit()

            cursor.execute('UPDATE user_info SET happiness = happiness + 20 WHERE name = ?', (name,))
            conn.commit()

            embed = discord.Embed(title="Freedom", type='rich',
                                description="You have successfully set **Free Speech** as your freedom law.", color=discord.Color.red())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='fre-mod')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fre_mod(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if freedom == "Moderate Freedom":
                await ctx.send("You already have Moderate Freedom as your freedom law.")
                return

            cursor.execute('UPDATE user_info SET freedom = ? WHERE user_id = ?', ("Moderate Freedom", user_id))
            conn.commit()

            cursor.execute('UPDATE user_info SET happiness = happiness + 10 WHERE name = ?', (name,))
            conn.commit()

            embed = discord.Embed(title="Freedom", type='rich',
                                description="You have successfully set **Moderate Freedom** as your freedom law.", color=discord.Color.red())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='fre-no')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fre_no(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if freedom == "No Freedom":
                await ctx.send("You already have No Freedom as your freedom law.")
                return

            cursor.execute('UPDATE user_info SET freedom = ? WHERE user_id = ?', ("No Freedom", user_id))
            conn.commit()

            cursor.execute('UPDATE user_info SET happiness = happiness - 20 WHERE name = ?', (name,))
            conn.commit()

            embed = discord.Embed(title="Freedom", type='rich',
                                description="You have successfully set **No Freedom** as your freedom law.", color=discord.Color.red())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)


    @commands.command(name='gov-pol')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gov_pol(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            embed = discord.Embed(title="Police Policy", type='rich',
                                description="Displays your police policy.", color=discord.Color.dark_blue())
            embed.add_field(name="Chill Police", value=f"+15 Happiness{new_line}"
                                                       f"Riots are not dealt with.{new_line}", inline=False)
            embed.add_field(name="Normal Police", value=f"Normal state security.{new_line}"
                                                        f"1,000 Required Funding.{new_line}", inline=False)
            embed.add_field(name="Serious Police", value=f"-10 Happiness{new_line}"
                                                       f"Riots are dealth with.{new_line}"
                                                       f"7,000 Required Funding.{new_line}", inline=False)
            embed.add_field(name='Command Usage', value=f'`pol-X`{new_line}'
                                                        f"X = first 3 letters of the policy.", inline=False)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='pol-chi')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pol_chi(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if police_policy == "Chill Police":
                await ctx.send("You already have Chill Police as your police policy.")
                return

            cursor.execute('UPDATE user_info SET police_policy = ? WHERE user_id = ?', ("Chill Police", user_id))
            conn.commit()

            cursor.execute('UPDATE user_info SET happiness = happiness + 15 WHERE name = ?', (name,))
            conn.commit()

            embed = discord.Embed(title="Police Policy", type='rich',
                                description="You have successfully set **Chill Police** as your police policy.", color=discord.Color.dark_blue())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='pol-nor')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pol_nor(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if police_policy == "Normal Police":
                await ctx.send("You already have Normal Police as your police policy.")
                return

            cursor.execute('UPDATE user_info SET police_policy = ? WHERE user_id = ?', ("Normal Police", user_id))
            conn.commit()

            cursor.execute('UPDATE user_info SET happiness = happiness + 0 WHERE name = ?', (name,))
            conn.commit()

            embed = discord.Embed(title="Police Policy", type='rich',
                                description="You have successfully set **Normal Police** as your police policy.", color=discord.Color.dark_blue())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='pol-ser')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pol_ser(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if police_policy == "Serious Police":
                await ctx.send("You already have Serious Police as your police policy.")
                return

            cursor.execute('UPDATE user_info SET police_policy = ? WHERE user_id = ?', ("Serious Police", user_id))
            conn.commit()

            cursor.execute('UPDATE user_info SET happiness = happiness - 10 WHERE name = ?', (name,))
            conn.commit()

            embed = discord.Embed(title="Police Policy", type='rich',
                                description="You have successfully set **Serious Police** as your police policy.", color=discord.Color.dark_blue())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='gov-tax')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gov_tax(self, ctx, amount: int):
        user_id = ctx.author.id

        if amount <= 0:
            await ctx.send("Invalid amount, try a positive number.")
            return

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if gov_type == "Democracy":
                if amount < 300:
                    await ctx.send("You cannot set your tax lower than 300 as a Democracy.")
                    return

            embed = discord.Embed(title="Tax Rate", type='rich',
                                description="Set a custom tax rate.", color=discord.Color.blue())
            tax_emb = await ctx.send(embed=embed)

            cursor.execute('UPDATE user_info SET tax_rate = ? WHERE user_id = ?', (amount, user_id))
            conn.commit()

            done_emb = discord.Embed(title="Tax Rate", type='rich',
                                    description=f"Your tax rate has been set to {amount}!")
            await tax_emb.edit(embed=done_emb)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='gov-fir')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gov_fir(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            embed = discord.Embed(title="Firefighter Policy", type='rich',
                                description="Displays your firefighter policy.", color=discord.Color.dark_red())
            embed.add_field(name="Careless Firefighters", value=f"-20 Happiness{new_line}", inline=False)
            embed.add_field(name="Normal Firefighters", value=f"Normal fire control.{new_line}", inline=False)
            embed.add_field(name="Speedy Firefighters", value=f"+15 Happiness{new_line}"
                                                       f"7,000 Required Funding.{new_line}", inline=False)
            embed.add_field(name='Command Usage', value=f'`fir-X`{new_line}'
                                                        f"X = first 3 letters of the policy.", inline=False)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='fir-car')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fir_car(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if fire_policy == "Careless Firefighters":
                await ctx.send("You already have Careless Firefighters as your firefighter policy.")
                return

            cursor.execute('UPDATE user_info SET fire_policy = ? WHERE user_id = ?', ("Careless Firefighters", user_id))
            conn.commit()

            cursor.execute('UPDATE user_info SET happiness = happiness - 20 WHERE name = ?', (name,))
            conn.commit()

            embed = discord.Embed(title="Firefigther Policy", type='rich',
                                description="You have successfully set **Careless Firefighters** as your fire policy.", color=discord.Color.dark_blue())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='fir-nor')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fir_nor(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if fire_policy == "Normal Firefighters":
                await ctx.send("You already have Normal Firefighters as your firefighter policy.")
                return

            cursor.execute('UPDATE user_info SET fire_policy = ? WHERE user_id = ?', ("Normal Firefighters", user_id))
            conn.commit()

            cursor.execute('UPDATE user_info SET happiness = happiness + 0 WHERE name = ?', (name,))
            conn.commit()

            embed = discord.Embed(title="Firefigther Policy", type='rich',
                                description="You have successfully set **Normal Firefighters** as your fire policy.", color=discord.Color.dark_blue())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='fir-spe')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fir_spe(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if fire_policy == "Speedy Firefighters":
                await ctx.send("You already have Speedy Firefighters as your firefighter policy.")
                return

            cursor.execute('UPDATE user_info SET fire_policy = ? WHERE user_id = ?', ("Speedy Firefighters", user_id))
            conn.commit()

            cursor.execute('UPDATE user_info SET happiness = happiness + 20 WHERE name = ?', (name,))
            conn.commit()

            embed = discord.Embed(title="Firefigther Policy", type='rich',
                                description="You have successfully set **Speedy Firefighters** as your fire policy.", color=discord.Color.dark_blue())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='gov-hea')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gov_hea(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            embed = discord.Embed(title="Healthcare Policy", type='rich',
                                description="Displays your healtcare policy.", color=discord.Color.dark_red())
            embed.add_field(name="Enhanced Healthcare", value=f"+15 Happiness{new_line}"
                                                       f"18,000 Required funding.{new_line}", inline=False)
            embed.add_field(name="Normal Healthcare", value=f"1000 Required funding.{new_line}", inline=False)
            embed.add_field(name="Private Healthcare", value=f"-15 Happiness{new_line}"
                                                       f"5s00 Required Funding.{new_line}", inline=False)
            embed.add_field(name="No Healthcare", value=f"-40 Happiness{new_line}"
                                                       f"0 Required Funding.{new_line}", inline=False)
            embed.add_field(name='Command Usage', value=f'`hea-X`{new_line}'
                                                        f"X = first 3 letters of the policy.", inline=False)
            await ctx.send(embed=embed)
            
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='hea-enh')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hea_enh(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if hospital_policy == "Enhanced Healthcare":
                await ctx.send("You already have Enhanced Healthcare as your healthcare policy.")
                return

            cursor.execute('UPDATE user_info SET hospital_policy = ? WHERE user_id = ?', ("Enhanced Healthcare", user_id))
            conn.commit()

            cursor.execute('UPDATE user_info SET happiness = happiness + 20 WHERE name = ?', (name,))
            conn.commit()

            embed = discord.Embed(title="Healthcare Policy", type='rich',
                                description="You have successfully set **Enhanced Healthcare** as your healthcare policy.", color=discord.Color.dark_blue())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='hea-nor')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hea_nor(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if hospital_policy == "Normal Healthcare":
                await ctx.send("You already have Normal Healthcare as your healthcare policy.")
                return

            cursor.execute('UPDATE user_info SET hospital_policy = ? WHERE user_id = ?', ("Normal Healthcare", user_id))
            conn.commit()

            cursor.execute('UPDATE user_info SET happiness = happiness + 0 WHERE name = ?', (name,))
            conn.commit()

            embed = discord.Embed(title="Healthcare Policy", type='rich',
                                description="You have successfully set **Normal Healthcare** as your healthcare policy.", color=discord.Color.dark_blue())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='hea-no')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hea_no(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if hospital_policy == "No Healthcare":
                await ctx.send("You already have No Healthcare as your healthcare policy.")
                return

            cursor.execute('UPDATE user_info SET hospital_policy = ? WHERE user_id = ?', ("No Healthcare", user_id))
            conn.commit()

            cursor.execute('UPDATE user_info SET happiness = happiness - 40 WHERE name = ?', (name,))
            conn.commit()

            embed = discord.Embed(title="Healthcare Policy", type='rich',
                                description="You have successfully set **No Healthcare** as your healthcare policy.", color=discord.Color.dark_blue())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    @commands.command(name='hea-pri')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hea_pri(self, ctx):
        user_id = ctx.author.id

        # fetch user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            if hospital_policy == "Private Healthcare":
                await ctx.send("You already have Private Healthcare as your healthcare policy.")
                return

            cursor.execute('UPDATE user_info SET hospital_policy = ? WHERE user_id = ?', ("Private Healthcare", user_id))
            conn.commit()

            cursor.execute('UPDATE user_info SET happiness = happiness - 15 WHERE name = ?', (name,))
            conn.commit()

            embed = discord.Embed(title="Healthcare Policy", type='rich',
                                description="You have successfully set **Private Healthcare** as your healthcare policy.", color=discord.Color.dark_blue())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Politics(bot))