from flask import Flask, render_template, redirect, request, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'my_dark_secret'

conn = sqlite3.connect('player_info.db')
cursor = conn.cursor()

def get_data(nation_name):
    conn = sqlite3.connect('player_info.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    data = {}
    for table in tables:
        table_name = table[0]
        query = f'SELECT * FROM {table_name} WHERE name = ?'
        cursor.execute(query, (nation_name,))
        columns = [description[0] for description in cursor.description]
        table_data = cursor.fetchall()
        data[table_name] = [dict(zip(columns, row)) for row in table_data]
    conn.close()
    return data

def update_data(table, nation_name, column, operation, amount):
    conn = sqlite3.connect('player_info.db')
    cursor = conn.cursor()
    if column == "name":
        flash("You cannot edit the 'name' column.")
        return redirect(url_for('update'))
    if operation == "add":
        query = f'UPDATE {table} SET {column} = {column} + ? WHERE name = ?'
    elif operation == "subtract":
        query = f'UPDATE {table} SET {column} = {column} - ? WHERE name = ?'
    cursor.execute(query, (amount, nation_name))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/modify', methods=['POST'])
def modify():
    nation_name = request.form.get('nation_name')
    selection = request.form.get('table')
    return redirect(url_for('modify_get', nation_name=nation_name, selection=selection))

@app.route('/modify', methods=['GET'])
def modify_get():
    nation_name = request.args.get('nation_name')
    selection = request.args.get('selection')

    match selection:
        case "infra":
            data = get_data(nation_name)
        case "resources":
            data = get_data(nation_name)
        case "user_info":
            data = get_data(nation_name)
        case "user_mil":
            data = get_data(nation_name)
        case "user_stats":
            data = get_data(nation_name)
        case _:
            data = []

    return render_template('modify.html', nation_name=nation_name, selection=selection, data=data)

@app.route('/update', methods=['POST'])
def update():
    nation_name = request.form.get('nation_name')
    selection = request.form.get('table')
    column = request.form.get('column')
    operation = request.form.get('operation')
    amount = int(request.form.get('amount'))

    update_data(selection, nation_name, column, operation, amount)

    return redirect(url_for('modify_get', nation_name=nation_name, selection=selection))

app.run()