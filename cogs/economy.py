import sqlite3
import discord
from discord.ext import commands

new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = sqlite3.connect('player_info.db')
cursor = conn.cursor()


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='eco')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def economy(self, ctx):
        user_id = ctx.author.id

        # fetch user nation_name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, nation_name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            # fetch user's resources
            cursor.execute(
                'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                (nation_name,))
            res_result = cursor.fetchone()

            # fetch user's production infra
            cursor.execute(
                'SELECT name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory FROM infra WHERE name = ?',
                (nation_name,))
            infra_result = cursor.fetchone()

            # fetch user's military stats
            cursor.execute(
                'SELECT name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory FROM user_mil WHERE name_nation = ?',
                (nation_name,))
            mil_result = cursor.fetchone()

            # fetch user's population stats.
            cursor.execute(
                'SELECT name, nation_score, gdp, adult, balance FROM user_stats WHERE name = ?',
                (nation_name,))
            pop_result = cursor.fetchone()


            if infra_result and res_result:
                name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory = infra_result
                name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result
                name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result
                name, nation_score, gdp, adult, balance = pop_result

                if gov_type == "Communism":
                    # The production of each resource
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

                    resource_revenue = wood_income + coal_income + iron_income + lead_income + bauxite_income + oil_income + uranium_income + food_income + aluminium_income + steel_income + gas_income + ammo_income + concrete_income

                    total_pop = adult
                    tax_revenue = round((tax_rate * total_pop) * 0.50)

                    basic_house_upkeep = basic_house * 10 * 0.8
                    small_flat_upkeep = small_flat * 20 * 0.8
                    apt_complex_upkeep = apt_complex * 30 * 0.8
                    skyscraper_upkeep = skyscraper * 50 * 0.8

                    lumber_mill_upkeep = lumber_mill * 50 * 0.8
                    coal_mine_upkeep = coal_mine * 75 * 0.8
                    iron_mine_upkeep = iron_mine * 100 * 0.8
                    lead_mine_upkeep = lead_mine * 125 * 0.8
                    bauxite_mine_upkeep = bauxite_mine * 150 * 0.8
                    oil_derrick_upkeep = oil_derrick * 200 * 0.8
                    uranium_mine_upkeep = uranium_mine * 300 * 0.8

                    farm_upkeep = farm * 50 * 0.8

                    aluminium_factory_upkeep = aluminium_factory * 200 * 0.8
                    steel_factory_upkeep = steel_factory * 250 * 0.8
                    oil_refinery_upkeep = oil_refinery * 300 * 0.8
                    ammo_factory_upkeep = ammo_factory * 350 * 0.8
                    concrete_factory_upkeep = concrete_factory * 300 * 0.8
                    militaryfactory_upkeep = militaryfactory * 400 * 0.8

                    infra_upkeep = (basic_house_upkeep + small_flat_upkeep + apt_complex_upkeep + skyscraper_upkeep +
                    lumber_mill_upkeep + coal_mine_upkeep + iron_mine_upkeep + lead_mine_upkeep +
                    bauxite_mine_upkeep + oil_derrick_upkeep + uranium_mine_upkeep +
                    farm_upkeep + aluminium_factory_upkeep + steel_factory_upkeep +
                    oil_refinery_upkeep + ammo_factory_upkeep + concrete_factory_upkeep +
                    militaryfactory_upkeep)

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

                        net_income = round((tax_revenue + resource_revenue) - (infra_upkeep + military_upkeep + policy_upkeep))

                        embed = discord.Embed(title="Economy", type='rich',
                                            description=f"Displays {nation_name}'s economy.", color=discord.Color.green())
                        embed.add_field(name="Overview", value=f"Tax Revenue: {tax_revenue:,}{new_line}"
                                                            f"Resource Revenue: {resource_revenue:,}{new_line}"
                                                            f"Infrastructure Upkeep: {infra_upkeep:,}{new_line}"
                                                            f"Military Upkeep: {military_upkeep:,}{new_line}"
                                                            f"Policy Upkeep: {policy_upkeep:,}{new_line}", inline=False)
                        embed.add_field(name="", value=f"Net Income: {net_income:,}", inline=False)
                        await ctx.send(embed=embed)

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

                        net_income = round((tax_revenue + resource_revenue) - (infra_upkeep + military_upkeep + policy_upkeep))

                        embed = discord.Embed(title="Economy", type='rich',
                                            description=f"Displays {nation_name}'s economy.", color=discord.Color.green())
                        embed.add_field(name="Overview", value=f"Tax Revenue: {tax_revenue:,}{new_line}"
                                                            f"Resource Revenue: {resource_revenue:,}{new_line}"
                                                            f"Infrastructure Upkeep: {infra_upkeep:,}{new_line}"
                                                            f"Military Upkeep: {military_upkeep:,}{new_line}"
                                                            f"Policy Upkeep: {policy_upkeep:,}{new_line}", inline=False)
                        embed.add_field(name="", value=f"Net Income: {net_income}", inline=False)
                        await ctx.send(embed=embed)

                elif gov_type == "Democracy":
                    # The production of each resource
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
                    usage_oil_gas = prod_gas
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
                    tax_revenue = round((tax_rate * total_pop) * 1.2)

                    basic_house_upkeep = basic_house * 10 * 1.2
                    small_flat_upkeep = small_flat * 20 * 1.2
                    apt_complex_upkeep = apt_complex * 30 * 1.2
                    skyscraper_upkeep = skyscraper * 50 * 1.2

                    lumber_mill_upkeep = lumber_mill * 50 * 1.2
                    coal_mine_upkeep = coal_mine * 75 * 1.2
                    iron_mine_upkeep = iron_mine * 100 * 1.2
                    lead_mine_upkeep = lead_mine * 125 * 1.2
                    bauxite_mine_upkeep = bauxite_mine * 150 * 1.2
                    oil_derrick_upkeep = oil_derrick * 200 * 1.2
                    uranium_mine_upkeep = uranium_mine * 300 * 1.2

                    farm_upkeep = farm * 50 * 1.2

                    aluminium_factory_upkeep = aluminium_factory * 200 * 1.2
                    steel_factory_upkeep = steel_factory * 250 * 1.2
                    oil_refinery_upkeep = oil_refinery * 300 * 1.2
                    ammo_factory_upkeep = ammo_factory * 350 * 1.2
                    concrete_factory_upkeep = concrete_factory * 300 * 1.2
                    militaryfactory_upkeep = militaryfactory * 400 * 1.2

                    infra_upkeep = (basic_house_upkeep + small_flat_upkeep + apt_complex_upkeep + skyscraper_upkeep +
                    lumber_mill_upkeep + coal_mine_upkeep + iron_mine_upkeep + lead_mine_upkeep +
                    bauxite_mine_upkeep + oil_derrick_upkeep + uranium_mine_upkeep +
                    farm_upkeep + aluminium_factory_upkeep + steel_factory_upkeep +
                    oil_refinery_upkeep + ammo_factory_upkeep + concrete_factory_upkeep +
                    militaryfactory_upkeep)

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

                        embed = discord.Embed(title="Economy", type='rich',
                                            description=f"Displays {nation_name}'s economy.", color=discord.Color.green())
                        embed.add_field(name="Overview", value=f"Tax Revenue: {tax_revenue:,}{new_line}"
                                                            f"Resource Revenue: {resource_revenue:,}{new_line}"
                                                            f"Infrastructure Upkeep: {infra_upkeep:,}{new_line}"
                                                            f"Military Upkeep: {military_upkeep:,}{new_line}"
                                                            f"Policy Upkeep: {policy_upkeep:,}{new_line}", inline=False)
                        embed.add_field(name="", value=f"Net Income: {net_income:,}", inline=False)
                        await ctx.send(embed=embed)

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

                        embed = discord.Embed(title="Economy", type='rich',
                                            description=f"Displays {nation_name}'s economy.", color=discord.Color.green())
                        embed.add_field(name="Overview", value=f"Tax Revenue: {tax_revenue:,}{new_line}"
                                                            f"Resource Revenue: {resource_revenue:,}{new_line}"
                                                            f"Infrastructure Upkeep: {infra_upkeep:,}{new_line}"
                                                            f"Military Upkeep: {military_upkeep:,}{new_line}"
                                                            f"Policy Upkeep: {policy_upkeep:,}{new_line}", inline=False)
                        embed.add_field(name="", value=f"Net Income: {net_income}", inline=False)
                        await ctx.send(embed=embed)


                elif gov_type == "Monarchy":
                    # The production of each resource
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
                    usage_oil_gas = prod_gas
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
                    tax_revenue = round((tax_rate * total_pop) * 1.1)

                    basic_house_upkeep = basic_house * 10 * 1.1
                    small_flat_upkeep = small_flat * 20 * 1.1
                    apt_complex_upkeep = apt_complex * 30 * 1.1
                    skyscraper_upkeep = skyscraper * 50 * 1.1

                    lumber_mill_upkeep = lumber_mill * 50 * 1.1
                    coal_mine_upkeep = coal_mine * 75 * 1.1
                    iron_mine_upkeep = iron_mine * 100 * 1.1
                    lead_mine_upkeep = lead_mine * 125 * 1.1
                    bauxite_mine_upkeep = bauxite_mine * 150 * 1.1
                    oil_derrick_upkeep = oil_derrick * 200 * 1.1
                    uranium_mine_upkeep = uranium_mine * 300 * 1.1

                    farm_upkeep = farm * 50 * 1.1

                    aluminium_factory_upkeep = aluminium_factory * 200 * 1.1
                    steel_factory_upkeep = steel_factory * 250 * 1.1
                    oil_refinery_upkeep = oil_refinery * 300 * 1.1
                    ammo_factory_upkeep = ammo_factory * 350 * 1.1
                    concrete_factory_upkeep = concrete_factory * 300 * 1.1
                    militaryfactory_upkeep = militaryfactory * 400 * 1.1

                    infra_upkeep = (basic_house_upkeep + small_flat_upkeep + apt_complex_upkeep + skyscraper_upkeep +
                    lumber_mill_upkeep + coal_mine_upkeep + iron_mine_upkeep + lead_mine_upkeep +
                    bauxite_mine_upkeep + oil_derrick_upkeep + uranium_mine_upkeep +
                    farm_upkeep + aluminium_factory_upkeep + steel_factory_upkeep +
                    oil_refinery_upkeep + ammo_factory_upkeep + concrete_factory_upkeep +
                    militaryfactory_upkeep)

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

                        embed = discord.Embed(title="Economy", type='rich',
                                            description=f"Displays {nation_name}'s economy.", color=discord.Color.green())
                        embed.add_field(name="Overview", value=f"Tax Revenue: {tax_revenue:,}{new_line}"
                                                            f"Resource Revenue: {resource_revenue:,}{new_line}"
                                                            f"Infrastructure Upkeep: {infra_upkeep:,}{new_line}"
                                                            f"Military Upkeep: {military_upkeep:,}{new_line}"
                                                            f"Policy Upkeep: {policy_upkeep:,}{new_line}", inline=False)
                        embed.add_field(name="", value=f"Net Income: {net_income:,}", inline=False)
                        await ctx.send(embed=embed)

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

                        embed = discord.Embed(title="Economy", type='rich',
                                            description=f"Displays {nation_name}'s economy.", color=discord.Color.green())
                        embed.add_field(name="Overview", value=f"Tax Revenue: {tax_revenue:,}{new_line}"
                                                            f"Resource Revenue: {resource_revenue:,}{new_line}"
                                                            f"Infrastructure Upkeep: {infra_upkeep:,}{new_line}"
                                                            f"Military Upkeep: {military_upkeep:,}{new_line}"
                                                            f"Policy Upkeep: {policy_upkeep:,}{new_line}", inline=False)
                        embed.add_field(name="", value=f"Net Income: {net_income}", inline=False)
                        await ctx.send(embed=embed)

                elif gov_type == "Fascism":
                    # The production of each resource
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
                    usage_oil_gas = prod_gas
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
                    tax_revenue = round((tax_rate * total_pop) * 0.9)

                    basic_house_upkeep = basic_house * 10 * 1.5
                    small_flat_upkeep = small_flat * 20 * 1.5
                    apt_complex_upkeep = apt_complex * 30 * 1.5
                    skyscraper_upkeep = skyscraper * 50 * 1.5

                    lumber_mill_upkeep = lumber_mill * 50 * 1.5
                    coal_mine_upkeep = coal_mine * 75 * 1.5
                    iron_mine_upkeep = iron_mine * 100 * 1.5
                    lead_mine_upkeep = lead_mine * 125 * 1.5
                    bauxite_mine_upkeep = bauxite_mine * 150 * 1.5
                    oil_derrick_upkeep = oil_derrick * 200 * 1.5
                    uranium_mine_upkeep = uranium_mine * 300 * 1.5

                    farm_upkeep = farm * 50 * 1.5

                    aluminium_factory_upkeep = aluminium_factory * 200 * 1.5
                    steel_factory_upkeep = steel_factory * 250 * 1.5
                    oil_refinery_upkeep = oil_refinery * 300 * 1.5
                    ammo_factory_upkeep = ammo_factory * 350 * 1.5
                    concrete_factory_upkeep = concrete_factory * 300 * 1.5
                    militaryfactory_upkeep = militaryfactory * 400 * 1.5

                    infra_upkeep = (basic_house_upkeep + small_flat_upkeep + apt_complex_upkeep + skyscraper_upkeep +
                    lumber_mill_upkeep + coal_mine_upkeep + iron_mine_upkeep + lead_mine_upkeep +
                    bauxite_mine_upkeep + oil_derrick_upkeep + uranium_mine_upkeep +
                    farm_upkeep + aluminium_factory_upkeep + steel_factory_upkeep +
                    oil_refinery_upkeep + ammo_factory_upkeep + concrete_factory_upkeep +
                    militaryfactory_upkeep)

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

                        embed = discord.Embed(title="Economy", type='rich',
                                            description=f"Displays {nation_name}'s economy.", color=discord.Color.green())
                        embed.add_field(name="Overview", value=f"Tax Revenue: {tax_revenue:,}{new_line}"
                                                            f"Resource Revenue: {resource_revenue:,}{new_line}"
                                                            f"Infrastructure Upkeep: {infra_upkeep:,}{new_line}"
                                                            f"Military Upkeep: {military_upkeep:,}{new_line}"
                                                            f"Policy Upkeep: {policy_upkeep:,}{new_line}", inline=False)
                        embed.add_field(name="", value=f"Net Income: {net_income:,}", inline=False)
                        await ctx.send(embed=embed)

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

                        embed = discord.Embed(title="Economy", type='rich',
                                            description=f"Displays {nation_name}'s economy.", color=discord.Color.green())
                        embed.add_field(name="Overview", value=f"Tax Revenue: {tax_revenue:,}{new_line}"
                                                            f"Resource Revenue: {resource_revenue:,}{new_line}"
                                                            f"Infrastructure Upkeep: {infra_upkeep:,}{new_line}"
                                                            f"Military Upkeep: {military_upkeep:,}{new_line}"
                                                            f"Policy Upkeep: {policy_upkeep:,}{new_line}", inline=False)
                        embed.add_field(name="", value=f"Net Income: {net_income}", inline=False)
                        await ctx.send(embed=embed)

                elif gov_type == "Socialism":
                    # The production of each resource
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
                    usage_oil_gas = prod_gas
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
                    tax_revenue = round((tax_rate * total_pop) * 0.6)

                    basic_house_upkeep = basic_house * 10 * 0.9
                    small_flat_upkeep = small_flat * 20 * 0.9
                    apt_complex_upkeep = apt_complex * 30 * 0.9
                    skyscraper_upkeep = skyscraper * 50 * 0.9

                    lumber_mill_upkeep = lumber_mill * 50 * 0.9
                    coal_mine_upkeep = coal_mine * 75 * 0.9
                    iron_mine_upkeep = iron_mine * 100 * 0.9
                    lead_mine_upkeep = lead_mine * 125 * 0.9
                    bauxite_mine_upkeep = bauxite_mine * 150 * 0.9
                    oil_derrick_upkeep = oil_derrick * 200 * 0.9
                    uranium_mine_upkeep = uranium_mine * 300 * 0.9

                    farm_upkeep = farm * 50 * 0.9

                    aluminium_factory_upkeep = aluminium_factory * 200 * 0.9
                    steel_factory_upkeep = steel_factory * 250 * 0.9
                    oil_refinery_upkeep = oil_refinery * 300 * 0.9
                    ammo_factory_upkeep = ammo_factory * 350 * 0.9
                    concrete_factory_upkeep = concrete_factory * 300 * 0.9
                    militaryfactory_upkeep = militaryfactory * 400 * 0.9

                    infra_upkeep = (basic_house_upkeep + small_flat_upkeep + apt_complex_upkeep + skyscraper_upkeep +
                    lumber_mill_upkeep + coal_mine_upkeep + iron_mine_upkeep + lead_mine_upkeep +
                    bauxite_mine_upkeep + oil_derrick_upkeep + uranium_mine_upkeep +
                    farm_upkeep + aluminium_factory_upkeep + steel_factory_upkeep +
                    oil_refinery_upkeep + ammo_factory_upkeep + concrete_factory_upkeep +
                    militaryfactory_upkeep)

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

                        embed = discord.Embed(title="Economy", type='rich',
                                            description=f"Displays {nation_name}'s economy.", color=discord.Color.green())
                        embed.add_field(name="Overview", value=f"Tax Revenue: {tax_revenue:,}{new_line}"
                                                            f"Resource Revenue: {resource_revenue:,}{new_line}"
                                                            f"Infrastructure Upkeep: {infra_upkeep:,}{new_line}"
                                                            f"Military Upkeep: {military_upkeep:,}{new_line}"
                                                            f"Policy Upkeep: {policy_upkeep:,}{new_line}", inline=False)
                        embed.add_field(name="", value=f"Net Income: {net_income:,}", inline=False)
                        await ctx.send(embed=embed)

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

                        embed = discord.Embed(title="Economy", type='rich',
                                            description=f"Displays {nation_name}'s economy.", color=discord.Color.green())
                        embed.add_field(name="Overview", value=f"Tax Revenue: {tax_revenue:,}{new_line}"
                                                            f"Resource Revenue: {resource_revenue:,}{new_line}"
                                                            f"Infrastructure Upkeep: {infra_upkeep:,}{new_line}"
                                                            f"Military Upkeep: {military_upkeep:,}{new_line}"
                                                            f"Policy Upkeep: {policy_upkeep:,}{new_line}", inline=False)
                        embed.add_field(name="", value=f"Net Income: {net_income}", inline=False)
                        await ctx.send(embed=embed)

                elif gov_type == "Anarchy":
                    # The production of each resource
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
                    usage_oil_gas = prod_gas
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
                    tax_revenue = round((tax_rate * total_pop) * 0)

                    basic_house_upkeep = basic_house * 10 * 1
                    small_flat_upkeep = small_flat * 20 * 1
                    apt_complex_upkeep = apt_complex * 30 * 1
                    skyscraper_upkeep = skyscraper * 50 * 1

                    lumber_mill_upkeep = lumber_mill * 50 * 1
                    coal_mine_upkeep = coal_mine * 75 * 1
                    iron_mine_upkeep = iron_mine * 100 * 1
                    lead_mine_upkeep = lead_mine * 125 * 1
                    bauxite_mine_upkeep = bauxite_mine * 150 * 1
                    oil_derrick_upkeep = oil_derrick * 200 * 1
                    uranium_mine_upkeep = uranium_mine * 300 * 1

                    farm_upkeep = farm * 50 * 1

                    aluminium_factory_upkeep = aluminium_factory * 200 * 1
                    steel_factory_upkeep = steel_factory * 250 * 1
                    oil_refinery_upkeep = oil_refinery * 300 * 1
                    ammo_factory_upkeep = ammo_factory * 350 * 1
                    concrete_factory_upkeep = concrete_factory * 300 * 1
                    militaryfactory_upkeep = militaryfactory * 400 * 1

                    infra_upkeep = (basic_house_upkeep + small_flat_upkeep + apt_complex_upkeep + skyscraper_upkeep +
                    lumber_mill_upkeep + coal_mine_upkeep + iron_mine_upkeep + lead_mine_upkeep +
                    bauxite_mine_upkeep + oil_derrick_upkeep + uranium_mine_upkeep +
                    farm_upkeep + aluminium_factory_upkeep + steel_factory_upkeep +
                    oil_refinery_upkeep + ammo_factory_upkeep + concrete_factory_upkeep +
                    militaryfactory_upkeep)

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

                        embed = discord.Embed(title="Economy", type='rich',
                                            description=f"Displays {nation_name}'s economy.", color=discord.Color.green())
                        embed.add_field(name="Overview", value=f"Tax Revenue: {tax_revenue:,}{new_line}"
                                                            f"Resource Revenue: {resource_revenue:,}{new_line}"
                                                            f"Infrastructure Upkeep: {infra_upkeep:,}{new_line}"
                                                            f"Military Upkeep: {military_upkeep:,}{new_line}"
                                                            f"Policy Upkeep: {policy_upkeep:,}{new_line}", inline=False)
                        embed.add_field(name="", value=f"Net Income: {net_income:,}", inline=False)
                        await ctx.send(embed=embed)

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

                        embed = discord.Embed(title="Economy", type='rich',
                                            description=f"Displays {nation_name}'s economy.", color=discord.Color.green())
                        embed.add_field(name="Overview", value=f"Tax Revenue: {tax_revenue:,}{new_line}"
                                                            f"Resource Revenue: {resource_revenue:,}{new_line}"
                                                            f"Infrastructure Upkeep: {infra_upkeep:,}{new_line}"
                                                            f"Military Upkeep: {military_upkeep:,}{new_line}"
                                                            f"Policy Upkeep: {policy_upkeep:,}{new_line}", inline=False)
                        embed.add_field(name="", value=f"Net Income: {net_income}", inline=False)
                        await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                            description=f'Cannot find `gov_type`, Please ping a dev.')
                    await ctx.send(embed=embed)

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
    await bot.add_cog(Economy(bot))