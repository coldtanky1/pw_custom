import logging
import random
import discord
from discord.ext import commands, tasks

from sim_funcs.NAI_func import NAI_Determiner
from sim_funcs.corps_func import Corp_spawn
from sim_funcs.corps_func import Corp_remove

import asyncio
import globals
from schema import *

new_line = '\n'

logging_folder = globals.logging_folder + 'update.log'

logging.basicConfig(filename=logging_folder, level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    force=True)

logger = logging.getLogger(__name__)

# Check housing.
async def CheckHousing():
    try:
        for row in UserInfo.select(UserInfo.user_id, UserInfo.name, UserInfo.happiness).tuples():
            user_id, name, happiness = row

            # Fetch user's production infra
            infra_result = Infra.select(
                Infra.basic_house, Infra.small_flat, Infra.apt_complex,
                Infra.skyscraper, Infra.lumber_mill, Infra.coal_mine,
                Infra.iron_mine, Infra.lead_mine, Infra.bauxite_mine,
                Infra.oil_derrick, Infra.uranium_mine, Infra.farm,
                Infra.aluminium_factory, Infra.steel_factory, Infra.oil_refinery,
                Infra.ammo_factory, Infra.concrete_factory, Infra.militaryfactory).where(Infra.name == name).tuples().first()

            # Fetch user's population stats.
            pop_result = UserStats.select().where(UserStats.name == name).first()

            if infra_result and pop_result:
                basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory = infra_result
                adult = pop_result.adult

                # Check for housing.
                # Population Housing
                basic_house_housing = basic_house * 4
                small_flat_housing = small_flat * 25
                apt_complex_housing = apt_complex * 30
                skyscraper_housing = skyscraper * 100

                total_housing = basic_house_housing + small_flat_housing + apt_complex_housing + skyscraper_housing

                if adult > total_housing:  # If user does not have enough housing.
                    if happiness <= 0:
                        happiness = 0
                        UserInfo.update(happiness=0).where(UserInfo.user_id == user_id).execute()
                        pass
                    else:
                        UserInfo.update(happiness=UserInfo.happiness - 15).where(UserInfo.user_id == user_id).execute()

                    riot_chance = random.randint(1, 25)

                    if riot_chance == 1:
                        logger.info(f"HOUSING CHECK: Check for housing done. Riot detected for {name}.\n")

                        # Calculates properties destroyed.
                        basic_house_damage = round(basic_house * 0.01)
                        small_flat_damage = round(small_flat * 0.01)
                        apt_complex_damage = round(apt_complex * 0.01)
                        skyscraper_damage = round(skyscraper * 0.01)
                        lumber_mill_damage = round(lumber_mill * 0.01)
                        coal_mine_damage = round(coal_mine * 0.01)
                        iron_mine_damage = round(iron_mine * 0.01)
                        lead_mine_damage = round(lead_mine * 0.01)
                        bauxite_mine_damage = round(bauxite_mine * 0.01)
                        oil_derrick_damage = round(oil_derrick * 0.01)
                        uranium_mine_damage = round(uranium_mine * 0.01)
                        farm_damage = round(farm * 0.01)
                        aluminium_factory_damage = round(aluminium_factory * 0.01)
                        steel_factory_damage = round(steel_factory * 0.01)
                        oil_refinery_damage = round(oil_refinery * 0.01)
                        ammo_factory_damage = round(ammo_factory * 0.01)
                        concrete_factory_damage = round(concrete_factory * 0.01)
                        militaryfactory_damage = round(militaryfactory * 0.01)
                        pop_death = round(adult//24)

                        # Update the population.
                        UserStats.update(adult=UserStats.adult - pop_death).where(UserStats.name == name).execute()

                        # Update the infrastructure.
                        Infra.update(basic_house=Infra.basic_house - basic_house_damage, small_flat=Infra.small_flat - small_flat_damage,
                            apt_complex=Infra.apt_complex - apt_complex_damage, skyscraper=Infra.skyscraper - skyscraper_damage,
                            lumber_mill=Infra.lumber_mill - lumber_mill_damage, coal_mine=Infra.coal_mine - coal_mine_damage,
                            iron_mine=Infra.iron_mine - iron_mine_damage, lead_mine=Infra.lead_mine - lead_mine_damage,
                            bauxite_mine=Infra.bauxite_mine - bauxite_mine_damage, oil_derrick=Infra.oil_derrick - oil_derrick_damage,
                            uranium_mine=Infra.uranium_mine - uranium_mine_damage, farm=Infra.farm - farm_damage,
                            aluminium_factory=Infra.aluminium_factory - aluminium_factory_damage,
                            steel_factory=Infra.steel_factory - steel_factory_damage,
                            oil_refinery=Infra.oil_refinery - oil_refinery_damage,
                            ammo_factory=Infra.ammo_factory - ammo_factory_damage,
                            concrete_factory=Infra.concrete_factory - concrete_factory_damage,
                            militaryfactory=Infra.militaryfactory - militaryfactory_damage).where(Infra.name == name).execute()

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
        for row in UserInfo.select(
            UserInfo.user_id, UserInfo.name, UserInfo.gov_type,
            UserInfo.tax_rate, UserInfo.police_policy, UserInfo.fire_policy,
            UserInfo.hospital_policy, UserInfo.war_status).tuples():
            user_id, name, gov_type, tax_rate, police_policy, fire_policy, hospital_policy, war_status = row

            # fetch user's resources
            res_result = Resources.select(Resources.iron, Resources.lead, Resources.bauxite, Resources.oil).where(Resources.name == name).tuples().first()
 
            # fetch user's production infra
            infra_result = Infra.select().where(Infra.name == name).tuples().first()

            # fetch user's military stats
            mil_result = UserMil.select().where(UserMil.name == name).tuples().first()

            # fetch user's population stats.
            pop_result = UserStats.select().where(UserStats.name == name).first()

            if infra_result:
                name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps, park, cinema, museum, concert_hall = infra_result
                iron, lead, bauxite, oil = res_result
                adult = pop_result.adult
                name, troops, planes, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result

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

                            logger.info(f"UPDATE RESOURCES: Updating resources done for {name}. DOES NOT MEET DEMANDS.\n")
                            
                        else:  # If the user does meet resource demands.
                            logger.info(f"UPDATE RESOURCES: Updating resources done for {name}. DOES MEET DEMANDS.\n")

                        Resources.update(wood=Resources.wood + prod_wood, coal=Resources.coal + prod_coal,
                            iron=Resources.iron + final_prod_iron, lead=Resources.lead + final_prod_lead,
                            bauxite=Resources.bauxite + final_prod_bauxite, oil=Resources.oil + final_prod_oil,
                            uranium=Resources.uranium + prod_uranium, food=Resources.food + prod_farm,
                            steel=Resources.steel + prod_steel, aluminium=Resources.aluminium + prod_aluminium,
                            gasoline=Resources.gasoline + prod_gas, ammo=Resources.ammo + prod_ammo,
                            concrete=Resources.concrete + prod_concrete).where(Resources.name == name).execute()

                    except Exception as e:
                        logger.info(f"UPDATE RESOURCES ERROR: {e}\n")

                # Calculating effects for different parts of update
                tax_revenue_bonus = 1
                upkeep_bonus = 1
                troops_upkeep_bonus = 1
                production_bonus = 1

                match gov_type:
                    case "Anarchy":
                        tax_revenue_bonus *= 0
                    case "Communism":
                        tax_revenue_bonus *= 0.5
                        upkeep_bonus *= 0.8
                        production_bonus *= 2
                    case "Democracy":
                        tax_revenue_bonus *= 1.2
                        upkeep_bonus *= 1.2
                    case "Fascism":
                        tax_revenue_bonus *= 0.9
                        upkeep_bonus *= 1.5
                        troops_upkeep_bonus *= 0.5
                    case "Monarchy":
                        tax_revenue_bonus *= 1.1
                        upkeep_bonus *= 1.1
                    case "Socialism":
                        tax_revenue_bonus *= 0.6
                        upkeep_bonus *= 0.9
                    case _:
                        logger.info(f"UPDATE ECONOMY ERROR: No 'gov_type' found for {name}.\n")

                # The production of each resource
                prod_wood = lumber_mill * 2 * production_bonus
                prod_coal = coal_mine * 1.2 * production_bonus
                prod_iron = iron_mine * 1 * production_bonus
                prod_lead = lead_mine * 0.8 * production_bonus
                prod_bauxite = bauxite_mine * 0.6 * production_bonus
                prod_oil = oil_derrick * 1 * production_bonus
                prod_uranium = uranium_mine * 0.05 * production_bonus
                prod_farm = farm * 10 * production_bonus
                prod_aluminium = aluminium_factory * 0.4 * production_bonus
                prod_steel = steel_factory * 0.3 * production_bonus
                prod_gas = oil_refinery * 0.2 * production_bonus
                prod_ammo = ammo_factory * 0.5 * production_bonus
                prod_concrete = concrete_factory * 0.6 * production_bonus

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

                NAI = NAI_Determiner(user_id)
                tax_revenue = round((tax_rate/100) * (NAI * adult)) * tax_revenue_bonus

                basic_house_upkeep = basic_house * 20
                small_flat_upkeep = small_flat * 40
                apt_complex_upkeep = apt_complex * 60
                skyscraper_upkeep = skyscraper * 100

                lumber_mill_upkeep = lumber_mill * 100
                coal_mine_upkeep = coal_mine * 150
                iron_mine_upkeep = iron_mine * 200
                lead_mine_upkeep = lead_mine * 250
                bauxite_mine_upkeep = bauxite_mine * 300
                oil_derrick_upkeep = oil_derrick * 400
                uranium_mine_upkeep = uranium_mine * 600

                farm_upkeep = farm * 100 * upkeep_bonus

                aluminium_factory_upkeep = aluminium_factory * 400
                steel_factory_upkeep = steel_factory * 500
                oil_refinery_upkeep = oil_refinery * 600
                ammo_factory_upkeep = ammo_factory * 700
                concrete_factory_upkeep = concrete_factory * 600
                militaryfactory_upkeep = militaryfactory * 800

                park_upkeep = park * 30
                cinema_upkeep = cinema * 60
                museum_upkeep = museum * 70
                concert_hall_upkeep = concert_hall * 120

                infra_upkeep = (basic_house_upkeep + small_flat_upkeep + apt_complex_upkeep + skyscraper_upkeep +
                                lumber_mill_upkeep + coal_mine_upkeep + iron_mine_upkeep + lead_mine_upkeep +
                                bauxite_mine_upkeep + oil_derrick_upkeep + uranium_mine_upkeep +
                                farm_upkeep + aluminium_factory_upkeep + steel_factory_upkeep +
                                oil_refinery_upkeep + ammo_factory_upkeep + concrete_factory_upkeep +
                                militaryfactory_upkeep + park_upkeep + cinema_upkeep + museum_upkeep + concert_hall_upkeep) * upkeep_bonus

                await UpdateResources(prod_wood, prod_coal, final_prod_iron, final_prod_lead, final_prod_bauxite, final_prod_oil, prod_uranium, prod_farm, prod_aluminium, prod_steel, prod_gas, prod_ammo, prod_concrete)

                if war_status == "In Peace":

                    troops_upkeep = troops * 5
                    planes_upkeep = planes * 50
                    tanks_upkeep = tanks * 100
                    artillery_upkeep = artillery * 150
                    anti_air_upkeep = anti_air * 200
                    barracks_upkeep = barracks * 200
                    tank_factory_upkeep = tank_factory * 300
                    plane_factory_upkeep = plane_factory * 400
                    artillery_factory_upkeep = artillery_factory * 450
                    anti_air_factory_upkeep = anti_air_factory * 500

                    military_upkeep = (troops_upkeep + planes_upkeep + tanks_upkeep +
                                       artillery_upkeep + anti_air_upkeep + barracks_upkeep +
                                       tank_factory_upkeep + plane_factory_upkeep +
                                       artillery_factory_upkeep + anti_air_factory_upkeep) * troops_upkeep_bonus

                    net_income = (tax_revenue + resource_revenue) - (infra_upkeep + military_upkeep + policy_upkeep)

                    UserStats.update(balance=UserStats.balance + net_income).where(UserStats.name == name).execute()

                    logger.info(f"UPDATE ECONOMY: Updating economy done for {name}.\n")
                else:
                    troops_upkeep = troops * 5 * 1.5
                    planes_upkeep = planes * 50 * 1.5
                    tanks_upkeep = tanks * 100 * 1.5
                    artillery_upkeep = artillery * 150 * 1.5
                    anti_air_upkeep = anti_air * 200 * 1.5
                    barracks_upkeep = barracks * 200 * 1.5
                    tank_factory_upkeep = tank_factory * 300 * 1.5
                    plane_factory_upkeep = plane_factory * 400 * 1.5
                    artillery_factory_upkeep = artillery_factory * 450 * 1.5
                    anti_air_factory_upkeep = anti_air_factory * 500 * 1.5

                    military_upkeep = (troops_upkeep + planes_upkeep + tanks_upkeep +
                                       artillery_upkeep + anti_air_upkeep + barracks_upkeep +
                                       tank_factory_upkeep + plane_factory_upkeep +
                                       artillery_factory_upkeep + anti_air_factory_upkeep) * troops_upkeep_bonus

                    net_income = (tax_revenue + resource_revenue) - (infra_upkeep + military_upkeep + policy_upkeep)

                    UserStats.update(balance=UserStats.balance + net_income).where(UserStats.name == name).execute()

                    logger.info(f"UPDATE ECONOMY: Updating economy done for {name}.\n")

            else:
                logger.info(f"UPDATE ECONOMY ERROR: Error fetching stats of {user_id}.\n")

    except Exception as e:
        logger.info(f'UPDATE ECONOMY ERROR: {e}\n')



async def FoodCheck():
    try:
        for row in UserInfo.select(UserInfo.user_id, UserInfo.name, UserInfo.hospital_policy, UserInfo.happiness).tuples():
            user_id, name, hospital_policy, happiness = row

            # fetch user's resources
            res_result = Resources.select().where(Resources.name == name).first()

            # fetch user's production infra
            infra_result = Infra.select(
                Infra.lumber_mill, Infra.coal_mine, Infra.iron_mine,
                Infra.lead_mine, Infra.bauxite_mine, Infra.oil_derrick,
                Infra.uranium_mine, Infra.farm, Infra.aluminium_factory,
                Infra.steel_factory, Infra.oil_refinery, Infra.ammo_factory,
                Infra.concrete_factory, Infra.militaryfactory).where(Infra.name == name).tuples().first()

            # fetch user's population stats.
            pop_result = UserStats.select().where(UserStats.name == name).first()

            if infra_result:
                lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory = infra_result
                food = res_result.food
                adult = pop_result.adult

                pop_food_req = round(adult//50)
                riot_chance = random.randint(1, 10)

                # if the user does NOT have enough food.
                if pop_food_req > food:

                    if riot_chance == 1:
                        if happiness <= 0:
                            happiness = 0
                            UserInfo.update(happiness=0).where(UserInfo.user_id == user_id).execute()
                        else:
                            UserInfo.update(happiness=UserInfo.happiness - 15).where(UserInfo.user_id == user_id).execute()

                        adult_deaths = round(adult//24)

                        # Update the pop values.
                        UserStats.update(adult=UserStats.adult - adult_deaths).where(UserStats.name == name).execute()

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
                        Infra.update(lumber_mill=lumber_mill - lumber_mill_damage, coal_mine=coal_mine - coal_mine_damage, iron_mine=iron_mine - iron_mine_damage,
                            lead_mine=lead_mine - lead_mine_damage, bauxite_mine=bauxite_mine - bauxite_mine_damage, oil_derrick=oil_derrick - oil_derrick_damage,
                            uranium_mine=uranium_mine - uranium_mine_damage, farm=farm - farm_damage, aluminium_factory=aluminium_factory - aluminium_factory_damage,
                            steel_factory=steel_factory - steel_factory_damage, oil_refinery=oil_refinery - oil_refinery_damage, ammo_factory=ammo_factory - ammo_factory_damage,
                            concrete_factory=concrete_factory - concrete_factory_damage, militaryfactory=militaryfactory - militaryfactory_damage).where(Infra.name == name).execute()

                        logger.info(f"FOOD CHECK: {name} failed the food check. RIOT DETECTED.\n")

                    else:
                        if happiness <= 0:
                            happiness = 0
                            UserInfo.update(happiness=0).where(UserInfo.user_id == user_id).execute()
                        else:
                            UserInfo.update(happiness=UserInfo.happiness - 15).where(UserInfo.user_id == user_id).execute()

                        adult_deaths = round(adult//24)

                        # Update the pop values.
                        UserStats.update(adult=UserStats.adult - adult_deaths).where(UserStats.name == name).execute()

                        logger.info(f"FOOD CHECK: {name} failed the food check. NO RIOT DETECTED.\n")

                else:
                    growth_multiplier = 1.0
                    if hospital_policy == "Enhanced Healthcare":
                        growth_multiplier += 0.2
                    # Update the population with the growth
                    adult_growth = round(adult//10 * growth_multiplier)
                    new_food = round((food - pop_food_req))

                    # Update the pop values.
                    UserStats.update(adult=UserStats.adult + adult_growth).where(UserStats.name == name).execute()

                    # Update food value.
                    Resources.update(food=Resources.food - new_food).where(Resources.name == name).execute()

                    logger.info(f"FOOD CHECK: {name} passed the food check.\n")

            else:
                logger.info(f"UPDATE ECONOMY ERROR: Error fetching stats of {user_id}.\n")

    except Exception as e:
        logger.info(f'FOOD CHECK ERROR: {e}\n')



async def UpdateMilitary():
    try:
        for row in UserInfo.select(UserInfo.user_id, UserInfo.name, UserInfo.gov_type).tuples():
            user_id, name, gov_type = row

            # fetch user's resources
            res_result = Resources.select(Resources.steel, Resources.gasoline).where(Resources.name == name).tuples().first()

            # fetch user's production infra
            infra_result = Infra.select().where(Infra.name == name).first()

            # fetch user's military stats
            mil_result = UserMil.select(
                UserMil.tank_factory, UserMil.plane_factory, UserMil.artillery_factory, UserMil.anti_air_factory).where(UserMil.name == name).tuples().first()

            if infra_result:
                militaryfactory = infra_result.militaryfactory
                steel, gasoline = res_result
                tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result

                # production multipliers
                base_output = 2.50
                mil_prod_efficiency = 0.5
                if gov_type == "Communism":
                    mil_prod_efficiency = 0.75
                    base_output = 3
                elif gov_type == "Fascism":
                    mil_prod_efficiency = 0.60
                    base_output = 2.75

                # Update Military.
                prod_aa = base_output * anti_air_factory * mil_prod_efficiency
                usage_aa_steel = anti_air_factory * 4
                usage_aa_gas = anti_air_factory * 1
                prod_arty = base_output * artillery_factory * mil_prod_efficiency
                usage_arty_steel = artillery_factory * 3
                usage_arty_gas = artillery_factory * 0.75
                prod_plane = base_output * plane_factory * mil_prod_efficiency
                usage_plane_steel = plane_factory * 5.75
                usage_plane_gas = plane_factory * 2
                prod_tank = base_output * tank_factory * mil_prod_efficiency
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

                    logger.info(f"UPDATE MILITARY: {name} does not have enough resources. Military has not been updated.\n")
                
                else:  # if the user DOES have enough resources.           
                    # Update resources for military.
                    Resources.update(steel=Resources.steel - mil_steel_usage, gasoline=Resources.gasoline - mil_gas_usage).where(Resources.name == name).execute()

                    # Update tank count.
                    UserMil.update(tanks=UserMil.tanks + prod_tank).where(UserMil.name == name).execute()

                    # Update plane count.
                    UserMil.update(planes=UserMil.planes + prod_plane).where(UserMil.name == name).execute()

                    # Update artillery count.
                    UserMil.update(artillery=UserMil.artillery + prod_arty).where(UserMil.name == name).execute()

                    # Update Anti-Air.
                    UserMil.update(anti_air=UserMil.anti_air + prod_aa).where(UserMil.name == name).execute()

                    logger.info(f"UPDATE MILITARY: {name}'s military has been updated.\n")

            else:
                logger.info(f"UPDATE ECONOMY ERROR: Error fetching stats of {user_id}.\n")

    except Exception as e:
        logger.info(f'UPDATE MILITARY ERROR: {e}\n')


async def HappinessCalculator():
    try:
        for row in UserInfo.select(UserInfo.user_id, UserInfo.name, UserInfo.happiness).tuples():
            user_id, name, happiness = row

            # fetch user's production infra
            infra_result = Infra.select(Infra.park, Infra.cinema, Infra.museum, Infra.concert_hall).where(Infra.name == name).tuples().first()

            if infra_result:
                park, cinema, museum, concert_hall = infra_result

                if happiness > 50:
                    return
                else:
                    # Calculate total happiness bonus
                    happiness_bonus = round(park * 0.07 + cinema * 0.08 + museum * 0.06 + concert_hall * 0.1)

                    # Log the happiness bonus
                    logger.info(f"HappinessCalculator: {name} has a happiness bonus of {happiness_bonus} per hour from entertainment buildings.\n")

                    # You can also update the user's happiness in the database if needed
                    UserInfo.update(happiness=UserInfo.happiness + happiness_bonus).where(UserInfo.user_id == user_id).execute()

                    return happiness_bonus

            else:
                logger.info(f'HappinessCalculator ERROR: could not find infra stats for {name}.\n')

    except Exception as e:
        logger.info(f'HappinessCalculator ERROR: {e}\n')


async def GDPCalculator():
    try:
        for row in UserInfo.select(
            UserInfo.user_id, UserInfo.name, UserInfo.gov_type, UserInfo.tax_rate, UserInfo.war_status, UserInfo.corp_tax).tuples():
            user_id, name, gov_type, tax_rate, war_status, corp_tax = row

            # fetch user's production infra
            infra_result = Infra.select().where(Infra.name == name).tuples().first()

            # fetch user's military stats
            mil_result = UserMil.select().where(UserMil.name == name).tuples().first()

            # fetch user's population stats.
            pop_result = UserStats.select().where(UserStats.name == name).first()

            if infra_result:
                name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps, park, cinema, museum, concert_hall = infra_result
                name, troops, planes, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result
                adult = pop_result.adult

                # Calculating effects for different parts of update
                tax_revenue_bonus = 1
                upkeep_bonus = 1
                troops_upkeep_bonus = 1
                production_bonus = 1

                match gov_type:
                    case "Anarchy":
                        tax_revenue_bonus *= 0
                    case "Communism":
                        tax_revenue_bonus *= 0.5
                        upkeep_bonus *= 0.8
                        production_bonus *= 2
                    case "Democracy":
                        tax_revenue_bonus *= 1.2
                        upkeep_bonus *= 1.2
                    case "Fascism":
                        tax_revenue_bonus *= 0.9
                        upkeep_bonus *= 1.5
                        troops_upkeep_bonus *= 0.5
                    case "Monarchy":
                        tax_revenue_bonus *= 1.1
                        upkeep_bonus *= 1.1
                    case "Socialism":
                        tax_revenue_bonus *= 0.6
                        upkeep_bonus *= 0.9

                # The production of each resource
                prod_wood = lumber_mill * 2 * production_bonus
                prod_coal = coal_mine * 1.2 * production_bonus
                prod_iron = iron_mine * 1 * production_bonus
                prod_lead = lead_mine * 0.8 * production_bonus
                prod_bauxite = bauxite_mine * 0.6 * production_bonus
                prod_oil = oil_derrick * 1 * production_bonus
                prod_uranium = uranium_mine * 0.05 * production_bonus
                prod_farm = farm * 10 * production_bonus
                prod_aluminium = aluminium_factory * 0.4 * production_bonus
                prod_steel = steel_factory * 0.3 * production_bonus
                prod_gas = oil_refinery * 0.2 * production_bonus
                prod_ammo = ammo_factory * 0.5 * production_bonus
                prod_concrete = concrete_factory * 0.6 * production_bonus

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

                total_resource_prod = prod_wood + prod_coal + prod_ammo + prod_aluminium + prod_concrete \
                                            + prod_farm + prod_gas + prod_steel + final_prod_bauxite + final_prod_iron \
                                            + final_prod_lead + final_prod_oil

                NAI = NAI_Determiner(user_id)
                tax_revenue = round(tax_rate * (NAI * adult) * tax_revenue_bonus)

                basic_house_upkeep = basic_house * 20
                small_flat_upkeep = small_flat * 40
                apt_complex_upkeep = apt_complex * 60
                skyscraper_upkeep = skyscraper * 100

                lumber_mill_upkeep = lumber_mill * 100
                coal_mine_upkeep = coal_mine * 150
                iron_mine_upkeep = iron_mine * 200
                lead_mine_upkeep = lead_mine * 250
                bauxite_mine_upkeep = bauxite_mine * 300
                oil_derrick_upkeep = oil_derrick * 400
                uranium_mine_upkeep = uranium_mine * 600

                farm_upkeep = farm * 100 * 1

                aluminium_factory_upkeep = aluminium_factory * 400
                steel_factory_upkeep = steel_factory * 500 * 1
                oil_refinery_upkeep = oil_refinery * 600 * 1
                ammo_factory_upkeep = ammo_factory * 700 * 1
                concrete_factory_upkeep = concrete_factory * 600
                militaryfactory_upkeep = militaryfactory * 800

                park_upkeep = park * 30
                cinema_upkeep = cinema * 60
                museum_upkeep = museum * 70
                concert_hall_upkeep = concert_hall * 120

                infra_upkeep = (basic_house_upkeep + small_flat_upkeep + apt_complex_upkeep + skyscraper_upkeep +
                                lumber_mill_upkeep + coal_mine_upkeep + iron_mine_upkeep + lead_mine_upkeep +
                                bauxite_mine_upkeep + oil_derrick_upkeep + uranium_mine_upkeep +
                                farm_upkeep + aluminium_factory_upkeep + steel_factory_upkeep +
                                oil_refinery_upkeep + ammo_factory_upkeep + concrete_factory_upkeep +
                                militaryfactory_upkeep + park_upkeep + cinema_upkeep + museum_upkeep + concert_hall_upkeep) * upkeep_bonus

                corp_income = round(corps * corp_tax)

                if war_status == "In Peace":
                    troops_upkeep = troops * 5
                    planes_upkeep = planes * 50
                    tanks_upkeep = tanks * 100
                    artillery_upkeep = artillery * 150
                    anti_air_upkeep = anti_air * 200
                    barracks_upkeep = barracks * 200
                    tank_factory_upkeep = tank_factory * 300
                    plane_factory_upkeep = plane_factory * 400
                    artillery_factory_upkeep = artillery_factory * 450
                    anti_air_factory_upkeep = anti_air_factory * 500

                    military_upkeep = (troops_upkeep + planes_upkeep + tanks_upkeep +
                                        artillery_upkeep + anti_air_upkeep + barracks_upkeep +
                                        tank_factory_upkeep + plane_factory_upkeep +
                                        artillery_factory_upkeep + anti_air_factory_upkeep)

                else:
                    troops_upkeep = troops * 5 * 1.5
                    planes_upkeep = planes * 50 * 1.5
                    tanks_upkeep = tanks * 100 * 1.5
                    artillery_upkeep = artillery * 150 * 1.5
                    anti_air_upkeep = anti_air * 200 * 1.5
                    barracks_upkeep = barracks * 200 * 1.5
                    tank_factory_upkeep = tank_factory * 300 * 1.5
                    plane_factory_upkeep = plane_factory * 400 * 1.5
                    artillery_factory_upkeep = artillery_factory * 450 * 1.5
                    anti_air_factory_upkeep = anti_air_factory * 500 * 1.5

                    military_upkeep = (troops_upkeep + planes_upkeep + tanks_upkeep +
                                       artillery_upkeep + anti_air_upkeep + barracks_upkeep +
                                       tank_factory_upkeep + plane_factory_upkeep +
                                       artillery_factory_upkeep + anti_air_factory_upkeep) * troops_upkeep_bonus

                new_gdp = round((total_resource_prod + tax_revenue + corp_income) - (infra_upkeep + military_upkeep))
                UserStats.update(gdp=new_gdp).where(UserStats.name == name).execute()

                logger.info(f'GDPCalculator: successfully updated GDP for {name}.\n')

            else:
                logger.info(f'GDPCalculator ERROR: could not find stats for {name}.\n')


    except Exception as e:
        logger.info(f'GPDCalulator ERROR: {e}\n')


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

@tasks.loop(seconds=3600)
async def HappinessCalculatorTask():
    await HappinessCalculator()

@tasks.loop(seconds=3600)
async def GDPCalculatorTask():
    await GDPCalculator()

@tasks.loop(seconds=3600)
async def SpawnCorps():
    for row in UserInfo.select(UserInfo.user_id):
        Corp_spawn(row.user_id)

@tasks.loop(seconds=3600)
async def RemoveCorps():
    for row in UserInfo.select(UserInfo.user_id):
        Corp_remove(row.user_id)

@tasks.loop(seconds=3600)
async def NAICalculator():
    for row in UserInfo.select(UserInfo.user_id):
        NAI_Determiner(row.user_id)

GDPCalculatorTask.start()
HappinessCalculatorTask.start()
NAICalculator.start()
RemoveCorps.start()
SpawnCorps.start()
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
        embed = discord.Embed(colour=0xEA76CB, title="Invalid Command", type='rich',
                              description=f"This is no longer a command. {new_line}It is done automatically for you :)")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Update(bot))
