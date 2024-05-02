import sqlite3
import discord
from discord.ext import commands, tasks


new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = sqlite3.connect('player_info.db')
cursor = conn.cursor()


armor_values = {
    "troop_armor": 3,
    "tank_armor": 100,
    "plane_armor": 200,
    "arty_armor": 3,
    "aa_armor": 10
}

health_values = {
    "troop_hp": 25,
    "tank_hp": 2000,
    "plane_hp": 1800,
    "arty_hp": 10,
    "aa_hp": 75
}

body_damage_values = {
    "troop_bdmg": 4,
    "tank_bdmg": 100,
    "plane_bdmg": 300,
    "arty_bdmg": 3000,
    "aa_bdmg": 1500
}

armor_damage_values = {
    "troop_admg": 1,
    "tank_admg": 300,
    "plane_admg": 900,
    "arty_admg": 300,
    "aa_admg": 5000
}


class War(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def war(self, ctx, user: discord.User):
        attker_id = ctx.author.id
        target_id = user.id

        # fetch user nation_name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (attker_id,))
        attker_result = cursor.fetchone()

        # fetch target user nation_name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (target_id,))
        target_result = cursor.fetchone()

        if attker_result and target_result:
            user_id, nation_name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = attker_result
            user_id, nation_name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = target_result

            attker_name = attker_result[1]
            target_name = target_result[1]

            if target_id != attker_id:
                cursor.execute('UPDATE user_info SET war_status = ? WHERE user_id = ?', ("In War", attker_id))
                cursor.execute('UPDATE user_info SET war_status = ? WHERE user_id = ?', ("In War", target_id))

                # fetch attacker's resources
                cursor.execute(
                    'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                    (attker_name,))
                attker_res_result = cursor.fetchone()

                # fetch attacker's mil stats
                cursor.execute(
                    'SELECT * FROM user_mil WHERE name_nation = ?',
                    (attker_name,))
                attker_mil_result = cursor.fetchone()

                # fetch target user's resources
                cursor.execute(
                    'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                    (target_name,))
                target_res_result = cursor.fetchone()

                # fetch target user's mil stats
                cursor.execute(
                    'SELECT * FROM user_mil WHERE name_nation = ?',
                    (target_name,))
                target_mil_result = cursor.fetchone()

                if attker_res_result and target_res_result and target_mil_result and attker_mil_result:
                    name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = attker_res_result
                    name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = target_res_result
                    name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = attker_mil_result
                    name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = target_mil_result

                    # The attacker's mil stats
                    attker_troops = attker_mil_result[1]
                    attker_tanks = attker_mil_result[4]
                    attker_planes = attker_mil_result[2]
                    attker_aa = attker_mil_result[6]
                    attker_artillery = attker_mil_result[5]

                    # The target's mil stats
                    target_troops = target_mil_result[1]
                    target_tanks = target_mil_result[4]
                    target_planes = target_mil_result[2]
                    target_aa = target_mil_result[6]
                    target_artillery = target_mil_result[5]

                    target_user = await self.bot.fetch_user(target_id)
                    attker_user = await self.bot.fetch_user(attker_id)

                    # Alert the target user.
                    await target_user.send(f"<@{attker_id}> has declared war on you!")

                    ground_tactic = ""
                    air_tactic = ""
                    try:
                        await target_user.send("What ground tactic would you like to use? (reply with a number)\n"
                                            "**1.** Trench Warfare\n"
                                            "**2.** Creeping Barage\n"
                                            "**3.** Superior Firepower\n"
                                            "**4.** Massed Assault\n"
                                            "**5.** Elastic Defense\n"
                                            "**6.** Armored Spearhead\n")

                        def check(message):
                            return message.author == target_id

                        msg = await self.bot.wait_for('message', timeout=60, check=check)

                        if msg.content == 1:
                            await target_user.send("Selected **Trench Warfare** as ground tactic.")
                            ground_tactic = "Trench Warfare"

                        elif msg.content == 2:
                            await target_user.send("Selected **Creeping Barage** as ground tactic.")
                            ground_tactic = "Creeping Barage"

                        elif msg.content == 3:
                            await target_user.send("Selected **Superior Firepower** as ground tactic.")
                            ground_tactic = "Superior Firepower"

                        elif msg.content == 4:
                            await target_user.send("Selected **Massed Assault** as ground tactic.")
                            ground_tactic = "Massed Assault"

                        elif msg.content == 5:
                            await target_user.send("Selected **Elastic Defense** as ground tactic.")
                            ground_tactic = "Elastic Defense"

                        elif msg.content == 6:
                            await target_user.send("Selected **Armored Spearhead** as ground tactic.")
                            ground_tactic = "Armored Spearhead"

                        else:
                            pass
                            
                    except asyncio.TimeoutError:
                            return await ctx.send("You took too long to respond.")

                    try:
                        await target_user.send("What air tactic would you like to use? (reply with a number)\n"
                                            "**1.** Scramble"
                                            "**2.** Close Air Support"
                                            "**3.** Formation Flying"
                                            "**4.** Superior Firepower")

                        def check2(message):
                            return message.author == target_id

                        msg2 = await self.bot.wait_for('message', timeout=60, check=check2)

                        if msg2.content == 1:
                            await target_user.send("Selected **Scramble** as air tactic.")
                            air_tactic = "Scramble"

                        elif msg2.content == 2:
                            await target_user.send("Selected **Close Air Support** as air tactic.")
                            air_tactic = "Close Air Support"

                        elif msg2.content == 3:
                            await target_user.send("Selected **Formation Flying** as air tactic.")
                            air_tactic = "Formation Flying"

                        elif msg2.content == 4:
                            await target_user.send("Selected **Superior Firepower** as air tactic.")
                            air_tactic = "Superior Firepower"

                        else:
                            return

                    except asyncio.TimeoutError:
                        return await ctx.send("You took too long to respond.")

async def setup(bot):
    await bot.add_cog(War(bot))