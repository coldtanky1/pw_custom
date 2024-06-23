import sqlite3
import logging
import random
import globals

logging_folder = globals.logging_folder + 'sim_logs.log'

logging.basicConfig(filename=logging_folder, level=logging.INFO,
                    format='%(asctime)s %(message)s')

logger = logging.getLogger(__name__)

# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = globals.conn
cursor = globals.cursor


def Corp_spawn(user_id):
    cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness, corp_tax = user_data

        # Fetch user's production infra
        cursor.execute(
            'SELECT name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps FROM infra WHERE name = ?',
            (name,))
        infra_result = cursor.fetchone()

        if infra_result:
            name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps = infra_result

            if random.randint(1, 30) == 1:
                spawn_amount = random.randint(1, 5)
                cursor.execute('UPDATE infra SET corps = corps + ? WHERE name = ?', (spawn_amount, name))
                conn.commit()
                
                logger.info(f"Corp_spawn: {name} has gotten {spawn_amount} of corps.")

            else:
                logger.info(f'Corp_spawn: {name} has NOT gotten any corps.')
            
        else:
            logger.info(f"Corp_spawn ERROR: COULD NOT FIND STATS FOR {name}.\n")

    else:
        logger.info(f"Corp_spawn ERROR: COULD NOT FIND {user_id}.\n")

def Corp_remove(user_id):
    cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        user_id, name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness, corp_tax = user_data

        # Fetch user's production infra
        cursor.execute(
            'SELECT name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps FROM infra WHERE name = ?',
            (name,))
        infra_result = cursor.fetchone()

        if infra_result:
            name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory, corps = infra_result
