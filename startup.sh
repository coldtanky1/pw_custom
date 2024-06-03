#!/bin/bash

# Function to terminate the processes.
function clean_up {
    echo "Terminating processes."
    pkill -f /home/void/pw_custom/main.py
    pkill -f /home/void/pw_custom/admin_panel/panel.py
    echo "Processes terminated."
    exit 0
}

echo 'Starting the bot.'
python /home/void/pw_custom/main.py &
bot_pid=$!

echo 'Bot started.'

echo 'Starting admin panel'
python /home/void/pw_custom/admin_panel/panel.py &
admin_pid=$!

echo 'Admin panel started.'

# Gets triggered when Ctrl+C is pressed.
trap clean_up INT

wait $admin_pid $bot_pid