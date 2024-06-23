import sqlite3
import discord
from discord.ext import commands
import asyncio
import globals


new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = globals.conn
cursor = globals.cursor


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
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (attker_id,))
        attker_result = cursor.fetchone()

        # fetch target user name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (target_id,))
        target_result = cursor.fetchone()

        if attker_result and target_result:

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
                    'SELECT * FROM user_mil WHERE name = ?',
                    (attker_name,))
                attker_mil_result = cursor.fetchone()

                # fetch target user's resources
                cursor.execute(
                    'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                    (target_name,))
                target_res_result = cursor.fetchone()

                # fetch target user's mil stats
                cursor.execute(
                    'SELECT * FROM user_mil WHERE name = ?',
                    (target_name,))
                target_mil_result = cursor.fetchone()

                if attker_res_result and target_res_result and target_mil_result and attker_mil_result:

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

                    # Ask for the ground tactics
                    try:
                        await target_user.send("What ground tactic would you like to use? (reply with a number)\n"
                                               "**1.** Trench Warfare\n"
                                               "**2.** Creeping Barrage\n"
                                               "**3.** Superior Firepower\n"
                                               "**4.** Massed Assault\n"
                                               "**5.** Elastic Defense\n"
                                               "**6.** Armored Spearhead\n")

                        def check(message):
                            return message.author == target_user

                        msg = await self.bot.wait_for('message', timeout=60, check=check)

                        match msg.content:
                            case "1":
                                await target_user.send("Selected **Trench Warfare** as ground tactic.")
                                target_ground_tactic = "Trench Warfare"
                            case "2":
                                await target_user.send("Selected **Creeping Barrage** as ground tactic.")
                                target_ground_tactic = "Creeping Barrage"
                            case "3":
                                await target_user.send("Selected **Superior Firepower** as ground tactic.")
                                target_ground_tactic = "Superior Firepower"
                            case "4":
                                await target_user.send("Selected **Massed Assault** as ground tactic.")
                                target_ground_tactic = "Massed Assault"
                            case "5":
                                await target_user.send("Selected **Elastic Defense** as ground tactic.")
                                target_ground_tactic = "Elastic Defense"
                            case "6":
                                await target_user.send("Selected **Armored Spearhead** as ground tactic.")
                                target_ground_tactic = "Armored Spearhead"
                            case _:
                                pass

                    except asyncio.TimeoutError:
                        return await target_user.send("You took too long to respond.")

                    await asyncio.sleep(10)

                    # Ask the attacker for tactic.
                    try:
                        await attker_user.send("What ground tactic would you like to use? (reply with a number)\n"
                                               "**1.** Trench Warfare\n"
                                               "**2.** Creeping Barrage\n"
                                               "**3.** Superior Firepower\n"
                                               "**4.** Massed Assault\n"
                                               "**5.** Elastic Defense\n"
                                               "**6.** Armored Spearhead\n")

                        def check3(message):
                            return message.author == attker_user

                        msg = await self.bot.wait_for('message', timeout=60, check=check3)

                        match msg.content:
                            case "1":
                                await attker_user.send("Selected **Trench Warfare** as ground tactic.")
                                attker_ground_tactic = "Trench Warfare"
                            case "2":
                                await attker_user.send("Selected **Creeping Barrage** as ground tactic.")
                                attker_ground_tactic = "Creeping Barrage"
                            case "3":
                                await attker_user.send("Selected **Superior Firepower** as ground tactic.")
                                attker_ground_tactic = "Superior Firepower"
                            case "4":
                                await attker_user.send("Selected **Massed Assault** as ground tactic.")
                                attker_ground_tactic = "Massed Assault"
                            case "5":
                                await attker_user.send("Selected **Elastic Defense** as ground tactic.")
                                attker_ground_tactic = "Elastic Defense"
                            case "6":
                                await attker_user.send("Selected **Armored Spearhead** as ground tactic.")
                                attker_ground_tactic = "Armored Spearhead"
                            case _:
                                pass

                    except asyncio.TimeoutError:
                        return await attker_user.send("You took too long to respond.")
                    
                    # Ask for the air tactics
                    await asyncio.sleep(10)

                    # Ask the defender for air tactic.
                    try:
                        await target_user.send("What air tactic would you like to use? (reply with a number)\n"
                                               "**1.** Scramble\n"
                                               "**2.** Close Air Support\n"
                                               "**3.** Formation Flying\n"
                                               "**4.** Superior Firepower\n")

                        def check2(message):
                            return message.author == target_user

                        msg2 = await self.bot.wait_for('message', timeout=60, check=check2)

                        match msg2.content:
                            case "1":
                                await target_user.send("Selected **Scramble** as air tactic.")
                                target_air_tactic = "Scramble"
                            case "2":
                                await target_user.send("Selected **Close Air Support** as air tactic.")
                                target_air_tactic = "Close Air Support"
                            case "3":
                                await target_user.send("Selected **Formation Flying** as air tactic.")
                                target_air_tactic = "Formation Flying"
                            case "4":
                                await target_user.send("Selected **Superior Firepower** as air tactic.")
                                target_air_tactic = "Superior Firepower"
                            case _:
                                pass

                    except asyncio.TimeoutError:
                        return await target_user.send("You took too long to respond.")

                    # Ask for the air tactics
                    await asyncio.sleep(10)
                    try:
                        await attker_user.send("What air tactic would you like to use? (reply with a number)\n"
                                               "**1.** Scramble\n"
                                               "**2.** Close Air Support\n"
                                               "**3.** Formation Flying\n"
                                               "**4.** Superior Firepower\n")

                        def check2(message):
                            return message.author == attker_user

                        msg2 = await self.bot.wait_for('message', timeout=60, check=check2)

                        match msg2.content:
                            case "1":
                                await attker_user.send("Selected **Scramble** as air tactic.")
                                attker_air_tactic = "Scramble"
                            case "2":
                                await attker_user.send("Selected **Close Air Support** as air tactic.")
                                attker_air_tactic = "Close Air Support"
                            case "3":
                                await attker_user.send("Selected **Formation Flying** as air tactic.")
                                attker_air_tactic = "Formation Flying"
                            case "4":
                                await attker_user.send("Selected **Superior Firepower** as air tactic.")
                                attker_air_tactic = "Superior Firepower"
                            case _:
                                pass

                    except asyncio.TimeoutError:
                        return await attker_user.send("You took too long to respond.")

                    # Attacker stats
                    attker_troops_hp = attker_troops * health_values["troop_hp"]
                    attker_tank_hp = attker_tanks * health_values["tank_hp"]
                    attker_art_hp = attker_artillery * health_values["arty_hp"]
                    attker_aa_hp = attker_aa * health_values["aa_hp"]
                    attker_total_hp = attker_troops_hp + attker_tank_hp + attker_art_hp + attker_aa_hp
                    attker_army_percentage = {
                        "troops": round(attker_troops_hp / attker_total_hp, 4),
                        "tanks": round(attker_tank_hp / attker_total_hp, 4),
                        "artillery": round(attker_art_hp / attker_total_hp, 4),
                        "antiair": round(attker_aa_hp / attker_total_hp, 4)
                    }

                    attker_troops_dmg = attker_troops * damage_values["troop_dmg"]
                    attker_veh_dmg = ((attker_tanks * damage_values["tank_dmg"]) + (attker_artillery * damage_values["arty_dmg"]) +
                                      (attker_aa * damage_values["aa_dmg"]))
                    attker_total_dmg = attker_troops_dmg + attker_veh_dmg

                    # Defender stats
                    target_troops_hp = target_troops * health_values["troop_hp"]
                    target_tank_hp = target_tanks * health_values["tank_hp"]
                    target_art_hp = target_artillery * health_values["arty_hp"]
                    target_aa_hp = target_aa * health_values["aa_hp"]
                    target_total_hp = target_troops_hp + target_tank_hp + target_art_hp + target_aa_hp
                    target_army_percentage = {
                        "troops": round(target_troops_hp / target_total_hp, 4),
                        "tanks": round(target_tank_hp / target_total_hp, 4),
                        "artillery": round(target_art_hp / target_total_hp, 4),
                        "antiair": round(target_aa_hp / target_total_hp, 4)
                    }

                    target_troops_dmg = target_troops * damage_values["troop_dmg"]
                    target_veh_dmg = ((target_tanks * damage_values["tank_dmg"]) + (target_artillery * damage_values["arty_dmg"]) +
                                      (target_aa * damage_values["aa_dmg"]))
                    target_total_dmg = target_troops_dmg + target_veh_dmg

                    # Bonuses
                    target_hp_bonus = 0
                    attker_hp_bonus = 0

                    target_dmg_bonus = 0
                    attker_dmg_bonus = 0

                    match target_ground_tactic:
                        case "Trench Warfare":
                            target_hp_bonus += target_total_hp * 0.3
                            target_dmg_bonus += target_total_dmg * 0.05
                        case "Creeping Barrage":
                            target_hp_bonus += target_total_hp * -0.05
                            target_dmg_bonus += target_total_dmg * 0.15
                        case "Superior Firepower":
                            target_hp_bonus += target_total_hp * 0.1
                            target_dmg_bonus += target_total_dmg * 0.50
                        case "Massed Assault":
                            target_hp_bonus += target_total_hp * 0.35
                            target_dmg_bonus += target_total_dmg * -0.05
                        case "Elastic Defense":
                            target_hp_bonus += target_total_hp * 0.10
                            target_dmg_bonus += target_total_dmg * 0.10
                        case "Armored Spearhead":
                            target_hp_bonus += target_total_hp * 0.10
                            target_dmg_bonus += target_total_dmg * 0.125
                        case _:
                            pass

                    match attker_ground_tactic:
                        case "Trench Warfare":
                            attker_hp_bonus += attker_total_hp * 0.3
                            attker_dmg_bonus += attker_total_dmg * 0.05
                        case "Creeping Barrage":
                            attker_hp_bonus += attker_total_hp * -0.05
                            attker_dmg_bonus += attker_total_dmg * 0.15
                        case "Superior Firepower":
                            attker_hp_bonus += attker_total_hp * 0.1
                            attker_dmg_bonus += attker_total_dmg * 0.50
                        case "Massed Assault":
                            attker_hp_bonus += attker_total_hp * 0.35
                            attker_dmg_bonus += attker_total_dmg * -0.05
                        case "Elastic Defense":
                            attker_hp_bonus += attker_total_hp * 0.10
                            attker_dmg_bonus += attker_total_dmg * 0.10
                        case "Armored Spearhead":
                            attker_hp_bonus += attker_total_hp * 0.10
                            attker_dmg_bonus += attker_total_dmg * 0.125
                        case _:
                            pass
                        
                    # Final attacker stats
                    final_attker_hp = attker_total_hp + attker_hp_bonus
                    print(attker_total_hp)
                    print(attker_hp_bonus)
                    print(f"final_attker_hp: {final_attker_hp}")
                    final_attker_dmg = attker_total_dmg + attker_dmg_bonus
                    print(f"final_attker_dmg: {final_attker_dmg}")

                    # Final defender stats
                    final_target_hp = target_total_hp + target_hp_bonus
                    print(f"final_target_hp: {final_attker_hp}")
                    final_target_dmg = target_total_dmg + target_dmg_bonus
                    print(f"final_target_dmg: {final_attker_dmg}")

                    init_emb = discord.Embed(title=f"{attker_name} VS {target_name}. | Ground Battle.", 
                                             description="The battle will start in 5 minutes.\n"
                                                         "Get ready!", color=0xEF2F73)
                    await ctx.send(embed=init_emb)
                    await asyncio.sleep(5)

                    initial_attker_hp = {
                        "troops": attker_troops * health_values["troop_hp"],
                        "tanks": attker_tanks * health_values["tank_hp"],
                        "artillery": attker_artillery * health_values["arty_hp"],
                        "aa": attker_aa * health_values["aa_hp"]
                    }

                    initial_target_hp = {
                        "troops": target_troops * health_values["troop_hp"],
                        "tanks": target_tanks * health_values["tank_hp"],
                        "artillery": target_artillery * health_values["arty_hp"],
                        "aa": target_aa * health_values["aa_hp"]
                    }

                    total_hp_attker = sum(initial_attker_hp.values())
                    total_hp_target = sum(initial_target_hp.values())

                    rounds = 0
                    while final_attker_hp > 0 and final_target_hp > 0:
                        final_target_hp -= final_attker_dmg
                        final_attker_hp -= final_target_dmg
                        rounds += 1

                        remaining_units_attker = {
                            "troops": max(0, round(final_attker_hp * attker_army_percentage["troops"] / health_values["troop_hp"])),
                            "tanks": max(0, round(final_attker_hp * attker_army_percentage["tanks"] / health_values["tank_hp"])),
                            "artillery": max(0, round(final_attker_hp * attker_army_percentage["artillery"] / health_values["arty_hp"])),
                            "aa": max(0, round(final_attker_hp * attker_army_percentage["antiair"] / health_values["aa_hp"]))
                        }

                        remaining_units_target = {
                            "troops": max(0, round(final_target_hp * target_army_percentage["troops"] / health_values["troop_hp"])),
                            "tanks": max(0, round(final_target_hp * target_army_percentage["tanks"] / health_values["tank_hp"])),
                            "artillery": max(0, round(final_target_hp * target_army_percentage["artillery"] / health_values["arty_hp"])),
                            "aa": max(0, round(final_target_hp * target_army_percentage["antiair"] / health_values["aa_hp"]))
                        }

                        await asyncio.sleep(3)
                        new_emb = discord.Embed(title=f"{attker_name} VS {target_name} | Ground Battle.",
                                                description=f"Round: {rounds}",
                                                color=0xEF2F73)
                        new_emb.add_field(name="Attacker Stats:\n", value=f"Troops: {remaining_units_attker['troops']:,}\n"
                                                                          f"Tanks: {remaining_units_attker['tanks']:,}\n"
                                                                          f"Artillery: {remaining_units_attker['artillery']:,}\n"
                                                                          f"Anti-Air: {remaining_units_attker['aa']:,}\n"
                                                                          f"HP: {max(0, final_attker_hp):,}\n"
                                                                          f"\n"
                                                                          f"Damage: {final_attker_dmg:,}\n", inline=True)
                        new_emb.add_field(name="Defender Stats:\n", value=f"Troops: {remaining_units_target['troops']:,}\n"
                                                                          f"Tanks: {remaining_units_target['tanks']:,}\n"
                                                                          f"Artillery: {remaining_units_target['artillery']:,}\n"
                                                                          f"Anti-Air: {remaining_units_target['aa']:,}\n"
                                                                          f"HP: {max(0, final_target_hp):,}\n"
                                                                          f"\n"
                                                                          f"Damage: {final_target_dmg:,}\n", inline=True)
                        await ctx.send(embed=new_emb)

                        # Gas and ammo usage
                        attker_gas_use = round((attker_tanks + attker_aa + attker_artillery) / 1000)
                        attker_ammo_use_troops = round(attker_troops / 4000)
                        attker_ammo_use_veh = round((attker_tanks + attker_aa + attker_artillery) / 500)
                        total_attker_ammo = attker_ammo_use_troops + attker_ammo_use_veh

                        cursor.execute('UPDATE resources SET gasoline = gasoline - ?, ammo = ammo - ? WHERE name = ?', (attker_gas_use, total_attker_ammo, attker_name))
                        conn.commit()

                        target_gas_use = round((target_tanks + target_aa + target_artillery) / 1000)
                        target_ammo_use_troops = round(target_troops / 4000)
                        target_ammo_use_veh = round((target_tanks + target_aa + target_artillery) / 500)
                        total_target_ammo = target_ammo_use_troops + target_ammo_use_veh

                        cursor.execute('UPDATE resources SET gasoline = gasoline - ?, ammo = ammo - ? WHERE name = ?', (target_gas_use, total_target_ammo, target_name))
                        conn.commit()

                    if final_attker_hp > final_target_hp:
                        winner_emb = discord.Embed(title=f"{attker_name} Victory!",
                                                   description=f"{attker_name} has won the war against {target_name}.",
                                                   color=0x5BF9A0)
                        await ctx.send(embed=winner_emb)

                        cursor.execute('UPDATE user_info SET war_status = ? WHERE user_id = ?', ("In Peace", attker_id))
                        conn.commit()
                        cursor.execute('UPDATE user_info SET war_status = ? WHERE user_id = ?', ("In Peace", target_id))
                        conn.commit()

                        # Update attacker's mil stats
                        cursor.execute('''UPDATE user_mil SET troops = ?, tanks = ?, artillery = ?, 
                                    anti_air = ? WHERE name = ?''', (remaining_units_attker["troops"], remaining_units_attker["tanks"], 
                                                                     remaining_units_attker["artillery"],
                                                                     remaining_units_attker["aa"], attker_name))
                        conn.commit()

                        # Update defender's mil stats
                        cursor.execute('''UPDATE user_mil SET troops = ?, tanks = ?, artillery = ?, 
                                    anti_air = ? WHERE name = ?''', (remaining_units_target['troops'], remaining_units_target['tanks'], 
                                                                     remaining_units_target['artillery'],
                                                                     remaining_units_target['aa'], target_name))
                        conn.commit()

                    else:
                        winner_emb = discord.Embed(title=f"{target_name} Victory!",
                                                   description=f"{target_name} has won the war against {attker_name}.",
                                                   color=0x5BF9A0)
                        await ctx.send(embed=winner_emb)

                        cursor.execute('UPDATE user_info SET war_status = ? WHERE user_id = ?', ("In Peace", attker_id))
                        conn.commit()
                        cursor.execute('UPDATE user_info SET war_status = ? WHERE user_id = ?', ("In Peace", target_id))
                        conn.commit()

                        # Update attacker's mil stats
                        cursor.execute('''UPDATE user_mil SET troops = ?, tanks = ?, artillery = ?, 
                                    anti_air = ? WHERE name = ?''', (remaining_units_attker["troops"], remaining_units_attker["tanks"], 
                                                                     remaining_units_attker["artillery"],
                                                                     remaining_units_attker["aa"], attker_name))
                        conn.commit()

                        # Update defender's mil stats
                        cursor.execute('''UPDATE user_mil SET troops = ?, tanks = ?, artillery = ?, 
                                    anti_air = ? WHERE name = ?''', (remaining_units_target['troops'], remaining_units_target['tanks'], 
                                                                     remaining_units_target['artillery'],
                                                                     remaining_units_target['aa'], target_name))
                        conn.commit()
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
