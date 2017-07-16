from flask import Flask, url_for, redirect, render_template, request, g


import datetime
import sqlite3

app = Flask(__name__)
app.config.from_object('_config')

def connect_db():
    return sqlite3.connect(app.config['DATABASE_PATH'], detect_types=sqlite3.PARSE_DECLTYPES)

def insert_task_string(task_name, min_days, max_days):
    """
    Helper function gives the insert sql query for a new task
    """
    date = datetime.datetime.now()
    return "INSERT INTO tasks (name, last_done, min_days, max_days) VALUES (?, ?, ?, ?)", (task_name, date, min_days, max_days)

@app.template_filter('datetime')
def format_datetime(value):
    format = "%D %I:%M %p"
    return value.strftime(format)

def update_task_string(task_id, date=None):
    """
    Helper function returns the update sql query to set the task
    with task_id to the current date/time
    """
    if date is None:
        date = datetime.datetime.now()
    return "UPDATE tasks SET last_done=? WHERE task_id=?", (date, task_id)

def get_dueness(task):
    current_time = datetime.datetime.now()
    how_many_days = (current_time - task['last_done']) / datetime.timedelta(days=1)
    dueness = (how_many_days - task['min_days']) / (task['max_days'] - task['min_days'])
    return dueness

def padded_hex(n):
    c = hex(n)[2:]
    if len(c) == 1:
        c = '0' + c
    return c

def get_task_color(task):
    """
    Helper function gets the hexadecimal color for a certain task
    """
    dueness = get_dueness(task)
    if dueness < 0:
        return "#CCCCCC"
    elif dueness < 0.5:
        hex_code = padded_hex(int((dueness / 0.5) * 255) + 1).upper()
        return "#%sFF00" % hex_code
    elif dueness < 1:
        hex_code = padded_hex(int((1 - dueness) * 255 / 0.5)).upper()
        return "#FF%s00" % hex_code
    else:
        return "#FF0000"

def wrap_task(task_row):
    return dict(task_id=task_row[0], name=task_row[1], min_days=task_row[2], max_days=task_row[3], last_done=task_row[4])

def get_all_tasks():
    """
    Returns a list of tasks (as dicts)
    """
    g.db = connect_db()
    cursor = g.db.execute("SELECT * FROM tasks")
    all_tasks = [wrap_task(t) for t in cursor.fetchall()]
    for task in all_tasks:
        task['task_color'] = get_task_color(task)
        task['dueness'] = get_dueness(task)
    g.db.close()
    return all_tasks

@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if request.method == 'GET':
        tasks = get_all_tasks()
        tasks.sort(key=get_dueness, reverse=True)
        return render_template('todo.html', tasks=tasks)
    else:
        g.db = connect_db()
        new_task = request.form["task"]
        min_days = request.form["min_days"]
        max_days = request.form["max_days"]
        insert_string, args = insert_task_string(new_task, min_days, max_days)
        g.db.execute(insert_string, args)
        g.db.commit()
        g.db.close()
        return redirect(url_for('todo'))

@app.route('/edit/<task_id>', methods=['GET', 'POST'])
def edit(task_id):
    g.db = connect_db()
    if request.method == 'GET':
        task = g.db.execute('SELECT * FROM tasks WHERE task_id=?', (task_id,)).fetchone()
        if task is None:
            return "Not a task actually"
        else:
            task = wrap_task(task)
            return render_template('task_edit.html', task=task)
    else:
        new_name= request.form["new_name"]
        last_done = request.form["new_date"]
        new_min = request.form["new_min"]
        new_max = request.form["new_max"]
        g.db.execute("UPDATE tasks SET name=?, last_done=?, min_days=?, max_days=? WHERE task_id=?", (new_name, last_done, new_min, new_max, task_id))
        g.db.commit()
        g.db.close()
        return redirect(url_for('todo'))

@app.route('/update/<task_id>')
def update(task_id):
    g.db = connect_db()
    task_string, args = update_task_string(task_id)
    g.db.execute(task_string, args)
    g.db.commit()
    g.db.close()
    return redirect(url_for('todo'))

if __name__ == "__main__":
    app.run(debug=True)
