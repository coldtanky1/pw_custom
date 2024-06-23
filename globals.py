# File for global variables across different files

import os
import sqlite3
import sqlite3 as sql

def init():
    global debug, cursor, logging_folder, conn
    debug = True
    logging_folder = os.getcwd() + '/logging/'
    if not os.path.exists(logging_folder):
        os.mkdir(logging_folder)
    conn = sqlite3.connect('player_info.db')
    cursor = conn.cursor()
