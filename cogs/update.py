import sqlite3
import discord
from discord.ext import commands, tasks
import random
import logging


new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = sqlite3.connect('player_info.db')
cursor = conn.cursor()

logging_folder = '/home/void/pw_custom/cogs/logging/update.log'

logging.basicConfig(filename=logging_folder, level=logging.INFO,
                    format='%(asctime)s %(message)s')

logger = logging.getLogger(__name__)


# Check housing.
async def CheckHousing():
    try:
        cursor.execute('SELECT * FROM user_info')
        for row in cursor.fetchall():
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = row

            # Fetch user's production infra
            cursor.execute(
                'SELECT name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory FROM infra WHERE name = ?',
                (name,))
            infra_result = cursor.fetchone()

            # Fetch user's military stats
            cursor.execute(
                'SELECT * FROM user_mil WHERE name = ?',
                (name,))
            mil_result = cursor.fetchone()

            # Fetch user's population stats.
            cursor.execute(
                'SELECT name, nation_score, gdp, adult, balance FROM user_stats WHERE name = ?',
                (name,))
            pop_result = cursor.fetchone()

            if infra_result and mil_result and pop_result:
                name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory = infra_result
                name, troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result
                name, nation_score, gdp, adult, balance = pop_result

                # Check for housing.
                # Population Housing
                basic_house_housing = basic_house * 4
                small_flat_housing = small_flat * 25
                apt_complex_housing = apt_complex * 30
                skyscraper_housing = skyscraper * 100

                total_housing = basic_house_housing + small_flat_housing + apt_complex_housing + skyscraper_housing

                if (adult > total_housing): # If user does not have enough housing.
                    if happiness <= 0:
                        happiness = 0
                        cursor.execute('UPDATE user_info SET happiness = 0 WHERE user_id = ?', (user_id,))
                        conn.commit()
                        pass
                    else:
                        cursor.execute('UPDATE user_info SET happiness = happiness - 15 WHERE name = ?', (name,))
                        conn.commit()

                    riot_chance = random.randint(1, 25)
                    not_housed = adult - total_housing

                    if riot_chance == 1:
                        logger.info(f"HOUSING CHECK: Check for housing done. Riot detected for {name}.\n")

                        # Calculates the damages of properties.
                        basic_house_damage = round(basic_house * 0.02)
                        small_flat_damage = round(small_flat * 0.02)
                        apt_complex_damage = round(apt_complex * 0.02)
                        skyscraper_damage = round(skyscraper * 0.02)
                        lumber_mill_damage = round(lumber_mill * 0.02)
                        coal_mine_damage = round(coal_mine * 0.02)
                        iron_mine_damage = round(iron_mine * 0.02)
                        lead_mine_damage = round(lead_mine * 0.02)
                        bauxite_mine_damage = round(bauxite_mine * 0.02)
                        oil_derrick_damage = round(oil_derrick * 0.02)
                        uranium_mine_damage = round(uranium_mine * 0.02)
                        farm_damage = round(farm * 0.02)
                        aluminium_factory_damage = round(aluminium_factory * 0.02)
                        steel_factory_damage = round(steel_factory * 0.02)
                        oil_refinery_damage = round(oil_refinery * 0.02)
                        ammo_factory_damage = round(ammo_factory * 0.02)
                        concrete_factory_damage = round(concrete_factory * 0.02)
                        militaryfactory_damage = round(militaryfactory * 0.02)
                        pop_death = round(adult//24)

                        # Update the population.
                        cursor.execute('UPDATE user_stats SET adult = adult - ? WHERE name = ?', (pop_death, name))
                        conn.commit()

                        # Update the infrastructure.
                        cursor.execute('''UPDATE infra SET basic_house = basic_house - ?, small_flat = small_flat - ?, apt_complex = apt_complex - ?, skyscraper = skyscraper - ?,
                                        lumber_mill = lumber_mill - ?, coal_mine = coal_mine - ?, iron_mine = iron_mine - ?, lead_mine = lead_mine - ?, bauxite_mine = bauxite_mine - ?,
                                        oil_derrick = oil_derrick - ?, uranium_mine = uranium_mine - ?, farm = farm - ?, aluminium_factory = aluminium_factory - ?,
                                        steel_factory = steel_factory - ?, oil_refinery = oil_refinery - ?, ammo_factory = ammo_factory - ?, concrete_factory = concrete_factory - ?,
                                        militaryfactory = militaryfactory - ? WHERE name = ?''',
                                        (basic_house_damage, small_flat_damage, apt_complex_damage, skyscraper_damage, lumber_mill_damage, coal_mine_damage, iron_mine_damage,
                                        lead_mine_damage, bauxite_mine_damage, oil_derrick_damage, uranium_mine_damage, farm_damage, aluminium_factory_damage,
                                        steel_factory_damage, oil_refinery_damage, ammo_factory_damage, concrete_factory_damage, militaryfactory_damage, name))
                        conn.commit()

                        logger.info(f'HOUSING CHECK: Damages caused by riots done for {name}.\n')
                    else:
                        logger.info(f"HOUSING CHECK: {name} did not pass the housing check. No riot for {name}.\n")

                else:
                    logger.info(f'HOUSING CHECK: {name} passed the housing check.\n')

            else:
                logger.info(f"HOUSING CHECK ERROR: Error fetching stats of {user_id}.\n")

    except Exception as e:
        print(f"HOUSING CHECK ERROR: {e}\n")


async def UpdateEconomy():
    try:
        cursor.execute('SELECT * FROM user_info')
        for row in cursor.fetchall():
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = row

            # fetch user's resources
            cursor.execute(
                'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                (name,))
            res_result = cursor.fetchone()

            # fetch user's production infra
            cursor.execute(
                'SELECT name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory FROM infra WHERE name = ?',
                (name,))
            infra_result = cursor.fetchone()

            # fetch user's military stats
            cursor.execute(
                'SELECT * FROM user_mil WHERE name = ?',
                (name,))
            mil_result = cursor.fetchone()

            # fetch user's population stats.
            cursor.execute(
                'SELECT name, nation_score, gdp, adult, balance FROM user_stats WHERE name = ?',
                (name,))
            pop_result = cursor.fetchone()

            if infra_result:
                name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory = infra_result
                name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result
                name, nation_score, gdp, adult, balance = pop_result
                name, troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result

                policy_upkeep = 0
                match police_policy:
                    case "Chill Police":
                        req_police_stations = adult // 300
                        policy_upkeep += req_police_stations * 0

                    case "Normal Police":
                        req_police_stations = adult // 300
                        policy_upkeep += round(req_police_stations * 1000)

                    case "Serious Police":
                        req_police_stations = adult // 300
                        policy_upkeep += round(req_police_stations * 7000)

                    case _:
                        pass

                match fire_policy:
                    case "Careless Firefighters":
                        req_fire_stations = adult // 500
                        policy_upkeep += round(req_fire_stations * 0)

                    case "Normal Firefighters":
                        req_fire_stations = adult // 500
                        policy_upkeep += round(req_fire_stations * 1000)

                    case "Speedy Firefighters":
                        req_fire_stations = adult // 500
                        policy_upkeep += round(req_fire_stations * 7000)

                    case _:
                        pass

                match hospital_policy:
                    case "Enhanced Healthcare":
                        req_hospitals = adult // 400
                        policy_upkeep += round(req_hospitals * 18000)

                    case "Normal Healthcare":
                        req_hospitals = adult // 400
                        policy_upkeep += round(req_hospitals * 1000)

                    case "Private Healthcare":
                        req_hospitals = adult // 400
                        policy_upkeep += round(req_hospitals * 500)

                    case "No Healthcare":
                        req_hospitals = adult // 400
                        policy_upkeep += round(req_hospitals * 0)
                    
                    case _:
                        pass

                async def UpdateResources(prod_wood, prod_coal, final_prod_iron, final_prod_lead, final_prod_bauxite, final_prod_oil, prod_uranium, prod_farm, prod_aluminium, prod_steel, prod_gas, prod_ammo, prod_concrete):
                    try:
                        # If the user does NOT meet resource demands.
                        if (iron < final_usage_iron) or (lead < final_usage_lead) or (bauxite < final_usage_bauxite) or (oil < usage_oil_gas):
                            prod_aluminium = 0
                            prod_steel = 0
                            prod_gas = 0
                            prod_ammo = 0
                            prod_concrete = 0

                            # Update the resources table
                            cursor.execute('UPDATE resources SET wood = wood + ?, coal = coal + ?, iron = iron + ?, lead = lead + ?, bauxite = bauxite + ?, oil = oil + ?, uranium = uranium + ?, food = food + ?, aluminium = aluminium + ?, steel = steel + ?, gasoline = gasoline + ?, ammo = ammo + ?, concrete = concrete + ? WHERE name = ?', 
                            (prod_wood, prod_coal, final_prod_iron, final_prod_lead, final_prod_bauxite, final_prod_oil, prod_uranium, prod_farm, prod_aluminium, prod_steel, prod_gas, prod_ammo, prod_concrete, name))
                            # Commit the changes to the database
                            conn.commit()

                            logger.info(f"UPDATE RESOURCES: Updating resources done for {name}. DOES NOT MEET DEMANDS.\n")
                            
                        else:  # If the user does meet resource demands.
                            # Update the resources table
                            cursor.execute('UPDATE resources SET wood = wood + ?, coal = coal + ?, iron = iron + ?, lead = lead + ?, bauxite = bauxite + ?, oil = oil + ?, uranium = uranium + ?, food = food + ?, aluminium = aluminium + ?, steel = steel + ?, gasoline = gasoline + ?, ammo = ammo + ?, concrete = concrete + ? WHERE name = ?', 
                            (prod_wood, prod_coal, final_prod_iron, final_prod_lead, final_prod_bauxite, final_prod_oil, prod_uranium, prod_farm, prod_aluminium, prod_steel, prod_gas, prod_ammo, prod_concrete, name))
                            conn.commit()

                            logger.info(f"UPDATE RESOURCES: Updating resources done for {name}. DOES MEET DEMANDS.\n")

                    except Exception as e:
                        logger.info(f"UPDATE RESOURCES ERROR: {e}\n")

                match gov_type:
                    case "Communism":
                        prod_wood = lumber_mill * 2 * 2
                        prod_coal = coal_mine * 1.2 * 2
                        prod_iron = iron_mine * 1 * 2
                        prod_lead = lead_mine * 0.8 * 2
                        prod_bauxite = bauxite_mine * 0.6 * 2
                        prod_oil = oil_derrick * 1 * 2
                        prod_uranium = uranium_mine * 0.05 * 2
                        prod_farm = farm * 10 * 2
                        prod_aluminium = aluminium_factory * 0.4 * 2
                        prod_steel = steel_factory * 0.3 * 2
                        prod_gas = oil_refinery * 0.2 * 2
                        prod_ammo = ammo_factory * 0.5 * 2
                        prod_concrete = concrete_factory * 0.6 * 2

                        # The consumption of each resource
                        usage_iron_wood = prod_wood * 0
                        usage_lead_wood = prod_wood * 0
                        usage_bauxite_wood = prod_wood * 0
                        usage_iron_coal = prod_coal * 0
                        usage_lead_coal = prod_coal * 0
                        usage_bauxite_coal = prod_coal * 0
                        usage_iron_iron = prod_iron * 0
                        usage_lead_iron = prod_iron * 0
                        usage_bauxite_iron = prod_iron * 0
                        usage_iron_lead = prod_lead * 0
                        usage_lead_lead = prod_lead * 0
                        usage_bauxite_lead = prod_lead * 0
                        usage_iron_bauxite = prod_bauxite * 0
                        usage_lead_bauxite = prod_bauxite * 0
                        usage_bauxite_bauxite = prod_bauxite * 0
                        usage_iron_oil = prod_oil * 0
                        usage_lead_oil = prod_oil * 0
                        usage_bauxite_oil = prod_oil * 0
                        usage_iron_uranium = prod_uranium * 0
                        usage_lead_uranium = prod_uranium * 0
                        usage_bauxite_uranium = prod_uranium * 0
                        usage_iron_food = prod_farm * 0
                        usage_lead_food = prod_farm * 0
                        usage_bauxite_food = prod_farm * 0
                        usage_iron_aluminium = prod_aluminium * 0.2
                        usage_lead_aluminium = prod_aluminium * 0.1
                        usage_bauxite_aluminium = prod_aluminium * 1.2
                        usage_iron_steel = prod_steel * 1.4
                        usage_lead_steel = prod_steel * 0.3
                        usage_bauxite_steel = prod_steel * 0.3
                        usage_oil_gas = prod_gas * 2
                        usage_lead_gas = prod_gas * 0
                        usage_bauxite_gas = prod_gas * 0
                        usage_iron_ammo = prod_ammo * 0.2
                        usage_lead_ammo = prod_ammo * 1.1
                        usage_bauxite_ammo = prod_ammo * 0
                        usage_iron_concrete = prod_concrete * 0.5
                        usage_lead_concrete = prod_concrete * 0
                        usage_bauxite_concrete = prod_concrete * 0

                        final_usage_iron = usage_iron_wood + usage_iron_coal + usage_iron_iron + usage_iron_lead + usage_iron_bauxite + usage_iron_oil + usage_iron_uranium + usage_iron_food + usage_iron_aluminium + usage_iron_steel + usage_iron_ammo + usage_iron_concrete
                        final_usage_lead = usage_lead_wood + usage_lead_coal + usage_lead_iron + usage_lead_lead + usage_lead_bauxite + usage_lead_oil + usage_lead_uranium + usage_lead_food + usage_lead_aluminium + usage_lead_steel + usage_lead_ammo + usage_lead_concrete
                        final_usage_bauxite = usage_bauxite_wood + usage_bauxite_coal + usage_bauxite_iron + usage_bauxite_lead + usage_bauxite_bauxite + usage_bauxite_oil + usage_bauxite_uranium + usage_bauxite_food + usage_bauxite_aluminium + usage_bauxite_steel + usage_bauxite_ammo + usage_bauxite_concrete

                        final_prod_iron = prod_iron - final_usage_iron
                        final_prod_lead = prod_lead - final_usage_lead
                        final_prod_bauxite = prod_bauxite - final_usage_bauxite
                        final_prod_oil = prod_oil - usage_oil_gas

                        wood_income = prod_wood * 10
                        coal_income = prod_coal * 30
                        iron_income = final_prod_iron * 20
                        lead_income = final_prod_lead * 50
                        bauxite_income = final_prod_bauxite * 80
                        oil_income = final_prod_oil * 200
                        uranium_income = prod_uranium * 1000
                        food_income = prod_farm * 20
                        aluminium_income = prod_aluminium * 1000
                        steel_income = prod_steel * 1500
                        gas_income = prod_gas * 1700
                        ammo_income = prod_ammo * 1000
                        concrete_income = prod_concrete * 800

                        resource_revenue = round(wood_income + coal_income + iron_income + lead_income + bauxite_income + oil_income + uranium_income + food_income + aluminium_income + steel_income + gas_income + ammo_income + concrete_income)

                        total_pop = adult
                        tax_revenue = (tax_rate * total_pop) * 0.50

                        basic_house_upkeep = basic_house * 20 * 0.8
                        small_flat_upkeep = small_flat * 40 * 0.8
                        apt_complex_upkeep = apt_complex * 60 * 0.8
                        skyscraper_upkeep = skyscraper * 100 * 0.8

                        lumber_mill_upkeep = lumber_mill * 100 * 0.8
                        coal_mine_upkeep = coal_mine * 150 * 0.8
                        iron_mine_upkeep = iron_mine * 200 * 0.8
                        lead_mine_upkeep = lead_mine * 250 * 0.8
                        bauxite_mine_upkeep = bauxite_mine * 300 * 0.8
                        oil_derrick_upkeep = oil_derrick * 400 * 0.8
                        uranium_mine_upkeep = uranium_mine * 600 * 0.8

                        farm_upkeep = farm * 100 * 0.8

                        aluminium_factory_upkeep = aluminium_factory * 400 * 0.8
                        steel_factory_upkeep = steel_factory * 500 * 0.8
                        oil_refinery_upkeep = oil_refinery * 600 * 0.8
                        ammo_factory_upkeep = ammo_factory * 700 * 0.8
                        concrete_factory_upkeep = concrete_factory * 600 * 0.8
                        militaryfactory_upkeep = militaryfactory * 800 * 0.8

                        infra_upkeep = (basic_house_upkeep + small_flat_upkeep + apt_complex_upkeep + skyscraper_upkeep +
                        lumber_mill_upkeep + coal_mine_upkeep + iron_mine_upkeep + lead_mine_upkeep +
                        bauxite_mine_upkeep + oil_derrick_upkeep + uranium_mine_upkeep +
                        farm_upkeep + aluminium_factory_upkeep + steel_factory_upkeep +
                        oil_refinery_upkeep + ammo_factory_upkeep + concrete_factory_upkeep +
                        militaryfactory_upkeep)

                        await UpdateResources(prod_wood, prod_coal, final_prod_iron, final_prod_lead, final_prod_bauxite, final_prod_oil, prod_uranium, prod_farm, prod_aluminium, prod_steel, prod_gas, prod_ammo, prod_concrete)

                        if war_status == "In Peace":

                            troops_upkeep = troops * 5
                            planes_upkeep = planes * 50
                            weapon_upkeep = weapon * 10
                            tanks_upkeep = tanks * 100
                            artillery_upkeep = artillery * 150
                            anti_air_upkeep = anti_air * 200
                            barracks_upkeep = barracks * 200
                            tank_factory_upkeep = tank_factory * 300
                            plane_factory_upkeep = plane_factory * 400
                            artillery_factory_upkeep = artillery_factory * 450
                            anti_air_factory_upkeep = anti_air_factory * 500

                            military_upkeep = (troops_upkeep + planes_upkeep + weapon_upkeep + tanks_upkeep +
                                            artillery_upkeep + anti_air_upkeep + barracks_upkeep +
                                            tank_factory_upkeep + plane_factory_upkeep +
                                            artillery_factory_upkeep + anti_air_factory_upkeep)

                            net_income = (tax_revenue + resource_revenue) - (infra_upkeep + military_upkeep + policy_upkeep)

                            cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (net_income, name))
                            conn.commit()

                            logger.info(f"UPDATE ECONOMY: Updating economy done for {name}.\n")

                        else:
                            troops_upkeep = troops * 5 * 1.5
                            planes_upkeep = planes * 50 * 1.5
                            weapon_upkeep = weapon * 10 * 1.5
                            tanks_upkeep = tanks * 100 * 1.5
                            artillery_upkeep = artillery * 150 * 1.5
                            anti_air_upkeep = anti_air * 200 * 1.5
                            barracks_upkeep = barracks * 200 * 1.5
                            tank_factory_upkeep = tank_factory * 300 * 1.5
                            plane_factory_upkeep = plane_factory * 400 * 1.5
                            artillery_factory_upkeep = artillery_factory * 450 * 1.5
                            anti_air_factory_upkeep = anti_air_factory * 500 * 1.5

                            military_upkeep = (troops_upkeep + planes_upkeep + weapon_upkeep + tanks_upkeep +
                                            artillery_upkeep + anti_air_upkeep + barracks_upkeep +
                                            tank_factory_upkeep + plane_factory_upkeep +
                                            artillery_factory_upkeep + anti_air_factory_upkeep)

                            net_income = (tax_revenue + resource_revenue) - (infra_upkeep + military_upkeep + policy_upkeep)

                            cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (net_income, name))
                            conn.commit()

                            logger.info(f"UPDATE ECONOMY: Updating economy done for {name}.\n")

                    case "Democracy":
                        prod_wood = lumber_mill * 2
                        prod_coal = coal_mine * 1.2
                        prod_iron = iron_mine * 1
                        prod_lead = lead_mine * 0.8
                        prod_bauxite = bauxite_mine * 0.6
                        prod_oil = oil_derrick * 1
                        prod_uranium = uranium_mine * 0.05
                        prod_farm = farm * 10
                        prod_aluminium = aluminium_factory * 0.4
                        prod_steel = steel_factory * 0.3
                        prod_gas = oil_refinery * 0.2
                        prod_ammo = ammo_factory * 0.5
                        prod_concrete = concrete_factory * 0.6

                        # The consumption of each resource
                        usage_iron_wood = prod_wood * 0
                        usage_lead_wood = prod_wood * 0
                        usage_bauxite_wood = prod_wood * 0
                        usage_iron_coal = prod_coal * 0
                        usage_lead_coal = prod_coal * 0
                        usage_bauxite_coal = prod_coal * 0
                        usage_iron_iron = prod_iron * 0
                        usage_lead_iron = prod_iron * 0
                        usage_bauxite_iron = prod_iron * 0
                        usage_iron_lead = prod_lead * 0
                        usage_lead_lead = prod_lead * 0
                        usage_bauxite_lead = prod_lead * 0
                        usage_iron_bauxite = prod_bauxite * 0
                        usage_lead_bauxite = prod_bauxite * 0
                        usage_bauxite_bauxite = prod_bauxite * 0
                        usage_iron_oil = prod_oil * 0
                        usage_lead_oil = prod_oil * 0
                        usage_bauxite_oil = prod_oil * 0
                        usage_iron_uranium = prod_uranium * 0
                        usage_lead_uranium = prod_uranium * 0
                        usage_bauxite_uranium = prod_uranium * 0
                        usage_iron_food = prod_farm * 0
                        usage_lead_food = prod_farm * 0
                        usage_bauxite_food = prod_farm * 0
                        usage_iron_aluminium = prod_aluminium * 0.2
                        usage_lead_aluminium = prod_aluminium * 0.1
                        usage_bauxite_aluminium = prod_aluminium * 1.2
                        usage_iron_steel = prod_steel * 1.4
                        usage_lead_steel = prod_steel * 0.3
                        usage_bauxite_steel = prod_steel * 0.3
                        usage_oil_gas = prod_gas * 0
                        usage_lead_gas = prod_gas * 0
                        usage_bauxite_gas = prod_gas * 0
                        usage_iron_ammo = prod_ammo * 0.2
                        usage_lead_ammo = prod_ammo * 1.1
                        usage_bauxite_ammo = prod_ammo * 0
                        usage_iron_concrete = prod_concrete * 0.5
                        usage_lead_concrete = prod_concrete * 0
                        usage_bauxite_concrete = prod_concrete * 0

                        final_usage_iron = usage_iron_wood + usage_iron_coal + usage_iron_iron + usage_iron_lead + usage_iron_bauxite + usage_iron_oil + usage_iron_uranium + usage_iron_food + usage_iron_aluminium + usage_iron_steel + usage_iron_ammo + usage_iron_concrete
                        final_usage_lead = usage_lead_wood + usage_lead_coal + usage_lead_iron + usage_lead_lead + usage_lead_bauxite + usage_lead_oil + usage_lead_uranium + usage_lead_food + usage_lead_aluminium + usage_lead_steel + usage_lead_ammo + usage_lead_concrete
                        final_usage_bauxite = usage_bauxite_wood + usage_bauxite_coal + usage_bauxite_iron + usage_bauxite_lead + usage_bauxite_bauxite + usage_bauxite_oil + usage_bauxite_uranium + usage_bauxite_food + usage_bauxite_aluminium + usage_bauxite_steel + usage_bauxite_ammo + usage_bauxite_concrete

                        final_prod_iron = prod_iron - final_usage_iron
                        final_prod_lead = prod_lead - final_usage_lead
                        final_prod_bauxite = prod_bauxite - final_usage_bauxite
                        final_prod_oil = prod_oil - usage_oil_gas

                        wood_income = prod_wood * 10
                        coal_income = prod_coal * 30
                        iron_income = final_prod_iron * 20
                        lead_income = final_prod_lead * 50
                        bauxite_income = final_prod_bauxite * 80
                        oil_income = final_prod_oil * 200
                        uranium_income = prod_uranium * 1000
                        food_income = prod_farm * 20
                        aluminium_income = prod_aluminium * 1000
                        steel_income = prod_steel * 1500
                        gas_income = prod_gas * 1700
                        ammo_income = prod_ammo * 1000
                        concrete_income = prod_concrete * 800

                        resource_revenue = wood_income + coal_income + iron_income + lead_income + bauxite_income + oil_income + uranium_income + food_income + aluminium_income + steel_income + gas_income + ammo_income + concrete_income

                        total_pop = adult
                        tax_revenue = (tax_rate * total_pop) * 0.50

                        basic_house_upkeep = basic_house * 20 * 1.2
                        small_flat_upkeep = small_flat * 40 * 1.2
                        apt_complex_upkeep = apt_complex * 60 * 1.2
                        skyscraper_upkeep = skyscraper * 100 * 1.2

                        lumber_mill_upkeep = lumber_mill * 100 * 1.2
                        coal_mine_upkeep = coal_mine * 150 * 1.2
                        iron_mine_upkeep = iron_mine * 200 * 1.2
                        lead_mine_upkeep = lead_mine * 250 * 1.2
                        bauxite_mine_upkeep = bauxite_mine * 300 * 1.2
                        oil_derrick_upkeep = oil_derrick * 400 * 1.2
                        uranium_mine_upkeep = uranium_mine * 600 * 1.2

                        farm_upkeep = farm * 100 * 1.2

                        aluminium_factory_upkeep = aluminium_factory * 400 * 1.2
                        steel_factory_upkeep = steel_factory * 500 * 1.2
                        oil_refinery_upkeep = oil_refinery * 600 * 1.2
                        ammo_factory_upkeep = ammo_factory * 700 * 1.2
                        concrete_factory_upkeep = concrete_factory * 600 * 1.2
                        militaryfactory_upkeep = militaryfactory * 800 * 1.2

                        infra_upkeep = (basic_house_upkeep + small_flat_upkeep + apt_complex_upkeep + skyscraper_upkeep +
                        lumber_mill_upkeep + coal_mine_upkeep + iron_mine_upkeep + lead_mine_upkeep +
                        bauxite_mine_upkeep + oil_derrick_upkeep + uranium_mine_upkeep +
                        farm_upkeep + aluminium_factory_upkeep + steel_factory_upkeep +
                        oil_refinery_upkeep + ammo_factory_upkeep + concrete_factory_upkeep +
                        militaryfactory_upkeep)

                        await UpdateResources(prod_wood, prod_coal, final_prod_iron, final_prod_lead, final_prod_bauxite, final_prod_oil, prod_uranium, prod_farm, prod_aluminium, prod_steel, prod_gas, prod_ammo, prod_concrete)

                        if war_status == "In Peace":

                            troops_upkeep = troops * 5
                            planes_upkeep = planes * 50
                            weapon_upkeep = weapon * 10
                            tanks_upkeep = tanks * 100
                            artillery_upkeep = artillery * 150
                            anti_air_upkeep = anti_air * 200
                            barracks_upkeep = barracks * 200
                            tank_factory_upkeep = tank_factory * 300
                            plane_factory_upkeep = plane_factory * 400
                            artillery_factory_upkeep = artillery_factory * 450
                            anti_air_factory_upkeep = anti_air_factory * 500

                            military_upkeep = (troops_upkeep + planes_upkeep + weapon_upkeep + tanks_upkeep +
                                            artillery_upkeep + anti_air_upkeep + barracks_upkeep +
                                            tank_factory_upkeep + plane_factory_upkeep +
                                            artillery_factory_upkeep + anti_air_factory_upkeep)

                            net_income = (tax_revenue + resource_revenue) - (infra_upkeep + military_upkeep + policy_upkeep)

                            cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (net_income, name))
                            conn.commit()

                            logger.info(f"UPDATE ECONOMY: Updating economy done for {name}.\n")
                        else:
                            troops_upkeep = troops * 5 * 1.5
                            planes_upkeep = planes * 50 * 1.5
                            weapon_upkeep = weapon * 10 * 1.5
                            tanks_upkeep = tanks * 100 * 1.5
                            artillery_upkeep = artillery * 150 * 1.5
                            anti_air_upkeep = anti_air * 200 * 1.5
                            barracks_upkeep = barracks * 200 * 1.5
                            tank_factory_upkeep = tank_factory * 300 * 1.5
                            plane_factory_upkeep = plane_factory * 400 * 1.5
                            artillery_factory_upkeep = artillery_factory * 450 * 1.5
                            anti_air_factory_upkeep = anti_air_factory * 500 * 1.5

                            military_upkeep = (troops_upkeep + planes_upkeep + weapon_upkeep + tanks_upkeep +
                                            artillery_upkeep + anti_air_upkeep + barracks_upkeep +
                                            tank_factory_upkeep + plane_factory_upkeep +
                                            artillery_factory_upkeep + anti_air_factory_upkeep)

                            net_income = (tax_revenue + resource_revenue) - (infra_upkeep + military_upkeep + policy_upkeep)

                            cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (net_income, name))
                            conn.commit()

                            logger.info(f"UPDATE ECONOMY: Updating economy done for {name}.\n")

                    case "Monarchy":
                        prod_wood = lumber_mill * 2
                        prod_coal = coal_mine * 1.2
                        prod_iron = iron_mine * 1
                        prod_lead = lead_mine * 0.8
                        prod_bauxite = bauxite_mine * 0.6
                        prod_oil = oil_derrick * 1
                        prod_uranium = uranium_mine * 0.05
                        prod_farm = farm * 10
                        prod_aluminium = aluminium_factory * 0.4
                        prod_steel = steel_factory * 0.3
                        prod_gas = oil_refinery * 0.2
                        prod_ammo = ammo_factory * 0.5
                        prod_concrete = concrete_factory * 0.6

                        # The consumption of each resource
                        usage_iron_wood = prod_wood * 0
                        usage_lead_wood = prod_wood * 0
                        usage_bauxite_wood = prod_wood * 0
                        usage_iron_coal = prod_coal * 0
                        usage_lead_coal = prod_coal * 0
                        usage_bauxite_coal = prod_coal * 0
                        usage_iron_iron = prod_iron * 0
                        usage_lead_iron = prod_iron * 0
                        usage_bauxite_iron = prod_iron * 0
                        usage_iron_lead = prod_lead * 0
                        usage_lead_lead = prod_lead * 0
                        usage_bauxite_lead = prod_lead * 0
                        usage_iron_bauxite = prod_bauxite * 0
                        usage_lead_bauxite = prod_bauxite * 0
                        usage_bauxite_bauxite = prod_bauxite * 0
                        usage_iron_oil = prod_oil * 0
                        usage_lead_oil = prod_oil * 0
                        usage_bauxite_oil = prod_oil * 0
                        usage_iron_uranium = prod_uranium * 0
                        usage_lead_uranium = prod_uranium * 0
                        usage_bauxite_uranium = prod_uranium * 0
                        usage_iron_food = prod_farm * 0
                        usage_lead_food = prod_farm * 0
                        usage_bauxite_food = prod_farm * 0
                        usage_iron_aluminium = prod_aluminium * 0.2
                        usage_lead_aluminium = prod_aluminium * 0.1
                        usage_bauxite_aluminium = prod_aluminium * 1.2
                        usage_iron_steel = prod_steel * 1.4
                        usage_lead_steel = prod_steel * 0.3
                        usage_bauxite_steel = prod_steel * 0.3
                        usage_oil_gas = prod_gas * 0
                        usage_lead_gas = prod_gas * 0
                        usage_bauxite_gas = prod_gas * 0
                        usage_iron_ammo = prod_ammo * 0.2
                        usage_lead_ammo = prod_ammo * 1.1
                        usage_bauxite_ammo = prod_ammo * 0
                        usage_iron_concrete = prod_concrete * 0.5
                        usage_lead_concrete = prod_concrete * 0
                        usage_bauxite_concrete = prod_concrete * 0

                        final_usage_iron = usage_iron_wood + usage_iron_coal + usage_iron_iron + usage_iron_lead + usage_iron_bauxite + usage_iron_oil + usage_iron_uranium + usage_iron_food + usage_iron_aluminium + usage_iron_steel + usage_iron_ammo + usage_iron_concrete
                        final_usage_lead = usage_lead_wood + usage_lead_coal + usage_lead_iron + usage_lead_lead + usage_lead_bauxite + usage_lead_oil + usage_lead_uranium + usage_lead_food + usage_lead_aluminium + usage_lead_steel + usage_lead_ammo + usage_lead_concrete
                        final_usage_bauxite = usage_bauxite_wood + usage_bauxite_coal + usage_bauxite_iron + usage_bauxite_lead + usage_bauxite_bauxite + usage_bauxite_oil + usage_bauxite_uranium + usage_bauxite_food + usage_bauxite_aluminium + usage_bauxite_steel + usage_bauxite_ammo + usage_bauxite_concrete

                        final_prod_iron = prod_iron - final_usage_iron
                        final_prod_lead = prod_lead - final_usage_lead
                        final_prod_bauxite = prod_bauxite - final_usage_bauxite
                        final_prod_oil = prod_oil - usage_oil_gas

                        wood_income = prod_wood * 10
                        coal_income = prod_coal * 30
                        iron_income = final_prod_iron * 20
                        lead_income = final_prod_lead * 50
                        bauxite_income = final_prod_bauxite * 80
                        oil_income = final_prod_oil * 200
                        uranium_income = prod_uranium * 1000
                        food_income = prod_farm * 20
                        aluminium_income = prod_aluminium * 1000
                        steel_income = prod_steel * 1500
                        gas_income = prod_gas * 1700
                        ammo_income = prod_ammo * 1000
                        concrete_income = prod_concrete * 800

                        resource_revenue = wood_income + coal_income + iron_income + lead_income + bauxite_income + oil_income + uranium_income + food_income + aluminium_income + steel_income + gas_income + ammo_income + concrete_income

                        total_pop = adult
                        tax_revenue = (tax_rate * total_pop) * 1.1

                        basic_house_upkeep = basic_house * 20 * 1.1
                        small_flat_upkeep = small_flat * 40 * 1.1
                        apt_complex_upkeep = apt_complex * 60 * 1.1
                        skyscraper_upkeep = skyscraper * 100 * 1.1

                        lumber_mill_upkeep = lumber_mill * 100 * 1.1
                        coal_mine_upkeep = coal_mine * 150 * 1.1
                        iron_mine_upkeep = iron_mine * 200 * 1.1
                        lead_mine_upkeep = lead_mine * 250 * 1.1
                        bauxite_mine_upkeep = bauxite_mine * 300 * 1.1
                        oil_derrick_upkeep = oil_derrick * 400 * 1.1
                        uranium_mine_upkeep = uranium_mine * 600 * 1.1

                        farm_upkeep = farm * 100 * 1.1

                        aluminium_factory_upkeep = aluminium_factory * 400 * 1.1
                        steel_factory_upkeep = steel_factory * 500 * 1.1
                        oil_refinery_upkeep = oil_refinery * 600 * 1.1
                        ammo_factory_upkeep = ammo_factory * 700 * 1.1
                        concrete_factory_upkeep = concrete_factory * 600 * 1.1
                        militaryfactory_upkeep = militaryfactory * 800 * 1.1

                        infra_upkeep = (basic_house_upkeep + small_flat_upkeep + apt_complex_upkeep + skyscraper_upkeep +
                        lumber_mill_upkeep + coal_mine_upkeep + iron_mine_upkeep + lead_mine_upkeep +
                        bauxite_mine_upkeep + oil_derrick_upkeep + uranium_mine_upkeep +
                        farm_upkeep + aluminium_factory_upkeep + steel_factory_upkeep +
                        oil_refinery_upkeep + ammo_factory_upkeep + concrete_factory_upkeep +
                        militaryfactory_upkeep)

                        await UpdateResources(prod_wood, prod_coal, final_prod_iron, final_prod_lead, final_prod_bauxite, final_prod_oil, prod_uranium, prod_farm, prod_aluminium, prod_steel, prod_gas, prod_ammo, prod_concrete)

                        if war_status == "In Peace":

                            troops_upkeep = troops * 5
                            planes_upkeep = planes * 50
                            weapon_upkeep = weapon * 10
                            tanks_upkeep = tanks * 100
                            artillery_upkeep = artillery * 150
                            anti_air_upkeep = anti_air * 200
                            barracks_upkeep = barracks * 200
                            tank_factory_upkeep = tank_factory * 300
                            plane_factory_upkeep = plane_factory * 400
                            artillery_factory_upkeep = artillery_factory * 450
                            anti_air_factory_upkeep = anti_air_factory * 500

                            military_upkeep = (troops_upkeep + planes_upkeep + weapon_upkeep + tanks_upkeep +
                                            artillery_upkeep + anti_air_upkeep + barracks_upkeep +
                                            tank_factory_upkeep + plane_factory_upkeep +
                                            artillery_factory_upkeep + anti_air_factory_upkeep)

                            net_income = (tax_revenue + resource_revenue) - (infra_upkeep + military_upkeep + policy_upkeep)

                            cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (net_income, name))
                            conn.commit()

                            logger.info(f"UPDATE ECONOMY: Updating economy done for {name}.\n")
                        else:
                            troops_upkeep = troops * 5 * 1.5
                            planes_upkeep = planes * 50 * 1.5
                            weapon_upkeep = weapon * 10 * 1.5
                            tanks_upkeep = tanks * 100 * 1.5
                            artillery_upkeep = artillery * 150 * 1.5
                            anti_air_upkeep = anti_air * 200 * 1.5
                            barracks_upkeep = barracks * 200 * 1.5
                            tank_factory_upkeep = tank_factory * 300 * 1.5
                            plane_factory_upkeep = plane_factory * 400 * 1.5
                            artillery_factory_upkeep = artillery_factory * 450 * 1.5
                            anti_air_factory_upkeep = anti_air_factory * 500 * 1.5

                            military_upkeep = (troops_upkeep + planes_upkeep + weapon_upkeep + tanks_upkeep +
                                            artillery_upkeep + anti_air_upkeep + barracks_upkeep +
                                            tank_factory_upkeep + plane_factory_upkeep +
                                            artillery_factory_upkeep + anti_air_factory_upkeep)

                            net_income = (tax_revenue + resource_revenue) - (infra_upkeep + military_upkeep + policy_upkeep)

                            cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (net_income, name))
                            conn.commit()

                            logger.info(f"UPDATE ECONOMY: Updating economy done for {name}.\n")

                    case "Fascism":
                        prod_wood = lumber_mill * 2
                        prod_coal = coal_mine * 1.2
                        prod_iron = iron_mine * 1
                        prod_lead = lead_mine * 0.8
                        prod_bauxite = bauxite_mine * 0.6
                        prod_oil = oil_derrick * 1
                        prod_uranium = uranium_mine * 0.05
                        prod_farm = farm * 10
                        prod_aluminium = aluminium_factory * 0.4
                        prod_steel = steel_factory * 0.3
                        prod_gas = oil_refinery * 0.2
                        prod_ammo = ammo_factory * 0.5
                        prod_concrete = concrete_factory * 0.6

                        # The consumption of each resource
                        usage_iron_wood = prod_wood * 0
                        usage_lead_wood = prod_wood * 0
                        usage_bauxite_wood = prod_wood * 0
                        usage_iron_coal = prod_coal * 0
                        usage_lead_coal = prod_coal * 0
                        usage_bauxite_coal = prod_coal * 0
                        usage_iron_iron = prod_iron * 0
                        usage_lead_iron = prod_iron * 0
                        usage_bauxite_iron = prod_iron * 0
                        usage_iron_lead = prod_lead * 0
                        usage_lead_lead = prod_lead * 0
                        usage_bauxite_lead = prod_lead * 0
                        usage_iron_bauxite = prod_bauxite * 0
                        usage_lead_bauxite = prod_bauxite * 0
                        usage_bauxite_bauxite = prod_bauxite * 0
                        usage_iron_oil = prod_oil * 0
                        usage_lead_oil = prod_oil * 0
                        usage_bauxite_oil = prod_oil * 0
                        usage_iron_uranium = prod_uranium * 0
                        usage_lead_uranium = prod_uranium * 0
                        usage_bauxite_uranium = prod_uranium * 0
                        usage_iron_food = prod_farm * 0
                        usage_lead_food = prod_farm * 0
                        usage_bauxite_food = prod_farm * 0
                        usage_iron_aluminium = prod_aluminium * 0.2
                        usage_lead_aluminium = prod_aluminium * 0.1
                        usage_bauxite_aluminium = prod_aluminium * 1.2
                        usage_iron_steel = prod_steel * 1.4
                        usage_lead_steel = prod_steel * 0.3
                        usage_bauxite_steel = prod_steel * 0.3
                        usage_oil_gas = prod_gas * 0
                        usage_lead_gas = prod_gas * 0
                        usage_bauxite_gas = prod_gas * 0
                        usage_iron_ammo = prod_ammo * 0.2
                        usage_lead_ammo = prod_ammo * 1.1
                        usage_bauxite_ammo = prod_ammo * 0
                        usage_iron_concrete = prod_concrete * 0.5
                        usage_lead_concrete = prod_concrete * 0
                        usage_bauxite_concrete = prod_concrete * 0

                        final_usage_iron = usage_iron_wood + usage_iron_coal + usage_iron_iron + usage_iron_lead + usage_iron_bauxite + usage_iron_oil + usage_iron_uranium + usage_iron_food + usage_iron_aluminium + usage_iron_steel + usage_iron_ammo + usage_iron_concrete
                        final_usage_lead = usage_lead_wood + usage_lead_coal + usage_lead_iron + usage_lead_lead + usage_lead_bauxite + usage_lead_oil + usage_lead_uranium + usage_lead_food + usage_lead_aluminium + usage_lead_steel + usage_lead_ammo + usage_lead_concrete
                        final_usage_bauxite = usage_bauxite_wood + usage_bauxite_coal + usage_bauxite_iron + usage_bauxite_lead + usage_bauxite_bauxite + usage_bauxite_oil + usage_bauxite_uranium + usage_bauxite_food + usage_bauxite_aluminium + usage_bauxite_steel + usage_bauxite_ammo + usage_bauxite_concrete

                        final_prod_iron = prod_iron - final_usage_iron
                        final_prod_lead = prod_lead - final_usage_lead
                        final_prod_bauxite = prod_bauxite - final_usage_bauxite
                        final_prod_oil = prod_oil - usage_oil_gas

                        wood_income = prod_wood * 10
                        coal_income = prod_coal * 30
                        iron_income = final_prod_iron * 20
                        lead_income = final_prod_lead * 50
                        bauxite_income = final_prod_bauxite * 80
                        oil_income = final_prod_oil * 200
                        uranium_income = prod_uranium * 1000
                        food_income = prod_farm * 20
                        aluminium_income = prod_aluminium * 1000
                        steel_income = prod_steel * 1500
                        gas_income = prod_gas * 1700
                        ammo_income = prod_ammo * 1000
                        concrete_income = prod_concrete * 800

                        resource_revenue = wood_income + coal_income + iron_income + lead_income + bauxite_income + oil_income + uranium_income + food_income + aluminium_income + steel_income + gas_income + ammo_income + concrete_income

                        total_pop = adult
                        tax_revenue = (tax_rate * total_pop) * 0.9

                        basic_house_upkeep = basic_house * 20 * 1.5
                        small_flat_upkeep = small_flat * 40 * 1.5
                        apt_complex_upkeep = apt_complex * 60 * 1.5
                        skyscraper_upkeep = skyscraper * 100 * 1.5

                        lumber_mill_upkeep = lumber_mill * 100 * 1.5
                        coal_mine_upkeep = coal_mine * 150 * 1.5
                        iron_mine_upkeep = iron_mine * 200 * 1.5
                        lead_mine_upkeep = lead_mine * 250 * 1.5
                        bauxite_mine_upkeep = bauxite_mine * 300 * 1.5
                        oil_derrick_upkeep = oil_derrick * 400 * 1.5
                        uranium_mine_upkeep = uranium_mine * 600 * 1.5

                        farm_upkeep = farm * 100 * 1.5

                        aluminium_factory_upkeep = aluminium_factory * 400 * 1.5
                        steel_factory_upkeep = steel_factory * 500 * 1.5
                        oil_refinery_upkeep = oil_refinery * 600 * 1.5
                        ammo_factory_upkeep = ammo_factory * 700 * 1.5
                        concrete_factory_upkeep = concrete_factory * 600 * 1.5
                        militaryfactory_upkeep = militaryfactory * 800 * 1.5

                        infra_upkeep = (basic_house_upkeep + small_flat_upkeep + apt_complex_upkeep + skyscraper_upkeep +
                        lumber_mill_upkeep + coal_mine_upkeep + iron_mine_upkeep + lead_mine_upkeep +
                        bauxite_mine_upkeep + oil_derrick_upkeep + uranium_mine_upkeep +
                        farm_upkeep + aluminium_factory_upkeep + steel_factory_upkeep +
                        oil_refinery_upkeep + ammo_factory_upkeep + concrete_factory_upkeep +
                        militaryfactory_upkeep)

                        await UpdateResources(prod_wood, prod_coal, final_prod_iron, final_prod_lead, final_prod_bauxite, final_prod_oil, prod_uranium, prod_farm, prod_aluminium, prod_steel, prod_gas, prod_ammo, prod_concrete)

                        if war_status == "In Peace":

                            troops_upkeep = troops * 5
                            planes_upkeep = planes * 50
                            weapon_upkeep = weapon * 10
                            tanks_upkeep = tanks * 100
                            artillery_upkeep = artillery * 150
                            anti_air_upkeep = anti_air * 200
                            barracks_upkeep = barracks * 200
                            tank_factory_upkeep = tank_factory * 300
                            plane_factory_upkeep = plane_factory * 400
                            artillery_factory_upkeep = artillery_factory * 450
                            anti_air_factory_upkeep = anti_air_factory * 500

                            military_upkeep = (troops_upkeep + planes_upkeep + weapon_upkeep + tanks_upkeep +
                                            artillery_upkeep + anti_air_upkeep + barracks_upkeep +
                                            tank_factory_upkeep + plane_factory_upkeep +
                                            artillery_factory_upkeep + anti_air_factory_upkeep)

                            net_income = (tax_revenue + resource_revenue) - (infra_upkeep + military_upkeep + policy_upkeep)

                            cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (net_income, name))
                            conn.commit()

                            logger.info(f"UPDATE ECONOMY: Updating economy done for {name}.\n")
                        else:
                            troops_upkeep = troops * 5 * 0.5
                            planes_upkeep = planes * 50 * 0.5
                            weapon_upkeep = weapon * 10 * 0.5
                            tanks_upkeep = tanks * 100 * 0.5
                            artillery_upkeep = artillery * 150 * 0.5
                            anti_air_upkeep = anti_air * 200 * 0.5
                            barracks_upkeep = barracks * 200 * 0.5
                            tank_factory_upkeep = tank_factory * 300 * 0.5
                            plane_factory_upkeep = plane_factory * 400 * 0.5
                            artillery_factory_upkeep = artillery_factory * 450 * 0.5
                            anti_air_factory_upkeep = anti_air_factory * 500 * 0.5

                            military_upkeep = (troops_upkeep + planes_upkeep + weapon_upkeep + tanks_upkeep +
                                            artillery_upkeep + anti_air_upkeep + barracks_upkeep +
                                            tank_factory_upkeep + plane_factory_upkeep +
                                            artillery_factory_upkeep + anti_air_factory_upkeep)

                            net_income = (tax_revenue + resource_revenue) - (infra_upkeep + military_upkeep + policy_upkeep)

                            cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (net_income, name))
                            conn.commit()

                            logger.info(f"UPDATE ECONOMY: Updating economy done for {name}.\n")

                    case "Socialism":
                        prod_wood = lumber_mill * 2
                        prod_coal = coal_mine * 1.2
                        prod_iron = iron_mine * 1
                        prod_lead = lead_mine * 0.8
                        prod_bauxite = bauxite_mine * 0.6
                        prod_oil = oil_derrick * 1
                        prod_uranium = uranium_mine * 0.05
                        prod_farm = farm * 10
                        prod_aluminium = aluminium_factory * 0.4
                        prod_steel = steel_factory * 0.3
                        prod_gas = oil_refinery * 0.2
                        prod_ammo = ammo_factory * 0.5
                        prod_concrete = concrete_factory * 0.6

                        # The consumption of each resource
                        usage_iron_wood = prod_wood * 0
                        usage_lead_wood = prod_wood * 0
                        usage_bauxite_wood = prod_wood * 0
                        usage_iron_coal = prod_coal * 0
                        usage_lead_coal = prod_coal * 0
                        usage_bauxite_coal = prod_coal * 0
                        usage_iron_iron = prod_iron * 0
                        usage_lead_iron = prod_iron * 0
                        usage_bauxite_iron = prod_iron * 0
                        usage_iron_lead = prod_lead * 0
                        usage_lead_lead = prod_lead * 0
                        usage_bauxite_lead = prod_lead * 0
                        usage_iron_bauxite = prod_bauxite * 0
                        usage_lead_bauxite = prod_bauxite * 0
                        usage_bauxite_bauxite = prod_bauxite * 0
                        usage_iron_oil = prod_oil * 0
                        usage_lead_oil = prod_oil * 0
                        usage_bauxite_oil = prod_oil * 0
                        usage_iron_uranium = prod_uranium * 0
                        usage_lead_uranium = prod_uranium * 0
                        usage_bauxite_uranium = prod_uranium * 0
                        usage_iron_food = prod_farm * 0
                        usage_lead_food = prod_farm * 0
                        usage_bauxite_food = prod_farm * 0
                        usage_iron_aluminium = prod_aluminium * 0.2
                        usage_lead_aluminium = prod_aluminium * 0.1
                        usage_bauxite_aluminium = prod_aluminium * 1.2
                        usage_iron_steel = prod_steel * 1.4
                        usage_lead_steel = prod_steel * 0.3
                        usage_bauxite_steel = prod_steel * 0.3
                        usage_oil_gas = prod_gas * 0
                        usage_lead_gas = prod_gas * 0
                        usage_bauxite_gas = prod_gas * 0
                        usage_iron_ammo = prod_ammo * 0.2
                        usage_lead_ammo = prod_ammo * 1.1
                        usage_bauxite_ammo = prod_ammo * 0
                        usage_iron_concrete = prod_concrete * 0.5
                        usage_lead_concrete = prod_concrete * 0
                        usage_bauxite_concrete = prod_concrete * 0

                        final_usage_iron = usage_iron_wood + usage_iron_coal + usage_iron_iron + usage_iron_lead + usage_iron_bauxite + usage_iron_oil + usage_iron_uranium + usage_iron_food + usage_iron_aluminium + usage_iron_steel + usage_iron_ammo + usage_iron_concrete
                        final_usage_lead = usage_lead_wood + usage_lead_coal + usage_lead_iron + usage_lead_lead + usage_lead_bauxite + usage_lead_oil + usage_lead_uranium + usage_lead_food + usage_lead_aluminium + usage_lead_steel + usage_lead_ammo + usage_lead_concrete
                        final_usage_bauxite = usage_bauxite_wood + usage_bauxite_coal + usage_bauxite_iron + usage_bauxite_lead + usage_bauxite_bauxite + usage_bauxite_oil + usage_bauxite_uranium + usage_bauxite_food + usage_bauxite_aluminium + usage_bauxite_steel + usage_bauxite_ammo + usage_bauxite_concrete

                        final_prod_iron = prod_iron - final_usage_iron
                        final_prod_lead = prod_lead - final_usage_lead
                        final_prod_bauxite = prod_bauxite - final_usage_bauxite
                        final_prod_oil = prod_oil - usage_oil_gas

                        wood_income = prod_wood * 10
                        coal_income = prod_coal * 30
                        iron_income = final_prod_iron * 20
                        lead_income = final_prod_lead * 50
                        bauxite_income = final_prod_bauxite * 80
                        oil_income = final_prod_oil * 200
                        uranium_income = prod_uranium * 1000
                        food_income = prod_farm * 20
                        aluminium_income = prod_aluminium * 1000
                        steel_income = prod_steel * 1500
                        gas_income = prod_gas * 1700
                        ammo_income = prod_ammo * 1000
                        concrete_income = prod_concrete * 800

                        resource_revenue = wood_income + coal_income + iron_income + lead_income + bauxite_income + oil_income + uranium_income + food_income + aluminium_income + steel_income + gas_income + ammo_income + concrete_income

                        total_pop = adult
                        tax_revenue = (tax_rate * total_pop) * 0.6

                        basic_house_upkeep = basic_house * 20 * 0.9
                        small_flat_upkeep = small_flat * 40 * 0.9
                        apt_complex_upkeep = apt_complex * 60 * 0.9
                        skyscraper_upkeep = skyscraper * 100 * 0.9

                        lumber_mill_upkeep = lumber_mill * 100 * 0.9
                        coal_mine_upkeep = coal_mine * 150 * 0.9
                        iron_mine_upkeep = iron_mine * 200 * 0.9
                        lead_mine_upkeep = lead_mine * 250 * 0.9
                        bauxite_mine_upkeep = bauxite_mine * 300 * 0.9
                        oil_derrick_upkeep = oil_derrick * 400 * 0.9
                        uranium_mine_upkeep = uranium_mine * 600 * 0.9

                        farm_upkeep = farm * 100 * 0.9

                        aluminium_factory_upkeep = aluminium_factory * 400 * 0.9
                        steel_factory_upkeep = steel_factory * 500 * 0.9
                        oil_refinery_upkeep = oil_refinery * 600 * 0.9
                        ammo_factory_upkeep = ammo_factory * 700 * 0.9
                        concrete_factory_upkeep = concrete_factory * 600 * 0.9
                        militaryfactory_upkeep = militaryfactory * 800 * 0.9

                        infra_upkeep = (basic_house_upkeep + small_flat_upkeep + apt_complex_upkeep + skyscraper_upkeep +
                        lumber_mill_upkeep + coal_mine_upkeep + iron_mine_upkeep + lead_mine_upkeep +
                        bauxite_mine_upkeep + oil_derrick_upkeep + uranium_mine_upkeep +
                        farm_upkeep + aluminium_factory_upkeep + steel_factory_upkeep +
                        oil_refinery_upkeep + ammo_factory_upkeep + concrete_factory_upkeep +
                        militaryfactory_upkeep)

                        await UpdateResources(prod_wood, prod_coal, final_prod_iron, final_prod_lead, final_prod_bauxite, final_prod_oil, prod_uranium, prod_farm, prod_aluminium, prod_steel, prod_gas, prod_ammo, prod_concrete)

                        if war_status == "In Peace":

                            troops_upkeep = troops * 5
                            planes_upkeep = planes * 50
                            weapon_upkeep = weapon * 10
                            tanks_upkeep = tanks * 100
                            artillery_upkeep = artillery * 150
                            anti_air_upkeep = anti_air * 200
                            barracks_upkeep = barracks * 200
                            tank_factory_upkeep = tank_factory * 300
                            plane_factory_upkeep = plane_factory * 400
                            artillery_factory_upkeep = artillery_factory * 450
                            anti_air_factory_upkeep = anti_air_factory * 500

                            military_upkeep = (troops_upkeep + planes_upkeep + weapon_upkeep + tanks_upkeep +
                                            artillery_upkeep + anti_air_upkeep + barracks_upkeep +
                                            tank_factory_upkeep + plane_factory_upkeep +
                                            artillery_factory_upkeep + anti_air_factory_upkeep)

                            net_income = (tax_revenue + resource_revenue) - (infra_upkeep + military_upkeep + policy_upkeep)

                            cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (net_income, name))
                            conn.commit()

                            logger.info(f"UPDATE ECONOMY: Updating economy done for {name}.\n")
                        else:
                            troops_upkeep = troops * 5 * 1.5
                            planes_upkeep = planes * 50 * 1.5
                            weapon_upkeep = weapon * 10 * 1.5
                            tanks_upkeep = tanks * 100 * 1.5
                            artillery_upkeep = artillery * 150 * 1.5
                            anti_air_upkeep = anti_air * 200 * 1.5
                            barracks_upkeep = barracks * 200 * 1.5
                            tank_factory_upkeep = tank_factory * 300 * 1.5
                            plane_factory_upkeep = plane_factory * 400 * 1.5
                            artillery_factory_upkeep = artillery_factory * 450 * 1.5
                            anti_air_factory_upkeep = anti_air_factory * 500 * 1.5

                            military_upkeep = (troops_upkeep + planes_upkeep + weapon_upkeep + tanks_upkeep +
                                            artillery_upkeep + anti_air_upkeep + barracks_upkeep +
                                            tank_factory_upkeep + plane_factory_upkeep +
                                            artillery_factory_upkeep + anti_air_factory_upkeep)

                            net_income = (tax_revenue + resource_revenue) - (infra_upkeep + military_upkeep + policy_upkeep)

                            cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (net_income, name))
                            conn.commit()

                            logger.info(f"UPDATE ECONOMY: Updating economy done for {name}.\n")

                    case "Anarchy":
                        prod_wood = lumber_mill * 2
                        prod_coal = coal_mine * 1.2
                        prod_iron = iron_mine * 1
                        prod_lead = lead_mine * 0.8
                        prod_bauxite = bauxite_mine * 0.6
                        prod_oil = oil_derrick * 1
                        prod_uranium = uranium_mine * 0.05
                        prod_farm = farm * 10
                        prod_aluminium = aluminium_factory * 0.4
                        prod_steel = steel_factory * 0.3
                        prod_gas = oil_refinery * 0.2
                        prod_ammo = ammo_factory * 0.5
                        prod_concrete = concrete_factory * 0.6

                        # The consumption of each resource
                        usage_iron_wood = prod_wood * 0
                        usage_lead_wood = prod_wood * 0
                        usage_bauxite_wood = prod_wood * 0
                        usage_iron_coal = prod_coal * 0
                        usage_lead_coal = prod_coal * 0
                        usage_bauxite_coal = prod_coal * 0
                        usage_iron_iron = prod_iron * 0
                        usage_lead_iron = prod_iron * 0
                        usage_bauxite_iron = prod_iron * 0
                        usage_iron_lead = prod_lead * 0
                        usage_lead_lead = prod_lead * 0
                        usage_bauxite_lead = prod_lead * 0
                        usage_iron_bauxite = prod_bauxite * 0
                        usage_lead_bauxite = prod_bauxite * 0
                        usage_bauxite_bauxite = prod_bauxite * 0
                        usage_iron_oil = prod_oil * 0
                        usage_lead_oil = prod_oil * 0
                        usage_bauxite_oil = prod_oil * 0
                        usage_iron_uranium = prod_uranium * 0
                        usage_lead_uranium = prod_uranium * 0
                        usage_bauxite_uranium = prod_uranium * 0
                        usage_iron_food = prod_farm * 0
                        usage_lead_food = prod_farm * 0
                        usage_bauxite_food = prod_farm * 0
                        usage_iron_aluminium = prod_aluminium * 0.2
                        usage_lead_aluminium = prod_aluminium * 0.1
                        usage_bauxite_aluminium = prod_aluminium * 1.2
                        usage_iron_steel = prod_steel * 1.4
                        usage_lead_steel = prod_steel * 0.3
                        usage_bauxite_steel = prod_steel * 0.3
                        usage_oil_gas = prod_gas * 0
                        usage_lead_gas = prod_gas * 0
                        usage_bauxite_gas = prod_gas * 0
                        usage_iron_ammo = prod_ammo * 0.2
                        usage_lead_ammo = prod_ammo * 1.1
                        usage_bauxite_ammo = prod_ammo * 0
                        usage_iron_concrete = prod_concrete * 0.5
                        usage_lead_concrete = prod_concrete * 0
                        usage_bauxite_concrete = prod_concrete * 0

                        final_usage_iron = usage_iron_wood + usage_iron_coal + usage_iron_iron + usage_iron_lead + usage_iron_bauxite + usage_iron_oil + usage_iron_uranium + usage_iron_food + usage_iron_aluminium + usage_iron_steel + usage_iron_ammo + usage_iron_concrete
                        final_usage_lead = usage_lead_wood + usage_lead_coal + usage_lead_iron + usage_lead_lead + usage_lead_bauxite + usage_lead_oil + usage_lead_uranium + usage_lead_food + usage_lead_aluminium + usage_lead_steel + usage_lead_ammo + usage_lead_concrete
                        final_usage_bauxite = usage_bauxite_wood + usage_bauxite_coal + usage_bauxite_iron + usage_bauxite_lead + usage_bauxite_bauxite + usage_bauxite_oil + usage_bauxite_uranium + usage_bauxite_food + usage_bauxite_aluminium + usage_bauxite_steel + usage_bauxite_ammo + usage_bauxite_concrete

                        final_prod_iron = prod_iron - final_usage_iron
                        final_prod_lead = prod_lead - final_usage_lead
                        final_prod_bauxite = prod_bauxite - final_usage_bauxite
                        final_prod_oil = prod_oil - usage_oil_gas

                        wood_income = prod_wood * 10
                        coal_income = prod_coal * 30
                        iron_income = final_prod_iron * 20
                        lead_income = final_prod_lead * 50
                        bauxite_income = final_prod_bauxite * 80
                        oil_income = final_prod_oil * 200
                        uranium_income = prod_uranium * 1000
                        food_income = prod_farm * 20
                        aluminium_income = prod_aluminium * 1000
                        steel_income = prod_steel * 1500
                        gas_income = prod_gas * 1700
                        ammo_income = prod_ammo * 1000
                        concrete_income = prod_concrete * 80

                        resource_revenue = wood_income + coal_income + iron_income + lead_income + bauxite_income + oil_income + uranium_income + food_income + aluminium_income + steel_income + gas_income + ammo_income + concrete_income

                        total_pop = adult
                        tax_revenue = (tax_rate * total_pop) * 0

                        basic_house_upkeep = basic_house * 20 * 1
                        small_flat_upkeep = small_flat * 40 * 1
                        apt_complex_upkeep = apt_complex * 60 * 1
                        skyscraper_upkeep = skyscraper * 100 * 1

                        lumber_mill_upkeep = lumber_mill * 100 * 1
                        coal_mine_upkeep = coal_mine * 150 * 1
                        iron_mine_upkeep = iron_mine * 200 * 1
                        lead_mine_upkeep = lead_mine * 250 * 1
                        bauxite_mine_upkeep = bauxite_mine * 300 * 1
                        oil_derrick_upkeep = oil_derrick * 400 * 1
                        uranium_mine_upkeep = uranium_mine * 600 * 1

                        farm_upkeep = farm * 100 * 1

                        aluminium_factory_upkeep = aluminium_factory * 400 * 1
                        steel_factory_upkeep = steel_factory * 500 * 1
                        oil_refinery_upkeep = oil_refinery * 600 * 1
                        ammo_factory_upkeep = ammo_factory * 700 * 1
                        concrete_factory_upkeep = concrete_factory * 600 * 1
                        militaryfactory_upkeep = militaryfactory * 800 * 1

                        infra_upkeep = (basic_house_upkeep + small_flat_upkeep + apt_complex_upkeep + skyscraper_upkeep +
                        lumber_mill_upkeep + coal_mine_upkeep + iron_mine_upkeep + lead_mine_upkeep +
                        bauxite_mine_upkeep + oil_derrick_upkeep + uranium_mine_upkeep +
                        farm_upkeep + aluminium_factory_upkeep + steel_factory_upkeep +
                        oil_refinery_upkeep + ammo_factory_upkeep + concrete_factory_upkeep +
                        militaryfactory_upkeep)

                        await UpdateResources(prod_wood, prod_coal, final_prod_iron, final_prod_lead, final_prod_bauxite, final_prod_oil, prod_uranium, prod_farm, prod_aluminium, prod_steel, prod_gas, prod_ammo, prod_concrete)

                        if war_status == "In Peace":

                            troops_upkeep = troops * 5
                            planes_upkeep = planes * 50
                            weapon_upkeep = weapon * 10
                            tanks_upkeep = tanks * 100
                            artillery_upkeep = artillery * 150
                            anti_air_upkeep = anti_air * 200
                            barracks_upkeep = barracks * 200
                            tank_factory_upkeep = tank_factory * 300
                            plane_factory_upkeep = plane_factory * 400
                            artillery_factory_upkeep = artillery_factory * 450
                            anti_air_factory_upkeep = anti_air_factory * 500

                            military_upkeep = (troops_upkeep + planes_upkeep + weapon_upkeep + tanks_upkeep +
                                            artillery_upkeep + anti_air_upkeep + barracks_upkeep +
                                            tank_factory_upkeep + plane_factory_upkeep +
                                            artillery_factory_upkeep + anti_air_factory_upkeep)

                            net_income = (tax_revenue + resource_revenue) - (infra_upkeep + military_upkeep + policy_upkeep)

                            cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (net_income, name))
                            conn.commit()

                            logger.info(f"UPDATE ECONOMY: Updating economy done for {name}.\n")
                        else:
                            troops_upkeep = troops * 5 * 1.5
                            planes_upkeep = planes * 50 * 1.5
                            weapon_upkeep = weapon * 10 * 1.5
                            tanks_upkeep = tanks * 100 * 1.5
                            artillery_upkeep = artillery * 150 * 1.5
                            anti_air_upkeep = anti_air * 200 * 1.5
                            barracks_upkeep = barracks * 200 * 1.5
                            tank_factory_upkeep = tank_factory * 300 * 1.5
                            plane_factory_upkeep = plane_factory * 400 * 1.5
                            artillery_factory_upkeep = artillery_factory * 450 * 1.5
                            anti_air_factory_upkeep = anti_air_factory * 500 * 1.5

                            military_upkeep = (troops_upkeep + planes_upkeep + weapon_upkeep + tanks_upkeep +
                                            artillery_upkeep + anti_air_upkeep + barracks_upkeep +
                                            tank_factory_upkeep + plane_factory_upkeep +
                                            artillery_factory_upkeep + anti_air_factory_upkeep)

                            net_income = (tax_revenue + resource_revenue) - (infra_upkeep + military_upkeep + policy_upkeep)

                            cursor.execute('UPDATE user_stats SET balance = balance + ? WHERE name = ?', (net_income, name))
                            conn.commit()

                            logger.info(f"UPDATE ECONOMY: Updating economy done for {name}.\n")
                    
                    case _:
                        logger.info(f"UPDATE ECONOMY ERROR: No 'gov_type' found for {name}.\n")
                        pass

            else:
                logger.info(f"UPDATE ECONOMY ERROR: Error fetching stats of {user_id}.\n")


    except Exception as e:
        logger.info(f'UPDATE ECONOMY ERROR: {e}\n')


