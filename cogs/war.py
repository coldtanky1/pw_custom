import sqlite3
import discord
from discord.ext import commands, tasks
import asyncio


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
                conn.commit()
                cursor.execute('UPDATE user_info SET war_status = ? WHERE user_id = ?', ("In War", target_id))
                conn.commit()

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

                    target_ground_tactic = ""
                    target_air_tactic = ""
                    attker_ground_tactic = ""
                    attker_air_tactic = ""

                    try:
                        await target_user.send("What ground tactic would you like to use? (reply with a number)\n"
                                            "**1.** Trench Warfare\n"
                                            "**2.** Creeping Barage\n"
                                            "**3.** Superior Firepower\n"
                                            "**4.** Massed Assault\n"
                                            "**5.** Elastic Defense\n"
                                            "**6.** Armored Spearhead\n")

                        def check(message):
                            return target_user != attker_user and message.author == target_user

                        msg = await self.bot.wait_for('message', timeout=60, check=check)

                        if msg.content == '1':
                            await target_user.send("Selected **Trench Warfare** as ground tactic.")
                            target_ground_tactic = "Trench Warfare"

                        elif msg.content == '2':
                            await target_user.send("Selected **Creeping Barage** as ground tactic.")
                            target_ground_tactic = "Creeping Barage"

                        elif msg.content == '3':
                            await target_user.send("Selected **Superior Firepower** as ground tactic.")
                            target_ground_tactic = "Superior Firepower"

                        elif msg.content == '4':
                            await target_user.send("Selected **Massed Assault** as ground tactic.")
                            target_ground_tactic = "Massed Assault"

                        elif msg.content == '5':
                            await target_user.send("Selected **Elastic Defense** as ground tactic.")
                            target_ground_tactic = "Elastic Defense"

                        elif msg.content == '6':
                            await target_user.send("Selected **Armored Spearhead** as ground tactic.")
                            target_ground_tactic = "Armored Spearhead"

                        else:
                            await target_user.send("Invalid")
                            pass
                            
                    except asyncio.TimeoutError:
                            return await target_user.send("You took too long to respond.")

                    await asyncio.sleep(10)
                    try:
                        await target_user.send("What air tactic would you like to use? (reply with a number)\n"
                                            "**1.** Scramble\n"
                                            "**2.** Close Air Support\n"
                                            "**3.** Formation Flying\n"
                                            "**4.** Superior Firepower\n")

                        def check2(message):
                            return target_user != attker_user and message.author == target_user

                        msg2 = await self.bot.wait_for('message', timeout=60, check=check2)

                        if msg2.content == '1':
                            await target_user.send("Selected **Scramble** as air tactic.")
                            target_air_tactic = "Scramble"

                        elif msg2.content == '2':
                            await target_user.send("Selected **Close Air Support** as air tactic.")
                            target_air_tactic = "Close Air Support"

                        elif msg2.content == '3':
                            await target_user.send("Selected **Formation Flying** as air tactic.")
                            target_air_tactic = "Formation Flying"

                        elif msg2.content == '4':
                            await target_user.send("Selected **Superior Firepower** as air tactic.")
                            target_air_tactic = "Superior Firepower"

                        else:
                            await target_user.send("Invalid")
                            pass

                    except asyncio.TimeoutError:
                        return await target_user.send("You took too long to respond.")
                    
                    await asyncio.sleep(10)
                    # Ask the attacker for tactic.
                    try:
                        await attker_user.send("What ground tactic would you like to use? (reply with a number)\n"
                                            "**1.** Trench Warfare\n"
                                            "**2.** Creeping Barage\n"
                                            "**3.** Superior Firepower\n"
                                            "**4.** Massed Assault\n"
                                            "**5.** Elastic Defense\n"
                                            "**6.** Armored Spearhead\n")

                        def check3(message):
                            return attker_user != target_user and message.author == attker_user

                        msg = await self.bot.wait_for('message', timeout=60, check=check3)

                        if msg.content == '1':
                            await attker_user.send("Selected **Trench Warfare** as ground tactic.")
                            attker_ground_tactic = "Trench Warfare"

                        elif msg.content == '2':
                            await attker_user.send("Selected **Creeping Barage** as ground tactic.")
                            attker_ground_tactic = "Creeping Barage"

                        elif msg.content == '3':
                            await attker_user.send("Selected **Superior Firepower** as ground tactic.")
                            attker_ground_tactic = "Superior Firepower"

                        elif msg.content == '4':
                            await attker_user.send("Selected **Massed Assault** as ground tactic.")
                            attker_ground_tactic = "Massed Assault"

                        elif msg.content == '5':
                            await attker_user.send("Selected **Elastic Defense** as ground tactic.")
                            attker_ground_tactic = "Elastic Defense"

                        elif msg.content == '6':
                            await attker_user.send("Selected **Armored Spearhead** as ground tactic.")
                            attker_ground_tactic = "Armored Spearhead"

                        else:
                            await attker_user.send("Invalid")
                            pass
                            
                    except asyncio.TimeoutError:
                            return await attker_user.send("You took too long to respond.")

                    await asyncio.sleep(10)
                    try:
                        await attker_user.send("What air tactic would you like to use? (reply with a number)\n"
                                            "**1.** Scramble\n"
                                            "**2.** Close Air Support\n"
                                            "**3.** Formation Flying\n"
                                            "**4.** Superior Firepower\n")

                        def check4(message):
                            return attker_user != target_user and message.author == attker_user

                        msg2 = await self.bot.wait_for('message', timeout=60, check=check4)

                        if msg2.content == '1':
                            await attker_user.send("Selected **Scramble** as air tactic.")
                            attker_air_tactic = "Scramble"

                        elif msg2.content == '2':
                            await attker_user.send("Selected **Close Air Support** as air tactic.")
                            attker_air_tactic = "Close Air Support"

                        elif msg2.content == '3':
                            await attker_user.send("Selected **Formation Flying** as air tactic.")
                            attker_air_tactic = "Formation Flying"

                        elif msg2.content == '4':
                            await attker_user.send("Selected **Superior Firepower** as air tactic.")
                            attker_air_tactic = "Superior Firepower"

                        else:
                            await attker_user.send("Invalid")
                            pass

                    except asyncio.TimeoutError:
                        return await attker_user.send("You took too long to respond.")

                    # The health and armor points
                    attker_troop_health = (attker_troops * health_values["troop_hp"])
                    attker_veh_health = (attker_tanks * health_values["tank_hp"]) + (attker_artillery * health_values["arty_hp"]) + (attker_aa * health_values["aa_hp"])
                    attker_troop_armor = (attker_troops * armor_values["troop_armor"])
                    attker_veh_armor = (attker_tanks * armor_values["tank_armor"]) + (attker_artillery * armor_values["arty_armor"]) + (attker_aa * armor_values["aa_armor"])

                    target_troop_health = (target_troops * health_values["troop_hp"])
                    target_veh_health = (target_tanks * health_values["tank_hp"]) + (target_artillery * health_values["arty_hp"]) + (target_aa * health_values["aa_hp"])
                    target_troop_armor = (target_troops * armor_values["troop_armor"])
                    target_veh_armor = (target_tanks * armor_values["tank_armor"]) + (target_artillery * armor_values["arty_armor"]) + (target_aa * armor_values["aa_armor"])

                    # The body and armor damage points
                    attker_troop_admg = (attker_troops * armor_damage_values["troop_admg"])
                    attker_veh_admg = (attker_tanks * armor_damage_values["tank_admg"]) + (attker_artillery * armor_damage_values["arty_admg"]) + (attker_aa * armor_damage_values["aa_admg"])
                    attker_troop_bdmg = (attker_troops * body_damage_values["troop_bdmg"])
                    attker_veh_bdmg = (attker_tanks * body_damage_values["tank_bdmg"]) + (attker_artillery * body_damage_values["arty_bdmg"]) + (attker_aa * body_damage_values["aa_bdmg"])

                    target_troop_admg = (target_troops * armor_damage_values["troop_admg"])
                    target_veh_admg = (target_tanks * armor_damage_values["tank_admg"]) + (target_artillery * armor_damage_values["arty_admg"]) + (target_aa * armor_damage_values["aa_admg"])
                    target_troop_bdmg = (target_troops * body_damage_values["troop_bdmg"])
                    target_veh_bdmg = (target_tanks * body_damage_values["tank_bdmg"]) + (target_artillery * body_damage_values["arty_bdmg"]) + (target_aa * body_damage_values["aa_bdmg"])

                    # Bonus health points from tactics
                    target_troop_hp_bonus = 0
                    target_veh_hp_bonus = 0

                    attker_troop_hp_bonus = 0
                    attker_veh_hp_bonus = 0

                    target_troop_armor_bonus = 0
                    target_veh_armor_bonus = 0

                    attker_troop_armor_bonus = 0
                    attker_veh_armor_bonus = 0
                    
                    # Bonus damage points from tactics
                    target_veh_bdmg_bonus = 0
                    target_troop_bdmg_bonus = 0
                    target_veh_admg_bonus = 0
                    target_troop_admg_bonus = 0

                    attker_troop_admg_bonus = 0
                    attker_veh_admg_bonus = 0
                    attker_troop_bdmg_bonus = 0
                    attker_veh_bdmg_bonus = 0

                    match target_ground_tactic:
                        case "Trench Warfare":
                            target_troop_hp_bonus += target_troop_health * 1.3
                            target_veh_hp_bonus += target_veh_health * 1.3

                            target_troop_armor_bonus += target_troop_armor * 1.5
                            target_veh_armor_bonus += target_veh_armor * 1.5

                            target_troop_admg_bonus += target_troop_admg * 1.05
                            target_veh_admg_bonus += target_veh_admg * 1.05

                            target_troop_bdmg_bonus += target_troop_bdmg * 1.05
                            target_veh_bdmg_bonus += target_veh_bdmg * 1.05

                        case "Creeping Barage":
                            target_troop_hp_bonus += target_troop_health * 0.95 # -1.05
                            target_veh_hp_bonus += 0

                            target_troop_armor_bonus += target_troop_armor * 0.95 # -1.05
                            target_veh_armor_bonus += 0

                            target_troop_admg_bonus += target_troop_admg * 1.05
                            target_veh_admg_bonus += target_veh_admg * 1.05

                            target_troop_bdmg_bonus += target_troop_bdmg * 1.15
                            target_veh_bdmg_bonus += target_veh_bdmg * 1.15

                        case "Superior Firepower":
                            target_troop_hp_bonus += target_troop_health * 1.01
                            target_veh_hp_bonus += target_veh_health * 1.05

                            target_troop_armor_bonus += target_troop_armor * 1.05
                            target_veh_armor_bonus += target_veh_armor * 1.05

                            target_troop_admg_bonus += target_troop_admg * 1.25
                            target_veh_admg_bonus += target_veh_admg * 1.5

                            target_troop_bdmg_bonus += target_troop_bdmg * 1.5
                            target_veh_bdmg_bonus += target_veh_bdmg * 1.25

                        case "Massed Assault":
                            target_troop_hp_bonus += target_troop_health * 0.95 # -1.05
                            target_veh_hp_bonus += target_veh_health * 0.95 # -1.05

                            target_troop_armor_bonus += target_troop_armor * 0.95 # -1.05
                            target_veh_armor_bonus += 0

                            target_troop_admg_bonus += target_troop_admg * 1.1
                            target_veh_admg_bonus += target_veh_admg * 1.1

                            target_troop_bdmg_bonus += target_troop_bdmg * 1.35
                            target_veh_bdmg_bonus += target_veh_bdmg * 1.15

                        case "Elastic Defense":
                            target_troop_hp_bonus += target_troop_health * 1.1
                            target_veh_hp_bonus += target_veh_health * 1.05

                            target_troop_armor_bonus += target_troop_armor * 1.05
                            target_veh_armor_bonus += target_veh_armor * 1.1

                            target_troop_admg_bonus += target_troop_admg * 1.05
                            target_veh_admg_bonus += target_veh_admg * 1.15

                            target_troop_bdmg_bonus += target_troop_bdmg * 1.05
                            target_veh_bdmg_bonus += target_veh_bdmg * 1.05

                        case "Armored Spearhead":
                            target_troop_hp_bonus += target_troop_health * 1.05
                            target_veh_hp_bonus += target_veh_health * 1.125

                            target_troop_armor_bonus += target_troop_armor * 1.05
                            target_veh_armor_bonus += target_veh_armor * 1.25

                            target_troop_admg_bonus += target_troop_admg * 1.05
                            target_veh_admg_bonus += target_veh_admg * 1.25

                            target_troop_bdmg_bonus += target_troop_bdmg * 1.05
                            target_veh_bdmg_bonus += target_veh_bdmg * 1.05

                        case _:
                            await ctx.send("An error occurred. Ping a dev.")
                            return

                    match attker_ground_tactic:
                        case "Trench Warfare":
                            attker_troop_hp_bonus += attker_troop_health * 1.3
                            attker_veh_hp_bonus += attker_veh_health * 1.3

                            attker_troop_armor_bonus += attker_troop_armor * 1.5
                            attker_veh_armor_bonus += attker_veh_armor * 1.5

                            attker_troop_admg_bonus += attker_troop_admg * 1.05
                            attker_veh_admg_bonus += attker_veh_admg * 1.05

                            attker_troop_bdmg_bonus += attker_troop_bdmg * 1.05
                            attker_veh_bdmg_bonus += attker_veh_bdmg * 1.05

                        case "Creeping Barage":
                            attker_troop_hp_bonus += attker_troop_health * 0.95 # -1.05
                            attker_veh_hp_bonus += 0

                            attker_troop_armor_bonus += attker_troop_armor * 0.95 # -1.05
                            attker_veh_armor_bonus += 0

                            attker_troop_admg_bonus += attker_troop_admg * 1.05
                            attker_veh_admg_bonus += attker_veh_admg * 1.05

                            attker_troop_bdmg_bonus += attker_troop_bdmg * 1.15
                            attker_veh_bdmg_bonus += attker_veh_bdmg * 1.15

                        case "Superior Firepower":
                            attker_troop_hp_bonus += attker_troop_health * 1.01
                            attker_veh_hp_bonus += attker_veh_health * 1.05

                            attker_troop_armor_bonus += attker_troop_armor * 1.05
                            attker_veh_armor_bonus += attker_veh_armor * 1.05

                            attker_troop_admg_bonus += attker_troop_admg * 1.25
                            attker_veh_admg_bonus += attker_veh_admg * 1.5

                            attker_troop_bdmg_bonus += attker_troop_bdmg * 1.5
                            attker_veh_bdmg_bonus += attker_veh_bdmg * 1.25

                        case "Massed Assault":
                            attker_troop_hp_bonus += attker_troop_health * 0.95 # -1.05
                            attker_veh_hp_bonus += attker_veh_health * 0.95 # -1.05

                            attker_troop_armor_bonus += attker_troop_armor * 0.95 # -1.05
                            attker_veh_armor_bonus += 0

                            attker_troop_admg_bonus += attker_troop_admg * 1.1
                            attker_veh_admg_bonus += attker_veh_admg * 1.1

                            attker_troop_bdmg_bonus += attker_troop_bdmg * 1.35
                            attker_veh_bdmg_bonus += attker_veh_bdmg * 1.15

                        case "Elastic Defense":
                            attker_troop_hp_bonus += attker_troop_health * 1.1
                            attker_veh_hp_bonus += attker_veh_health * 1.05

                            attker_troop_armor_bonus += attker_troop_armor * 1.05
                            attker_veh_armor_bonus += attker_veh_armor * 1.1

                            attker_troop_admg_bonus += attker_troop_admg * 1.05
                            attker_veh_admg_bonus += attker_veh_admg * 1.15

                            attker_troop_bdmg_bonus += attker_troop_bdmg * 1.05
                            attker_veh_bdmg_bonus += attker_veh_bdmg * 1.05

                        case "Armored Spearhead":
                            attker_troop_hp_bonus += attker_troop_health * 1.05
                            attker_veh_hp_bonus += attker_veh_health * 1.125

                            attker_troop_armor_bonus += attker_troop_armor * 1.05
                            attker_veh_armor_bonus += attker_veh_armor * 1.25

                            attker_troop_admg_bonus += attker_troop_admg * 1.05
                            attker_veh_admg_bonus += attker_veh_admg * 1.25

                            attker_troop_bdmg_bonus += attker_troop_bdmg * 1.05
                            attker_veh_bdmg_bonus += attker_veh_bdmg * 1.05

                        case _:
                            await ctx.send("An error occurred. Ping a dev.")
                            return
                        
                    # Defender's final stats
                    targetf_troop_hp = target_troop_health + target_troop_hp_bonus
                    targetf_veh_hp = target_veh_health + target_veh_hp_bonus
                    target_total_hp = targetf_troop_hp + targetf_veh_hp

                    targetf_troop_armor = target_troop_armor + target_troop_armor_bonus
                    targetf_veh_armor = target_veh_armor + target_veh_armor_bonus
                    target_total_armor = targetf_troop_armor + targetf_veh_armor

                    targetf_troop_bdmg = target_troop_bdmg + target_troop_bdmg_bonus
                    targetf_veh_bdmg = target_veh_bdmg + target_veh_bdmg_bonus

                    targetf_troop_admg = target_troop_admg + target_troop_admg_bonus
                    targetf_veh_admg = target_veh_admg + target_veh_admg_bonus

                    # Attacker's final stats
                    attkerf_troop_hp = attker_troop_health + attker_troop_hp_bonus
                    attkerf_veh_hp = attker_veh_health + attker_veh_hp_bonus
                    attker_total_hp = attkerf_troop_hp + attkerf_veh_hp

                    attkerf_troop_armor = attker_troop_armor + attker_troop_armor_bonus
                    attkerf_veh_armor = attker_veh_armor + attker_veh_armor_bonus
                    attker_total_armor = attkerf_troop_armor + attkerf_veh_armor

                    attkerf_troop_bdmg = attker_troop_bdmg + attker_troop_bdmg_bonus
                    attkerf_veh_bdmg = attker_veh_bdmg + attker_veh_bdmg_bonus

                    attkerf_troop_admg = attker_troop_admg + attker_troop_admg_bonus
                    attkerf_veh_admg = attker_veh_admg + attker_veh_admg_bonus

                    war_ch = self.bot.get_channel(921494405909717092)

                    init_emb = discord.Embed(title=f"{attker_name} VS {target_name}. | Ground Battle.", 
                                                description="The battle will start in 5 minutes.\n"
                                                        "Get ready!", color=discord.Color.red())
                    await war_ch.send(embed=init_emb)

                    await asyncio.sleep(10)

                    start_emb = discord.Embed(title=f"{attker_name} VS {target_name} | Ground Battle.",
                                                      description=f"The battle between {attker_name} and {target_name} has started.",
                                                      color=discord.Color.red())
                    start_emb.add_field(name="Attacker Stats:\n", value=f"Troops: {attker_troops:,}\n"
                                                                        f"Tanks: {attker_tanks:,}\n"
                                                                        f"Artillery: {attker_artillery:,}\n"
                                                                        f"Anti-Air: {attker_aa:,}\n"
                                                                        f"HP: {attker_total_hp:,}\n"
                                                                        f"Armor: {attker_total_armor:,}\n"
                                                                        f"\n"
                                                                        f"Body DMG: {attkerf_troop_bdmg+attkerf_veh_bdmg:,}\n"
                                                                        f"Armor DMG: {attkerf_troop_admg+attkerf_veh_admg:,}\n", inline=True)
                    start_emb.add_field(name="Defender Stats:\n", value=f"Troops: {target_troops:,}\n"
                                                                        f"Tanks: {target_tanks:,}\n"
                                                                        f"Artillery: {target_artillery:,}\n"
                                                                        f"Anti-Air: {target_aa:,}\n"
                                                                        f"HP: {target_total_hp:,}\n"
                                                                        f"Armor: {target_total_armor:,}\n"
                                                                        f"\n"
                                                                        f"Body DMG: {targetf_troop_bdmg+targetf_veh_bdmg:,}\n"
                                                                        f"Armor DMG: {targetf_troop_admg+targetf_veh_admg:,}\n", inline=True)
                    await war_ch.send(embed=start_emb)

                    await asyncio.sleep(10)

                    def ensure_no_negative(value):
                        return max(value, 0)

                    # The battle. It will keep looping until either the attacker or the defender have 0 or less health.
                    while (target_total_hp > 0) and (attker_total_hp > 0):

                        # The battle stuff
                        if ((target_total_armor > 0) and (attker_total_armor > 0)):

                            if targetf_veh_admg > attkerf_veh_admg:
                                
                                # New defender armor.
                                targetf_troop_armor = ensure_no_negative(targetf_troop_armor - (attkerf_troop_admg))
                                targetf_veh_armor = ensure_no_negative(targetf_veh_armor - (attkerf_troop_admg))

                                target_total_armor -= target_troop_armor + target_veh_armor

                                # New attacker armor.
                                attkerf_troop_armor = ensure_no_negative(attkerf_troop_armor - (targetf_troop_admg + targetf_veh_admg))
                                attkerf_veh_armor = ensure_no_negative(attkerf_veh_armor - (targetf_troop_admg + targetf_veh_admg))

                                attker_total_armor -= attker_troop_armor + attker_veh_armor

                                await asyncio.sleep(3)
                                new_emb = discord.Embed(title=f"{attker_name} VS {target_name} | Ground Battle.",
                                                        description=f"The battle between {attker_name} and {target_name}.",
                                                        color=discord.Color.red())
                                new_emb.add_field(name="Attacker Stats:\n", value=f"Troops: {attker_troops:,}\n"
                                                                                    f"Tanks: {attker_tanks:,}\n"
                                                                                    f"Artillery: {attker_artillery:,}\n"
                                                                                    f"Anti-Air: {attker_aa:,}\n"
                                                                                    f"HP: {attker_total_hp:,}\n"
                                                                                    f"Armor: {attker_total_armor:,}\n"
                                                                                    f"\n"
                                                                                    f"Body DMG: {attkerf_troop_bdmg+attkerf_veh_bdmg:,}\n"
                                                                                    f"Armor DMG: {attkerf_troop_admg+attkerf_veh_admg:,}\n", inline=True)
                                new_emb.add_field(name="Defender Stats:\n", value=f"Troops: {target_troops:,}\n"
                                                                                    f"Tanks: {target_tanks:,}\n"
                                                                                    f"Artillery: {target_artillery:,}\n"
                                                                                    f"Anti-Air: {target_aa:,}\n"
                                                                                    f"HP: {target_total_hp:,}\n"
                                                                                    f"Armor: {target_total_armor:,}\n"
                                                                                    f"\n"
                                                                                    f"Body DMG: {targetf_troop_bdmg+targetf_veh_bdmg:,}\n"
                                                                                    f"Armor DMG: {targetf_troop_admg+targetf_veh_admg:,}\n", inline=True)
                                new_emb.set_footer(text="This is the battle for armor.")
                                await war_ch.send(embed=new_emb)

                            else:
                                # New defender armor.
                                targetf_troop_armor = ensure_no_negative(targetf_troop_armor - (attkerf_troop_admg + attkerf_veh_admg))
                                targetf_veh_armor = ensure_no_negative(targetf_veh_armor - (attkerf_troop_admg + attkerf_veh_admg))

                                target_total_armor -= target_troop_armor + target_veh_armor

                                # New attacker armor.
                                attkerf_troop_armor = ensure_no_negative(attkerf_troop_armor - (targetf_troop_admg))
                                attkerf_veh_armor = ensure_no_negative(attkerf_veh_armor - (targetf_troop_admg))

                                attker_total_armor -= attker_troop_armor + attker_veh_armor

                                await asyncio.sleep(3)
                                new_emb = discord.Embed(title=f"{attker_name} VS {target_name} | Ground Battle.",
                                                        description=f"The battle between {attker_name} and {target_name}.",
                                                        color=discord.Color.red())
                                new_emb.add_field(name="Attacker Stats:\n", value=f"Troops: {attker_troops:,}\n"
                                                                                    f"Tanks: {attker_tanks:,}\n"
                                                                                    f"Artillery: {attker_artillery:,}\n"
                                                                                    f"Anti-Air: {attker_aa:,}\n"
                                                                                    f"HP: {attker_total_hp:,}\n"
                                                                                    f"Armor: {attker_total_armor:,}\n"
                                                                                    f"\n"
                                                                                    f"Body DMG: {attkerf_troop_bdmg+attkerf_veh_bdmg:,}\n"
                                                                                    f"Armor DMG: {attkerf_troop_admg+attkerf_veh_admg:,}\n", inline=True)
                                new_emb.add_field(name="Defender Stats:\n", value=f"Troops: {target_troops:,}\n"
                                                                                    f"Tanks: {target_tanks:,}\n"
                                                                                    f"Artillery: {target_artillery:,}\n"
                                                                                    f"Anti-Air: {target_aa:,}\n"
                                                                                    f"HP: {target_total_hp:,}\n"
                                                                                    f"Armor: {target_total_armor:,}\n"
                                                                                    f"\n"
                                                                                    f"Body DMG: {targetf_troop_bdmg+targetf_veh_bdmg:,}\n"
                                                                                    f"Armor DMG: {targetf_troop_admg+targetf_veh_admg:,}\n", inline=True)
                                new_emb.set_footer(text="This is the battle for armor.")
                                await war_ch.send(embed=new_emb)

                        else: # If one of the users no longer has armor.
                            
                            # If the defender's armor is less or equal to 0, while attacker's armor is more than 0
                            if target_total_armor < 0 and attker_total_armor > 0:

                                if targetf_veh_bdmg > attkerf_veh_bdmg:

                                    # New target hp.
                                    targetf_troop_hp = ensure_no_negative(targetf_troop_hp - (attkerf_troop_bdmg))
                                    targetf_veh_hp = ensure_no_negative(targetf_veh_hp - (attkerf_troop_bdmg))

                                    target_total_hp -= (targetf_troop_hp + targetf_veh_hp)

                                    target_troops -= round(targetf_troop_hp//25)
                                    target_tanks -= round(targetf_veh_hp//2000)
                                    target_artillery -= round(targetf_veh_hp//10)
                                    target_aa -= round(targetf_veh_hp//75)

                                    # New attacker armor.
                                    attkerf_troop_armor = ensure_no_negative(attkerf_troop_armor - (targetf_troop_admg + targetf_veh_admg))
                                    attkerf_veh_armor = ensure_no_negative(attkerf_veh_armor - (targetf_troop_admg + targetf_veh_admg))

                                    attker_total_armor -= attker_troop_armor + attker_veh_armor

                                    newhp_emb = discord.Embed(title=f"{attker_name} VS {target_name} | Ground Battle.",
                                                            description=f"The battle between {attker_name} and {target_name}.",
                                                            color=discord.Color.red())
                                    newhp_emb.add_field(name="Attacker Stats:\n", value=f"Troops: {attker_troops:,}\n"
                                                                                        f"Tanks: {attker_tanks:,}\n"
                                                                                        f"Artillery: {attker_artillery:,}\n"
                                                                                        f"Anti-Air: {attker_aa:,}\n"
                                                                                        f"HP: {attker_total_hp:,}\n"
                                                                                        f"Armor: {attker_total_armor}\n"
                                                                                        f"\n"
                                                                                        f"Body DMG: {attkerf_troop_bdmg+attkerf_veh_bdmg:,}\n"
                                                                                        f"Armor DMG: {attkerf_troop_admg+attkerf_veh_admg:,}\n", inline=True)
                                    
                                    newhp_emb.add_field(name="Defender Stats:\n", value=f"Troops: {target_troops:,}\n"
                                                                                        f"Tanks: {target_tanks:,}\n"
                                                                                        f"Artillery: {target_artillery:,}\n"
                                                                                        f"Anti-Air: {target_aa:,}\n"
                                                                                        f"HP: {target_total_hp:,}\n"
                                                                                        f"Armor: 0\n"
                                                                                        f"\n"
                                                                                        f"Body DMG: {targetf_troop_bdmg+targetf_veh_bdmg:,}\n"
                                                                                        f"Armor DMG: {targetf_troop_admg+targetf_veh_admg:,}\n", inline=True)
                                    await war_ch.send(embed=newhp_emb)

                                else:
                                    # New target hp.
                                    targetf_troop_hp = ensure_no_negative(targetf_troop_hp - (attkerf_troop_bdmg + attkerf_veh_bdmg))
                                    targetf_veh_hp = ensure_no_negative(targetf_veh_hp - (attkerf_troop_bdmg + attkerf_veh_bdmg))

                                    target_total_hp -= targetf_troop_hp + targetf_veh_hp

                                    target_troops -= round(targetf_troop_hp//25)
                                    target_tanks -= round(targetf_veh_hp//2000)
                                    target_artillery -= round(targetf_veh_hp//10)
                                    target_aa -= round(targetf_veh_hp//75)

                                    # New attacker armor.
                                    attkerf_troop_armor = ensure_no_negative(attkerf_troop_armor - (targetf_troop_admg))
                                    attkerf_veh_armor = ensure_no_negative(attkerf_veh_armor - (targetf_troop_admg))

                                    attker_total_armor -= attker_troop_armor + attker_veh_armor

                                    newhp_emb = discord.Embed(title=f"{attker_name} VS {target_name} | Ground Battle.",
                                                            description=f"The battle between {attker_name} and {target_name}.",
                                                            color=discord.Color.red())
                                    newhp_emb.add_field(name="Attacker Stats:\n", value=f"Troops: {attker_troops:,}\n"
                                                                                        f"Tanks: {attker_tanks:,}\n"
                                                                                        f"Artillery: {attker_artillery:,}\n"
                                                                                        f"Anti-Air: {attker_aa:,}\n"
                                                                                        f"HP: {attker_total_hp:,}\n"
                                                                                        f"Armor: {attker_total_armor}\n"
                                                                                        f"\n"
                                                                                        f"Body DMG: {attkerf_troop_bdmg+attkerf_veh_bdmg:,}\n"
                                                                                        f"Armor DMG: {attkerf_troop_admg+attkerf_veh_admg:,}\n", inline=True)
                                    newhp_emb.add_field(name="Defender Stats:\n", value=f"Troops: {target_troops:,}\n"
                                                                                        f"Tanks: {target_tanks:,}\n"
                                                                                        f"Artillery: {target_artillery:,}\n"
                                                                                        f"Anti-Air: {target_aa:,}\n"
                                                                                        f"HP: {target_total_hp:,}\n"
                                                                                        f"Armor: 0\n"
                                                                                        f"\n"
                                                                                        f"Body DMG: {targetf_troop_bdmg+targetf_veh_bdmg:,}\n"
                                                                                        f"Armor DMG: {targetf_troop_admg+targetf_veh_admg:,}\n", inline=True)
                                    await war_ch.send(embed=newhp_emb)

                            # If the defender's armor is more than 0, while attacker's armor is less or equal to 0
                            elif target_total_armor > 0 and attker_total_armor < 0:
                                if targetf_veh_bdmg > attkerf_veh_bdmg:

                                    # New target armor.
                                    targetf_troop_armor = ensure_no_negative(targetf_troop_armor - (attkerf_troop_admg))
                                    targetf_veh_armor = ensure_no_negative(targetf_veh_armor - (attkerf_troop_admg))

                                    target_total_armor -= target_troop_armor + target_veh_armor

                                    # New attacker hp.
                                    attkerf_troop_hp = ensure_no_negative(attkerf_troop_hp - (targetf_troop_bdmg + targetf_veh_bdmg))
                                    attkerf_veh_hp = ensure_no_negative(attkerf_veh_hp - (targetf_troop_bdmg + targetf_veh_bdmg))

                                    attker_total_hp -= (attkerf_troop_hp + attkerf_veh_hp)

                                    attker_troops -= round(attkerf_troop_hp//25)
                                    attker_tanks -= round(attkerf_veh_hp//2000)
                                    attker_artillery -= round(attkerf_veh_hp//10)
                                    attker_aa -= round(attkerf_veh_hp//75)

                                    newhp_emb = discord.Embed(title=f"{attker_name} VS {target_name} | Ground Battle.",
                                                            description=f"The battle between {attker_name} and {target_name}.",
                                                            color=discord.Color.red())
                                    newhp_emb.add_field(name="Attacker Stats:\n", value=f"Troops: {attker_troops:,}\n"
                                                                                        f"Tanks: {attker_tanks:,}\n"
                                                                                        f"Artillery: {attker_artillery:,}\n"
                                                                                        f"Anti-Air: {attker_aa:,}\n"
                                                                                        f"HP: {attker_total_hp:,}\n"
                                                                                        f"Armor: 0\n"
                                                                                        f"\n"
                                                                                        f"Body DMG: {attkerf_troop_bdmg+attkerf_veh_bdmg:,}\n"
                                                                                        f"Armor DMG: {attkerf_troop_admg+attkerf_veh_admg:,}\n", inline=True)
                                    newhp_emb.add_field(name="Defender Stats:\n", value=f"Troops: {target_troops:,}\n"
                                                                                        f"Tanks: {target_tanks:,}\n"
                                                                                        f"Artillery: {target_artillery:,}\n"
                                                                                        f"Anti-Air: {target_aa:,}\n"
                                                                                        f"HP: {target_total_hp:,}\n"
                                                                                        f"Armor: {target_total_armor}\n"
                                                                                        f"\n"
                                                                                        f"Body DMG: {targetf_troop_bdmg+targetf_veh_bdmg:,}\n"
                                                                                        f"Armor DMG: {targetf_troop_admg+targetf_veh_admg:,}\n", inline=True)
                                    await war_ch.send(embed=newhp_emb)

                                else:
                                    # New target armor.
                                    targetf_troop_armor = ensure_no_negative(targetf_troop_armor - (attkerf_troop_admg + attkerf_veh_admg))
                                    targetf_veh_armor = ensure_no_negative(targetf_veh_armor - (attkerf_troop_admg + attkerf_veh_admg))

                                    target_total_armor -= target_troop_armor + target_veh_armor

                                    # New attacker hp.
                                    attkerf_troop_hp = ensure_no_negative(attkerf_troop_hp - (targetf_troop_bdmg))
                                    attkerf_veh_hp = ensure_no_negative(attkerf_veh_hp - (targetf_troop_bdmg))

                                    attker_total_hp -= attkerf_troop_hp + attkerf_veh_hp

                                    attker_troops -= round(attkerf_troop_hp//25)
                                    attker_tanks -= round(attkerf_veh_hp//2000)
                                    attker_artillery -= round(attkerf_veh_hp//10)
                                    attker_aa -= round(attkerf_veh_hp//75)

                                    newhp_emb = discord.Embed(title=f"{attker_name} VS {target_name} | Ground Battle.",
                                                            description=f"The battle between {attker_name} and {target_name}.",
                                                            color=discord.Color.red())
                                    newhp_emb.add_field(name="Attacker Stats:\n", value=f"Troops: {attker_troops:,}\n"
                                                                                        f"Tanks: {attker_tanks:,}\n"
                                                                                        f"Artillery: {attker_artillery:,}\n"
                                                                                        f"Anti-Air: {attker_aa:,}\n"
                                                                                        f"HP: {attker_total_hp:,}\n"
                                                                                        f"Armor: 0\n"
                                                                                        f"\n"
                                                                                        f"Body DMG: {attkerf_troop_bdmg+attkerf_veh_bdmg:,}\n"
                                                                                        f"Armor DMG: {attkerf_troop_admg+attkerf_veh_admg:,}\n", inline=True)
                                    newhp_emb.add_field(name="Defender Stats:\n", value=f"Troops: {target_troops:,}\n"
                                                                                        f"Tanks: {target_tanks:,}\n"
                                                                                        f"Artillery: {target_artillery:,}\n"
                                                                                        f"Anti-Air: {target_aa:,}\n"
                                                                                        f"HP: {target_total_hp:,}\n"
                                                                                        f"Armor: 0\n"
                                                                                        f"\n"
                                                                                        f"Body DMG: {targetf_troop_bdmg+targetf_veh_bdmg:,}\n"
                                                                                        f"Armor DMG: {targetf_troop_admg+targetf_veh_admg:,}\n", inline=True)
                                    await war_ch.send(embed=newhp_emb)

                            # If both the attacker and defender do not have armor.
                            if targetf_veh_bdmg > attkerf_veh_bdmg:

                                # New target hp.
                                targetf_troop_hp = ensure_no_negative(targetf_troop_hp - (attkerf_troop_bdmg))
                                targetf_veh_hp = ensure_no_negative(targetf_veh_hp - (attkerf_troop_bdmg))

                                target_total_hp = ensure_no_negative(target_total_hp - (targetf_troop_hp + targetf_veh_hp))

                                target_troops -= round(targetf_troop_hp//25)
                                target_tanks -= round(targetf_veh_hp//2000)
                                target_artillery -= round(targetf_veh_hp//10)
                                target_aa -= round(targetf_veh_hp//75)

                                # New attacker hp.
                                attkerf_troop_hp = ensure_no_negative(attkerf_troop_hp - (targetf_troop_bdmg + targetf_veh_bdmg))
                                attkerf_veh_hp = ensure_no_negative(attkerf_veh_hp - (targetf_troop_bdmg + targetf_veh_bdmg))

                                attker_total_hp = ensure_no_negative(attker_total_hp - (attkerf_troop_hp + attkerf_veh_hp))

                                attker_troops -= round(attkerf_troop_hp//25)
                                attker_tanks -= round(attkerf_veh_hp//2000)
                                attker_artillery -= round(attkerf_veh_hp//10)
                                attker_aa -= round(attkerf_veh_hp//75)

                                newhp_emb = discord.Embed(title=f"{attker_name} VS {target_name} | Ground Battle.",
                                                        description=f"The battle between {attker_name} and {target_name}.",
                                                        color=discord.Color.red())
                                newhp_emb.add_field(name="Attacker Stats:\n", value=f"Troops: {attker_troops:,}\n"
                                                                                    f"Tanks: {attker_tanks:,}\n"
                                                                                    f"Artillery: {attker_artillery:,}\n"
                                                                                    f"Anti-Air: {attker_aa:,}\n"
                                                                                    f"HP: {attker_total_hp:,}\n"
                                                                                    f"Armor: 0\n"
                                                                                    f"\n"
                                                                                    f"Body DMG: {attkerf_troop_bdmg+attkerf_veh_bdmg:,}\n"
                                                                                    f"Armor DMG: {attkerf_troop_admg+attkerf_veh_admg:,}\n", inline=True)
                                newhp_emb.add_field(name="Defender Stats:\n", value=f"Troops: {target_troops:,}\n"
                                                                                    f"Tanks: {target_tanks:,}\n"
                                                                                    f"Artillery: {target_artillery:,}\n"
                                                                                    f"Anti-Air: {target_aa:,}\n"
                                                                                    f"HP: {target_total_hp:,}\n"
                                                                                    f"Armor: 0\n"
                                                                                    f"\n"
                                                                                    f"Body DMG: {targetf_troop_bdmg+targetf_veh_bdmg:,}\n"
                                                                                    f"Armor DMG: {targetf_troop_admg+targetf_veh_admg:,}\n", inline=True)
                                await war_ch.send(embed=newhp_emb)

                            else:
                                # New target hp.
                                targetf_troop_hp = ensure_no_negative(targetf_troop_hp - (attkerf_troop_bdmg + attkerf_veh_bdmg))
                                targetf_veh_hp = ensure_no_negative(targetf_veh_hp - (attkerf_troop_bdmg + attkerf_veh_bdmg))

                                target_total_hp = ensure_no_negative(target_total_hp - (targetf_troop_hp + targetf_veh_hp))

                                target_troops -= round(targetf_troop_hp//25)
                                target_tanks -= round(targetf_veh_hp//2000)
                                target_artillery -= round(targetf_veh_hp//10)
                                target_aa -= round(targetf_veh_hp//75)

                                # New attacker hp.
                                attkerf_troop_hp = ensure_no_negative(attkerf_troop_hp - (targetf_troop_bdmg))
                                attkerf_veh_hp = ensure_no_negative(attkerf_veh_hp - (targetf_troop_bdmg))

                                attker_total_hp = ensure_no_negative(attker_total_hp - (attkerf_troop_hp + attkerf_veh_hp))

                                attker_troops -= round(attkerf_troop_hp//25)
                                attker_tanks -= round(attkerf_veh_hp//2000)
                                attker_artillery -= round(attkerf_veh_hp//10)
                                attker_aa -= round(attkerf_veh_hp//75)

                                newhp_emb = discord.Embed(title=f"{attker_name} VS {target_name} | Ground Battle.",
                                                        description=f"The battle between {attker_name} and {target_name}.",
                                                        color=discord.Color.red())
                                newhp_emb.add_field(name="Attacker Stats:\n", value=f"Troops: {attker_troops:,}\n"
                                                                                    f"Tanks: {attker_tanks:,}\n"
                                                                                    f"Artillery: {attker_artillery:,}\n"
                                                                                    f"Anti-Air: {attker_aa:,}\n"
                                                                                    f"HP: {attker_total_hp:,}\n"
                                                                                    f"Armor: 0\n"
                                                                                    f"\n"
                                                                                    f"Body DMG: {attkerf_troop_bdmg+attkerf_veh_bdmg:,}\n"
                                                                                    f"Armor DMG: {attkerf_troop_admg+attkerf_veh_admg:,}\n", inline=True)
                                newhp_emb.add_field(name="Defender Stats:\n", value=f"Troops: {target_troops:,}\n"
                                                                                    f"Tanks: {target_tanks:,}\n"
                                                                                    f"Artillery: {target_artillery:,}\n"
                                                                                    f"Anti-Air: {target_aa:,}\n"
                                                                                    f"HP: {target_total_hp:,}\n"
                                                                                    f"Armor: 0\n"
                                                                                    f"\n"
                                                                                    f"Body DMG: {targetf_troop_bdmg+targetf_veh_bdmg:,}\n"
                                                                                    f"Armor DMG: {targetf_troop_admg+targetf_veh_admg:,}\n", inline=True)
                                await war_ch.send(embed=newhp_emb)

                            if ((target_troops <= 0 and attker_troops > 0) or (target_tanks <= 0 and attker_tanks > 0) or 
                                (target_artillery <= 0 and attker_artillery > 0) or (target_aa <= 0 and attker_aa > 0)):
                                winner_emb = discord.Embed(title=f"{attker_name} Victory!",
                                                           description=f"{attker_name} has won the war against {target_name}.",
                                                           color=discord.Color.green())
                                await war_ch.send(embed=winner_emb)

                                # Update the war status for attacker.
                                cursor.execute('UPDATE user_info SET war_status = ? WHERE user_id = ?', ("In Peace", attker_id))
                                conn.commit()

                                # Update the war status for defender.
                                cursor.execute('UPDATE user_info SET war_status = ? WHERE user_id = ?', ("In Peace", target_id))
                                conn.commit()

                                # Update attacker's mil stats
                                cursor.execute('''UPDATE user_mil SET troops = ?, tanks = ?, artillery = ?, 
                                            anti_air = ? WHERE name_nation = ?''', (attker_troops, attker_tanks, 
                                                                                    attker_artillery, attker_aa, attker_name))
                                conn.commit()

                                # Update defender's mil stats
                                cursor.execute('''UPDATE user_mil SET troops = ?, tanks = ?, artillery = ?, 
                                            anti_air = ? WHERE name_nation = ?''', (0, target_tanks, target_artillery,
                                                                                                target_aa, target_name))
                                conn.commit()
                                break

                            else:
                                winner_emb = discord.Embed(title=f"{target_name} Victory!",
                                                           description=f"{target_name} has won the war against {attker_name}.",
                                                           color=discord.Color.green())
                                await war_ch.send(embed=winner_emb)

                                cursor.execute('UPDATE user_info SET war_status = ? WHERE user_id = ?', ("In Peace", attker_id))
                                conn.commit()
                                cursor.execute('UPDATE user_info SET war_status = ? WHERE user_id = ?', ("In Peace", target_id))
                                conn.commit()

                                # Update attacker's mil stats
                                cursor.execute('''UPDATE user_mil SET troops = ?, tanks = ?, artillery = ?, 
                                            anti_air = ? WHERE name_nation = ?''', (0, attker_tanks, 
                                                                                    attker_artillery, attker_aa, attker_name))
                                conn.commit()

                                # Update defender's mil stats
                                cursor.execute('''UPDATE user_mil SET troops = ?, tanks = ?, artillery = ?, 
                                            anti_air = ? WHERE name_nation = ?''', (target_troops, target_tanks, target_artillery,
                                                                                                target_aa, target_name))
                                conn.commit()
                                break

            else:
                await ctx.send("Cannot declare war on yourself. ||retard||")

async def setup(bot):
    await bot.add_cog(War(bot))