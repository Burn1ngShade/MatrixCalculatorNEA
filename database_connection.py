import sqlite3
import constants as c

# class for all interaction with the database
class Database_Connection: 
    def __init__(self, path = c.DEFAULT_DATABASE_PATH): #init connection to the database
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
        
    def close(self, commit = False): # do not use class after closing, commit only needed when modifying database
        if (commit): self.con.commit()
        self.con.close()
        
    # --- DATABASE INTERACTION ---
 
    def get_record(self, table, column, column_value, all_records=False): # get record(s) from the database
        self.cur.execute(f"SELECT * FROM {table} WHERE {column} == '{column_value}'")
        return self.cur.fetchall() if all_records else self.cur.fetchone()

    def insert_record(self, table, column_names, column_values): # insert a new record into the database
        formatted_column_names = ', '.join(name for name in column_names)
        formatted_column_values = ', '.join("?" for col in column_values)
        self.cur.execute(f'''INSERT INTO {table} ({formatted_column_names}) VALUES ({formatted_column_values})''', column_values)

    def update_record(self, table, column_names, column_values, replace_column, replace_value): # update exisiting record from the database  
        formatted_column_names = ', '.join(f"{col} = ?" for col in column_names)
        self.cur.execute(f'''UPDATE {table} SET {formatted_column_names} WHERE {replace_column} = ?''', list(column_values) + [replace_value])  
        
    def delete_record(self, table, column, column_value): # delete a record from the database
        self.cur.execute(f"DELETE FROM {table} WHERE {column} = '{column_value}'")
        