async def FoodCheck():
    try:
        cursor.execute('SELECT * FROM user_info')
        for row in cursor.fetchall():
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = row

            # fetch user's resources
            cursor.execute(
                'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                (name,))
            res_result = cursor.fetchone()

            # fetch user's production infra
            cursor.execute(
                'SELECT name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory FROM infra WHERE name = ?',
                (name,))
            infra_result = cursor.fetchone()

            # fetch user's military stats
            cursor.execute(
                'SELECT * FROM user_mil WHERE name = ?',
                (name,))
            mil_result = cursor.fetchone()

            # fetch user's population stats.
            cursor.execute(
                'SELECT name, nation_score, gdp, adult, balance FROM user_stats WHERE name = ?',
                (name,))
            pop_result = cursor.fetchone()

            if infra_result:
                name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory = infra_result
                name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result
                name, nation_score, gdp, adult, balance = pop_result
                name, troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result

                pop_food_req = round(adult//50)
                riot_chance = random.randint(1, 10)

                # if the user does NOT have enough food.
                if (pop_food_req > food):

                    if riot_chance == 1:
                        if happiness <= 0:
                            happiness = 0
                            cursor.execute('UPDATE user_info SET happiness = 0 WHERE user_id = ?', (user_id, ))
                            conn.commit()
                        else:
                            cursor.execute('UPDATE user_info SET happiness = happiness - ? WHERE user_id = ?', (15, user_id))
                            conn.commit()

                        adult_deaths = round(adult//24)

                        # Update the pop values.
                        cursor.execute('UPDATE user_stats SET adult = adult - ? WHERE name = ?',
                                        (adult_deaths, name))
                        conn.commit()

                        # Calculates the damages for infra.
                        lumber_mill_damage = round(lumber_mill * 0.02)
                        coal_mine_damage = round(coal_mine * 0.02)
                        iron_mine_damage = round(iron_mine * 0.02)
                        lead_mine_damage = round(lead_mine * 0.02)
                        bauxite_mine_damage = round(bauxite_mine * 0.02)
                        oil_derrick_damage = round(oil_derrick * 0.02)
                        uranium_mine_damage = round(uranium_mine * 0.02)
                        farm_damage = round(farm * 0.02)
                        aluminium_factory_damage = round(aluminium_factory * 0.02)
                        steel_factory_damage = round(steel_factory * 0.02)
                        oil_refinery_damage = round(oil_refinery * 0.02)
                        ammo_factory_damage = round(ammo_factory * 0.02)
                        concrete_factory_damage = round(concrete_factory * 0.02)
                        militaryfactory_damage = round(militaryfactory * 0.02)

                        # Update the infrastructure.
                        cursor.execute('''UPDATE infra SET lumber_mill = lumber_mill - ?, coal_mine = coal_mine - ?, iron_mine = iron_mine - ?, lead_mine = lead_mine - ?, bauxite_mine = bauxite_mine - ?,
                                        oil_derrick = oil_derrick - ?, uranium_mine = uranium_mine - ?, farm = farm - ?, aluminium_factory = aluminium_factory - ?,
                                        steel_factory = steel_factory - ?, oil_refinery = oil_refinery - ?, ammo_factory = ammo_factory - ?, concrete_factory = concrete_factory - ?,
                                        militaryfactory = militaryfactory - ? WHERE name = ?''',
                                        (lumber_mill_damage, coal_mine_damage, iron_mine_damage,
                                        lead_mine_damage, bauxite_mine_damage, oil_derrick_damage, uranium_mine_damage, farm_damage, aluminium_factory_damage,
                                        steel_factory_damage, oil_refinery_damage, ammo_factory_damage, concrete_factory_damage, militaryfactory_damage, name))
                        conn.commit()

                        logger.info(f"FOOD CHECK: {name} failed the food check. RIOT DETECTED.\n")

                    else:
                        if happiness <= 0:
                            happiness = 0
                            cursor.execute('UPDATE user_info SET happiness = 0 WHERE user_id = ?', (user_id, ))
                            conn.commit()
                        else:
                            cursor.execute('UPDATE user_info SET happiness = happiness - ? WHERE user_id = ?', (15, user_id))
                            conn.commit()

                        adult_deaths = round(adult//24)

                        # Update the pop values.
                        cursor.execute('UPDATE user_stats SET adult = adult - ? WHERE name = ?',
                                        (adult_deaths, name))
                        conn.commit()

                        logger.info(f"FOOD CHECK: {name} failed the food check. NO RIOT DETECTED.\n")

                else:
                    growth_multiplier = 1.0
                    if hospital_policy == "Enhanced Healthcare":
                        growth_multiplier += 0.2
                    # Update the population with the growth
                    adult_growth = round(adult//10 * growth_multiplier)
                    new_food = round((food - pop_food_req))

                    # Update the pop values.
                    cursor.execute('UPDATE user_stats SET adult = adult + ? WHERE name = ?',
                                    (adult_growth, name))
                    conn.commit()

                    # Update food value.
                    cursor.execute('UPDATE resources SET food = food - ? WHERE name = ?', (new_food, name))
                    conn.commit()

                    logger.info(f"FOOD CHECK: {name} passed the food check.\n")

            else:
                logger.info(f"UPDATE ECONOMY ERROR: Error fetching stats of {user_id}.\n")

    except Exception as e:
        logger.info(f'FOOD CHECK ERROR: {e}\n')


async def UpdateMilitary():
    try:
        cursor.execute('SELECT * FROM user_info')
        for row in cursor.fetchall():
            user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = row

            # fetch user's resources
            cursor.execute(
                'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                (name,))
            res_result = cursor.fetchone()

            # fetch user's production infra
            cursor.execute(
                'SELECT name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory FROM infra WHERE name = ?',
                (name,))
            infra_result = cursor.fetchone()

            # fetch user's military stats
            cursor.execute(
                'SELECT * FROM user_mil WHERE name = ?',
                (name,))
            mil_result = cursor.fetchone()

            # fetch user's population stats.
            cursor.execute(
                'SELECT name, nation_score, gdp, adult, balance FROM user_stats WHERE name = ?',
                (name,))
            pop_result = cursor.fetchone()

            if infra_result:
                name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory = infra_result
                name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result
                name, nation_score, gdp, adult, balance = pop_result
                name, troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result

                # Update Military.
                prod_aa = anti_air_factory * militaryfactory // 42
                usage_aa_steel = anti_air_factory * 4
                usage_aa_gas = anti_air_factory * 1
                prod_arty = artillery_factory * militaryfactory // 42
                usage_arty_steel = artillery_factory * 3
                usage_arty_gas = artillery_factory * 0.75
                prod_plane = plane_factory * militaryfactory // 45
                usage_plane_steel = plane_factory * 5.75
                usage_plane_gas = plane_factory * 2
                prod_tank = tank_factory * militaryfactory // 42
                usage_tank_steel = tank_factory * 5
                usage_tank_gas = tank_factory * 1.25

                # Total Military usage.
                mil_steel_usage = usage_aa_steel + usage_arty_steel + usage_plane_steel + usage_tank_steel
                mil_gas_usage = usage_aa_gas + usage_arty_gas + usage_plane_gas + usage_tank_gas

                if (mil_steel_usage > steel) or (mil_gas_usage > gasoline):  # If the user does NOT have enough resources.
                    prod_tank = 0
                    prod_plane = 0
                    prod_arty = 0
                    prod_aa = 0

                    # Update tank count.
                    cursor.execute('UPDATE user_mil SET tanks = tanks + ? WHERE name = ?', (prod_tank, name))
                    conn.commit()

                    # Update plane count.
                    cursor.execute('UPDATE user_mil SET planes = planes + ? WHERE name = ?', (prod_plane, name))
                    conn.commit()
            
                    # Update artillery count.
                    cursor.execute('UPDATE user_mil SET artillery = artillery + ? WHERE name = ?', (prod_arty, name))
                    conn.commit()
                
                    # Update Anti-Air.
                    cursor.execute('UPDATE user_mil SET anti_air = anti_air + ? WHERE name = ?', (prod_aa, name))
                    conn.commit()

                    logger.info(f"UPDATE MILITARY: {name} does not have enough resources. Military has not been updated.\n")
                
                else:  # if the user DOES have enough resources.
                    # Update tank count.
                    cursor.execute('UPDATE user_mil SET tanks = tanks + ? WHERE name = ?', (prod_tank, name))
                    conn.commit()

                    # Update plane count.
                    cursor.execute('UPDATE user_mil SET planes = planes + ? WHERE name = ?', (prod_plane, name))
                    conn.commit()
            
                    # Update artillery count.
                    cursor.execute('UPDATE user_mil SET artillery = artillery + ? WHERE name = ?', (prod_arty, name))
                    conn.commit()
                
                    # Update Anti-Air.
                    cursor.execute('UPDATE user_mil SET anti_air = anti_air + ? WHERE name = ?', (prod_aa, name))
                    conn.commit()
                
                    # Update resources for military.
                    cursor.execute('UPDATE resources SET steel = steel - ?, gasoline = gasoline - ? WHERE name = ?', (mil_steel_usage, mil_gas_usage, name))
                    conn.commit()

                    logger.info(f"UPDATE MILITARY: {name}'s military has been updated.\n")

            else:
                logger.info(f"UPDATE ECONOMY ERROR: Error fetching stats of {user_id}.\n")

    except Exception as e:
        logger.info(f'UPDATE MILITARY ERROR: {e}\n')

@tasks.loop(seconds=3600)
async def CheckHousingTask():
    await CheckHousing()

@tasks.loop(seconds=3600)
async def UpdateEconomyTask():
    await UpdateEconomy()

@tasks.loop(seconds=3600)
async def FoodCheckTask():
    await FoodCheck()

@tasks.loop(seconds=3600)
async def UpdateMilitaryTask():
    await UpdateMilitary()

UpdateMilitaryTask.start()
FoodCheckTask.start()
UpdateEconomyTask.start()
CheckHousingTask.start()

class Update(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def update(self, ctx):
        await ctx.send("This is no longer a command. It is done automatically for you :)")      

async def setup(bot):
    await bot.add_cog(Update(bot))