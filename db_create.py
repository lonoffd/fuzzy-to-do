import sqlite3
import datetime
from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:
    c = connection.cursor()

    c.execute("""DROP TABLE IF EXISTS tasks""")

    c.execute("""CREATE TABLE tasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL, min_days REAL, max_days REAL, last_done TIMESTAMP)""")

    c.execute("""INSERT INTO tasks (name, last_done, min_days, max_days)
                VALUES("Change Litter", ?, 2.0, 3.5)""", (datetime.datetime(2017, 7, 5),))
    c.execute("""INSERT INTO tasks (name, last_done, min_days, max_days)
                VALUES("Clean Stove", ?, 14.0, 20.0)""", (datetime.datetime(2017, 7, 4),))

    c.execute("""INSERT INTO tasks (name, last_done, min_days, max_days)
                VALUES("Clean Shower", ?, 7.0, 21.0)""", (datetime.datetime(2017, 7, 3),))
