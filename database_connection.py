import sqlite3
import constants as c

class Database_Connection: # class for all interaction with the database
    def __init__(self, path = c.DEFAULT_DATABASE_PATH): #init connection to the database
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
 
    def get_record(self, table, column, column_value, all_records=False): # get record(s) from the database
        self.cur.execute(f"SELECT * FROM {table} WHERE {column} == '{column_value}'")
        return self.cur.fetchall() if all_records else self.cur.fetchone()

    def insert_record(self, table, column_names, column_values): # insert a new record into the database
        cn = ', '.join(name for name in column_names)
        cv = ', '.join("?" for col in column_values)
        self.cur.execute(f'''INSERT INTO {table} ({cn}) VALUES ({cv})''', column_values)

    def update_record(self, table, column_names, column_values, replace_column, replace_value): # update exisiting record from the database  
        set_clause = ', '.join(f"{col} = ?" for col in column_names)
        self.cur.execute(f'''UPDATE {table} SET {set_clause} WHERE {replace_column} = ?''', list(column_values) + [replace_value])  
        
    def delete_record(self, table, column, column_value): # delete a record from the database
        self.cur.execute(f"DELETE FROM {table} WHERE {column} = '{column_value}'")
        
    # DO NOT USE class after calling, commit only needed when making changes (insert, update or del)
    def close(self, commit = False):
        if (commit): self.con.commit()
        self.con.close()
