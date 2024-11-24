import sqlite3
import logging
import globals

logging_folder = globals.logging_folder + 'sim_logs.log'

logging.basicConfig(filename=logging_folder, level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    force=True)

logger = logging.getLogger(__name__)

# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = globals.conn
cursor = globals.cursor

def NAI_Determiner(user_id):
    global NAI
    cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness, corp_tax = user_data

        # Fetch user's production infra
        cursor.execute(
            'SELECT basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps FROM infra WHERE name = ?',
            (name,))
        infra_result = cursor.fetchone()

        # Fetch user's military stats
        cursor.execute(
            'SELECT * FROM user_mil WHERE name = ?',
            (name,))
        mil_result = cursor.fetchone()

        # Fetch user's population stats.
        cursor.execute(
            'SELECT nation_score, gdp, adult, balance FROM user_stats WHERE name = ?',
            (name,))
        pop_result = cursor.fetchone()

        if infra_result:
            basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps = infra_result
            name, troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result
            nation_score, gdp, adult, balance = pop_result

            # Constants
            MINER_SALARY = 1200
            FACTORY_WORKER_SALARY = 1000
            CORP_WORKER_SALARY = 2300

            # Calculate income from mines and mills
            mines_income = (coal_mine + lead_mine + iron_mine + uranium_mine + bauxite_mine) * MINER_SALARY
            mills_income = (lumber_mill + farm + oil_derrick) * MINER_SALARY

            # Calculate income from factories
            factories_income = (steel_factory + ammo_factory + aluminium_factory + concrete_factory) * FACTORY_WORKER_SALARY

            # Calculate income from corps
            corp_income = corps * CORP_WORKER_SALARY

            # Calculate National Average Income (NAI)
            total_income = mines_income + mills_income + factories_income + corp_income

            # For NAI, divide by the number of workers.
            num_miners = round(coal_mine + lead_mine + iron_mine + uranium_mine + bauxite_mine // 5)
            num_mill_workers = round(lumber_mill + farm + oil_derrick // 2.33)
            steel_workers = round(steel_factory // 8)
            aluminium_workers = round(aluminium_factory // 6)
            gas_workers = round(oil_refinery // 4)
            ammo_workers = round(ammo_factory // 10)
            concrete_workers = round(concrete_factory // 5)
            corp_workers = round(corps // 5500)

            total_workers = (num_miners + num_mill_workers + steel_workers + aluminium_workers + gas_workers + ammo_workers
                             + concrete_workers + corp_workers)

            NAI = round(total_income // total_workers)

            return NAI

        else:
            logger.info(f"NAI_Determiner ERROR: COULD NOT FIND STATS FOR {name}.\n")

    else:
        logger.info(f"NAI_Determiner ERROR: COULD NOT FIND {user_id}.\n")
