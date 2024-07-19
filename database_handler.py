import sqlite3
import entry_validation as val

path = "Assets/Matrix Calculator Database.db"

def get_record(table, column, column_value, all_records=False):
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM {table} WHERE {column} == '{column_value}'")
    result = cur.fetchall() if all_records else cur.fetchone()
    con.close()
    return result 

def insert_record(table, column_names, column_values):
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(f'''INSERT INTO {table} ({column_names}) VALUES (?, ?)''', column_values)
    con.commit()
    con.close()
    
def replace_record(table, column_names, column_values, replace_column, replace_value):
    val.raise_error("E900", "I aint implement this icl")
    

def delete_record(table, column, column_value):
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(f"DELETE FROM {table} WHERE {column} = '{column_value}'")
    con.commit()
    con.close()
