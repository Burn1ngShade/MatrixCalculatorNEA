import sqlite3

path = "Assets/Matrix Calculator Database.db"

def get_record(table, column, column_value):
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM {table} WHERE {column} == '{column_value}'")
    result = cur.fetchone()
    con.close()
    return result 

def insert_record(table, column_names, column_values):
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(f'''INSERT INTO {table} ({column_names}) VALUES (?, ?)''', column_values)
    con.commit()
    con.close()

def delete_record(table, column, column_value):
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(f"DELETE FROM {table} WHERE {column} = '{column_value}'")
    con.commit()
    con.close()
