import sqlite3
import logging
import random
import globals

logging_folder = globals.logging_folder + 'sim_logs.log'

logging.basicConfig(filename=logging_folder, level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    force=True)

logger = logging.getLogger(__name__)

# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = globals.conn
cursor = globals.cursor


def Corp_spawn(user_id):
    cursor.execute('SELECT name, corp_tax FROM user_info WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        name, corp_tax = user_data

        # Fetch user's production infra
        cursor.execute('SELECT corps FROM infra WHERE name = ?', (name,))
        infra_result = cursor.fetchone()

        if infra_result:
            corps = infra_result[0]  # unpack the result

            corp_tax *= 100  # turn it from a percentage.
            difference = corp_tax - 15  # 15% is the default corp tax.

            if difference < 0:
                spawn_probability = abs(difference)
                spawn_amount = 0

                # Calculate the number of corporations to spawn
                for _ in range(5):  # Attempt up to 5 spawns
                    if random.uniform(0, 100) < spawn_probability:
                        spawn_amount += 1

                if spawn_amount > 0:
                    cursor.execute('UPDATE infra SET corps = corps + ? WHERE name = ?', (spawn_amount, name))
                    conn.commit()

                    # Workers being employed from a corporation spawning.
                    cursor.execute('UPDATE user_stats SET adult = adult - ? WHERE name = ?', (spawn_amount * 575, name))
                    conn.commit()

                    logger.info(f"Corp_spawn: {name} has gotten {spawn_amount} corps.")
                else:
                    logger.info(f'Corp_spawn: {name} has NOT gotten any corps.')

            elif difference == 0:
                # Always spawn at least one corporation if the tax rate is exactly 15%
                if random.randint(1, 20) == 1:
                    spawn_amount = 1
                    cursor.execute('UPDATE infra SET corps = corps + ? WHERE name = ?', (spawn_amount, name))
                    conn.commit()

                    # Workers being employed from a corporation spawning.
                    cursor.execute('UPDATE user_stats SET adult = adult - ? WHERE name = ?', (spawn_amount * 575, name))
                    conn.commit()

                    logger.info(f"Corp_spawn: {name} has gotten 1 corp as tax rate is at default.")
                else:
                    logger.info(f'Corp_spawn: {name} has NOT gotten any corps.')
            else:
                logger.info(f"Corp_spawn: Tax rate is above default, no corps will spawn.")

        else:
            logger.info(f"Corp_spawn ERROR: COULD NOT FIND STATS FOR {name}.\n")

    else:
        logger.info(f"Corp_spawn ERROR: COULD NOT FIND {user_id}.\n")


def Corp_remove(user_id):
    cursor.execute('SELECT name, corp_tax FROM user_info WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        name, corp_tax = user_data

        # Fetch user's production infra
        cursor.execute('SELECT corps FROM infra WHERE name = ?', (name,))
        infra_result = cursor.fetchone()

        # Fetch user's pop stats.
        cursor.execute('SELECT adult FROM user_stats WHERE name = ?', (name,))
        pop_result = cursor.fetchone()

        if infra_result:
            corps = infra_result[0]
            adult = pop_result[0]

            corp_tax *= 100  # turn it from a percentage.
            difference = corp_tax - 15  # 15% is the default tax rate.

            if difference > 0:
                leave_probability = difference
                leave_amount = 0

                # Calculate the number of corporations to leave
                for _ in range(5):  # Attempt up to 5 leaves
                    if random.uniform(0, 100) < leave_probability:
                        leave_amount += 1

                if leave_amount > 0:
                    cursor.execute('UPDATE infra SET corps = corps - ? WHERE name = ?', (leave_amount, name))
                    conn.commit()

                    # Workers being unemployed from a corporation leaving.
                    cursor.execute('UPDATE user_stats SET adult = adult + ? WHERE name = ?', (leave_amount * 575, name))
                    conn.commit()

                    logger.info(f"Corp_remove: {leave_amount} corp(s) have left {name}.")
                else:
                    logger.info(f"Corp_remove: No corps have left {name}.")

            else:
                logger.info(f"Corp_remove: Tax rate is at or below default, no corps will leave.")

        else:
            logger.info(f"Corp_remove ERROR: COULD NOT FIND STATS FOR {name}.\n")

    else:
        logger.info(f"Corp_remove ERROR: COULD NOT FIND {user_id}.\n")