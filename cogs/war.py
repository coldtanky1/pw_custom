import discord
from discord.ext import commands
import asyncio
import globals
from schema import UserInfo, UserMil, Resources


new_line = '\n'


health_values = {
    "troop_hp": 28,
    "tank_hp": 2100,
    "plane_hp": 2000,
    "arty_hp": 13,
    "aa_hp": 85
}

damage_values = {
    "troop_dmg": 4,
    "tank_dmg": 100,
    "plane_dmg": 300,
    "arty_dmg": 3000,
    "aa_dmg": 1500
}

class War(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def war(self, ctx, user: discord.User = None):

        # Checks if target user was specified
        if user is None:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You cannot declare war on nothing!{new_line} Please specify a target.')
            await ctx.send(embed=embed)
            return

        attker_id = ctx.author.id
        target_id = user.id

        # fetch username
        attker_result = UserInfo.select().where(UserInfo.user_id == attker_id).first()

        # fetch target user name
        target_result = UserInfo.select().where(UserInfo.user_id == target_id).first()

        if attker_result and target_result:

            attker_name = attker_result.name
            target_name = target_result.name

            if target_id != attker_id:
                UserInfo.update(war_status="In War").where(UserInfo.user_id == target_id).execute()
                UserInfo.update(war_status="In War").where(UserInfo.user_id == attker_id).execute()

                # fetch attacker's resources
                attker_res_result = Resources.select().where(Resources.name == attker_name).first()

                # fetch attacker's mil stats
                attker_mil_result = UserMil.select().where(UserMil.name == attker_name).first()

                # fetch target user's resources
                target_res_result = Resources.select().where(Resources.name == target_name).first()

                # fetch target user's mil stats
                target_mil_result = UserMil.select().where(UserMil.name == target_name).first()

                if attker_res_result and target_res_result and target_mil_result and attker_mil_result:

                    # The attacker's mil stats
                    attker_troops = attker_mil_result.troops
                    attker_tanks = attker_mil_result.tanks
                    attker_planes = attker_mil_result.planes
                    attker_aa = attker_mil_result.anti_air
                    attker_artillery = attker_mil_result.artillery

                    # The target's mil stats
                    target_troops = target_mil_result.troops
                    target_tanks = target_mil_result.tanks
                    target_planes = target_mil_result.planes
                    target_aa = target_mil_result.anti_air
                    target_artillery = target_mil_result.artillery

                    target_user = await self.bot.fetch_user(target_id)
                    attker_user = await self.bot.fetch_user(attker_id)

            else:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description=f'You cannot declare war on yourself!.')
                await ctx.send(embed=embed)
                return
        else:
            if target_result:  # If the target (defender) does not have a nation.
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description=f'You do not have a nation.{new_line}'
                                                  f'To create one, type `$create`.')
                await ctx.send(embed=embed)
                return
            
            else:  # Else, if the attacker does not have a nation.
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description=f'<@{target_id}> does not have a nation.{new_line}'
                                                  f'To create one, type `$create`.')
                await ctx.send(embed=embed)
                return

async def setup(bot):
    await bot.add_cog(War(bot))
