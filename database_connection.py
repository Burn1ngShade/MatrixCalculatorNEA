import sqlite3
import constants as c

class Database_Connection:
    def __init__(self, path = c.DEFAULT_DATABASE_PATH):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
 
    def get_record(self, table, column, column_value, all_records=False):
        self.cur.execute(f"SELECT * FROM {table} WHERE {column} == '{column_value}'")
        return self.cur.fetchall() if all_records else self.cur.fetchone()

    def insert_record(self, table, column_names, column_values):
        cn = ', '.join(name for name in column_names)
        cv = ', '.join("?" for col in column_values)

        self.cur.execute(f'''INSERT INTO {table} ({cn}) VALUES ({cv})''', column_values)

    def update_record(self, table, column_names, column_values, replace_column, replace_value):    
        set_clause = ', '.join(f"{col} = ?" for col in column_names)
        self.cur.execute(f'''UPDATE {table} SET {set_clause} WHERE {replace_column} = ?''', list(column_values) + [replace_value])  
        
    def delete_record(self, table, column, column_value):
        self.cur.execute(f"DELETE FROM {table} WHERE {column} = '{column_value}'")
        
    # this is obvisouly terrible for security but as its a prototype it doesnt matter?
    def run_custom_SQL(self, sql):
        self.cur.execute(sql) # i hate secure code yayayayay
        
    # DO NOT USE class after calling
    def close(self, commit = False):
        if (commit): self.con.commit()
        self.con.close()
        
# WE NEED TO UPDATE DELETE ACCOUNT TO DELETE RECORDS ON ALL DATABASES
# DELETING FROM RECORD NEEDS TO DELETE FROM DATABASE
# NEED TO SORT THE LOADED DATA
