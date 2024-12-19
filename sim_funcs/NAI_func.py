import sqlite3
import logging
import globals
from schema import *

logging_folder = globals.logging_folder + 'sim_logs.log'

logging.basicConfig(filename=logging_folder, level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    force=True)

logger = logging.getLogger(__name__)


def NAI_Determiner(user_id):
    user_data = UserInfo.select().where(UserInfo.user_id == user_id).tuples().first()

    if user_data:
        user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness, corp_tax = user_data

        # Fetch user's production infra
        infra_result = Infra.select(
            Infra.basic_house, Infra.small_flat, Infra.apt_complex,
            Infra.skyscraper, Infra.lumber_mill, Infra.coal_mine,
            Infra.iron_mine, Infra.lead_mine, Infra.bauxite_mine,
            Infra.oil_derrick, Infra.uranium_mine, Infra.farm,
            Infra.aluminium_factory, Infra.steel_factory, Infra.oil_refinery,
            Infra.ammo_factory, Infra.concrete_factory, Infra.militaryfactory,
            Infra.corps).where(Infra.name == name).tuples().first()

        # Fetch user's military stats
        mil_result = UserMil.select().where(UserMil.name == name).tuples().first()

        # Fetch user's population stats.
        pop_result = UserStats.select(
            UserStats.nation_score, UserStats.gdp, UserStats.adult, UserStats.balance).where(UserStats.name == name).tuples().first()

        if infra_result and mil_result and pop_result:
            basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps = infra_result
            name, troops, planes, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result
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
