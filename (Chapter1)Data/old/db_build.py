import os
import sys
from datetime import datetime

import sqlite3
import numpy as np
import pandas as pd

class db_build:
    def __init__(self):
        self.date = datetime.today()
        print("main dir is : ", os.getcwd())
        os.chdir(os.path.join(os.getcwd(), 'data'))
        print("data dir is : ", os.getcwd())

    def connect_database(self):
        try:
            # creating file path
            dbfile = 'TRACE.db'
            # Create a SQL connection to our SQLite database
            self.conn = sqlite3.connect(dbfile)
            self.cursor = self.conn.cursor()
            return "TRACE db connected"
        except sqlite3.Error as e:
            print("Error connecting data from SQLite database:", e)
            return None
    
    def disconnect_database(self):
        try:
            self.cursor.close()
            self.conn.close()
            return "TRACE DB disconnected"
        
        except sqlite3.Error as e:
            print("Error disconnecting data from SQLite database:", e)
            return None
    
    def trucate_existing_table(self, table_name):

        try:
            self.cursor.execute("Delete from {table_name}")
            self.cursor.execute("DELETE FROM SQLITE_SEQUENCE WHERE name='{table_name}';")
        except sqlite3.Error as e:
            print("Error trucating data from SQLite database:", e)
            return None  
  

        
    def process_bond_price_data(self, bond_price_df):
        self.connect_database()

        # to be added

        self.process_factor_price_data()

        return "111"

    def process_factor_price_data(self, factor_data_df):
        self.connect_database()

        # to be added

        self.process_factor_price_data()
        return "222"


    
    def run(self):




# if __init__=="__main__":
#     data_bond.get_bond_data()