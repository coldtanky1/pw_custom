import asyncio
import discord
from discord.ext import commands
from discord.utils import get
from schema import init_db, UserInfo, UserStats, UserMil, Resources, Infra, UserCustom

new_line = '\n'


class Create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, ctx):
        user_id = ctx.author.id

        existing_record = UserInfo.select().where(UserInfo.user_id == user_id).first()

        # Check if the user already has an account
        if existing_record:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You already created a nation.')
            embed.set_footer(text="Dementia")
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(colour=0xFFF86E, title="Creating Nation", type='rich',
                              description="What is the name of your nation?"
                                          "Name cannot be longer than 25 characters.")
        emb = await ctx.send(embed=embed)

        # Checks if response is made by the same user and in the same channel
        def msgchk(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            nt_name = await self.bot.wait_for('message', check=msgchk, timeout=30.0)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long to respond.")
        nat_name = nt_name.content

        if len(nat_name) > 25:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Your nation name cannot be longer than 25 characters.')
            await emb.edit(embed=embed)
            return

        # Checks if name already exists in database
        name_exists = UserInfo.select().where(UserInfo.name == nat_name).exists()
        if name_exists:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'That name is already used.')
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title='Nation Successfully Created',
            description=f'This is the glorious start of the **{nat_name}**! '
                        f'{new_line}We wish you a successful journey in leading your people to greatness.',
            color=0x5BF9A0
        )
        await emb.edit(embed=embed)

        # add user to the database
        UserInfo.create(user_id=user_id, name=nat_name, turns_accumulated=1, gov_type='Democracy', tax_rate=0.25, conscription='Volunteer', freedom='Moderate Freedom', police_policy='Normal Police', fire_policy='Normal Firefighers', hospital_policy='Normal Healthcare', war_status="In Peace", happiness=50, corp_tax=0.15)

        print(f"Successfully added {user_id}({nat_name})")

        # add base stats to the user
        UserStats.create(name=nat_name, nation_score=0, gdp=0, adult=100000, balance=10000000)

        # add base mil stats to the user
        UserMil.create(name=nat_name, troops=10000, planes=0, weapon=0, tanks=0, artillery=0, anti_air=0, barracks=0, tank_factory=0, plane_factory=0, artillery_factory=0, anti_air_factory=0)

        # Add base resources to the user
        Resources.create(name=nat_name, wood=500, coal=300, iron=50, lead=50, bauxite=0, oil=50, uranium=0, food=10000, steel=50, aluminium=50, gasoline=100, ammo=1000, concrete=500)

        print(f"Successfully added stats to {user_id}({nat_name})")

        # Add base infra stats to the user
        Infra.create(name=nat_name, basic_house=12500, small_flat=1000, apt_complex=835, skyscraper=0, lumber_mill=10, coal_mine=10, iron_mine=10, lead_mine=10, bauxite_mine=10,
            oil_derrick=10, uranium_mine=0, farm=2500, aluminium_factory=0, steel_factory=0, oil_refinery=0, ammo_factory=0, concrete_factory=0, militaryfactory=0, corps=0, park=0, cinema=0, museum=0, concert_hall=0)

        print(f"Successfully added infra to {user_id}({nat_name})")

        UserCustom.create(name=nat_name, flag="")

        print(f"Successfully added custom to {user_id}({nat_name})")

async def setup(bot):
    await bot.add_cog(Create(bot))
