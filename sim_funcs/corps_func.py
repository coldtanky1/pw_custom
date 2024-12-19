import logging
import random

from discord import User
import globals
from schema import *

logging_folder = globals.logging_folder + 'sim_logs.log'

logging.basicConfig(filename=logging_folder, level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    force=True)

logger = logging.getLogger(__name__)


def Corp_spawn(user_id):
    user_data = UserInfo.select(UserInfo.name, UserInfo.corp_tax).where(UserInfo.user_id == user_id).tuples().first()

    if user_data:
        name, corp_tax = user_data

        # Fetch user's production infra
        infra_result = Infra.select().where(Infra.name == name).first()

        if infra_result:
            corps = infra_result.corps  # unpack the result

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
                    Infra.update(corps=Infra.corps + spawn_amount).where(Infra.name == name).execute()

                    # Workers being employed from a corporation spawning.
                    UserStats.update(adult=UserStats.adult - spawn_amount * 575).where(UserStats.name == name).execute()

                    logger.info(f"Corp_spawn: {name} has gotten {spawn_amount} corps.\n")
                else:
                    logger.info(f'Corp_spawn: {name} has NOT gotten any corps.\n')

            elif difference == 0:
                # Always spawn at least one corporation if the tax rate is exactly 15%
                if random.randint(1, 20) == 1:
                    spawn_amount = 1
                    Infra.update(corps=Infra.corps + spawn_amount).where(Infra.name == name).execute()

                    # Workers being employed from a corporation spawning.
                    UserStats.update(adult=UserStats.adult - spawn_amount * 575).where(UserStats.name == name).execute()

                    logger.info(f"Corp_spawn: {name} has gotten 1 corp as tax rate is at default.\n")
                else:
                    logger.info(f'Corp_spawn: {name} has NOT gotten any corps.\n')
            else:
                logger.info(f"Corp_spawn: Tax rate is above default, no corps will spawn.\n")

        else:
            logger.info(f"Corp_spawn ERROR: COULD NOT FIND STATS FOR {name}.\n")

    else:
        logger.info(f"Corp_spawn ERROR: COULD NOT FIND {user_id}.\n")


def Corp_remove(user_id):
    user_data = UserInfo.select(UserInfo.name, UserInfo.corp_tax).where(UserInfo.user_id == user_id).tuples().first()

    if user_data:
        name, corp_tax = user_data

        # Fetch user's production infra
        infra_result = Infra.select().where(Infra.name == name).first()

        # Fetch user's pop stats.
        pop_result = UserStats.select().where(UserStats.name == name).first()

        if infra_result:
            corps = infra_result.corps
            adult = pop_result.adult

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
                    Infra.update(corps=Infra.corps - leave_amount).where(Infra.name == name).execute()

                    # Workers being unemployed from a corporation leaving.
                    UserStats.update(adult=UserStats.adult + leave_amount * 575).where(UserStats.name == name).execute()

                    logger.info(f"Corp_remove: {leave_amount} corp(s) have left {name}.\n")
                else:
                    logger.info(f"Corp_remove: No corps have left {name}.\n")

            else:
                logger.info(f"Corp_remove: Tax rate is at or below default, no corps will leave.\n")

        else:
            logger.info(f"Corp_remove ERROR: COULD NOT FIND STATS FOR {name}.\n")

    else:
        logger.info(f"Corp_remove ERROR: COULD NOT FIND {user_id}.\n")