import os
import sys

import sqlite3
import numpy as np
import pandas as pd

class data_bond:
    def __init__(self):
        self.date = '20240501'
        print("main dir is : ", os.getcwd())
        os.chdir(os.path.join(os.getcwd(), 'data'))
        print("data dir is : ", os.getcwd())

    def get_bond_data(self):
        # creating file path
        dbfile = 'TRACE.db'
        # Create a SQL connection to our SQLite database
        conn = sqlite3.connect(dbfile)

        # creating cursor
        cursor = conn.cursor()

        # reading all table names
        table_list = [a for a in cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]

        print(table_list)
        return table_list
    
    def run(self):
        self.get_bond_data()

# if __init__=="__main__":
#     data_bond.get_bond_data()