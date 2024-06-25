import sqlite3
import requests
import json


class vsysdb:
    def __init__(self, db_name="vsys.db"):
        self.db_name = db_name
        self.input_data_format = """(
                hostname TEXT,
                sn TEXT PRIMARY KEY,
                vsys_max INTEGER,
                vsys_used INTEGER,
                vsys_reserved INTEGER,
                vsys_free INTEGER
                vsys_in_use TEXT
            )"""
        self.reservation_data = '''
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sn TEXT,
                vsys_id TEXT,
                start_time TEXT,
                duration INTEGER,
                FOREIGN KEY(firewall_id) REFERENCES vsys(firewall_id)
            )
        '''
        self.connect()
        

    def connect(self):
    # Step 2: Create and Set Up the SQLite Database
        self.conn = sqlite3.connect(self.db_name)  # Connect to SQLite database (or create it if it doesn't exist)
        self.cur = self.conn.cursor()
        

        # Create a table to store the vsys data
        self.cur.execute(f'''
            CREATE TABLE IF NOT EXISTS vsys {self.input_data_format}
        ''')

# Step 3: Insert JSON Data into the SQLite Database

    def insertdata(self, data):
        for entry in data:
            self.cur.execute('''
                INSERT OR REPLACE INTO vsys (serial, total_vsys, used_vsys)
                VALUES (?, ?, ?)
            ''', )


        self.conn.commit()

# Optional: Query the database to verify insertion
    def get_data_from_db(self):
        self.cur.execute("SELECT * FROM vsys")
        rows = self.cur.fetchall()
        for row in rows:
            print(row)

    # # Close the connection
    # conn.close()
