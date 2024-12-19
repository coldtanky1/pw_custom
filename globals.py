# File for global variables across different files

import os

def init():
    global debug, logging_folder
    debug = True
    logging_folder = os.getcwd() + '/logging/'
    if not os.path.exists(logging_folder):
        os.mkdir(logging_folder)

init()