import sqlite3
import requests
import json
from datetime import datetime, timedelta


class vsysdb:

    reservation_expiration_hours = 24

    def __init__(self, db_name="vsys.db"):
        self.db_name = db_name
        self.input_data_format = """(
                serial TEXT PRIMARY KEY,
                hostname TEXT,
                vsys_max INTEGER,
                vsys_used INTEGER,
                vsys_free INTEGER,
                vsys_in_use TEXT,
                ha_peer TEXT
            )"""
        
        self.reservation_data_format = '''(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                serial TEXT,
                start_time TEXT,
                duration INTEGER,
                FOREIGN KEY(serial) REFERENCES vsys(serial)
            )
        '''
        self.connect()
        self.create_tables()
        
        

    def connect(self):
    # Step 2: Create and Set Up the SQLite Database
        self.conn = sqlite3.connect(self.db_name)  # Connect to SQLite database (or create it if it doeserial't exist)
        self.cur = self.conn.cursor()
        

    def create_tables(self):
        # Create a table to store the vsys data if table doeserial't exist
        self.cur.execute(f'''
            CREATE TABLE IF NOT EXISTS vsys {self.input_data_format}
        ''')

        self.cur.execute(f'''
            CREATE TABLE IF NOT EXISTS reservations {self.reservation_data_format}
        ''')

# Step 3: Insert JSON Data into the SQLite Database

    def insertdata(self, data):
        for entry in data:
            vsys_in_use_json  = json.dumps(entry['vsys_in_use'])
            self.cur.execute('''
                    INSERT OR REPLACE INTO vsys (serial, hostname, vsys_max, vsys_used, vsys_free, vsys_in_use, ha_peer)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (entry['serial'], entry['hostname'], entry['vsys_max'], entry['vsys_used'], entry['vsys_free'], vsys_in_use_json, entry['ha_peer']))
        
        self.conn.commit()

# Optional: Query the database to verify insertion
    def get_data_from_db(self):
        self.cur.execute("SELECT * FROM vsys")
        rows = self.cur.fetchall()
        for row in rows:
            print(row)

    def reserve_vsys(self, serial):

        ha_fw = False
        # Determine if vsys are synced across HA
        vsys_data1 = self.fetch_vsys(serial)
        ha_peer_sn = vsys_data1[0][6]
        if ha_peer_sn:
            ha_fw = True
            vsys_data_peer = self.fetch_vsys(ha_peer_sn)
            if vsys_data1[0][5] != vsys_data_peer[0][5]: # this compares vsyss on each fw
                raise Exception("HA Devices not Synced")
        
        vsys_free = self.calculate_vsys_free(serial)
        if vsys_free is None or vsys_free <= 0:
            # No VSYS available to reserve
            return False  # Reservation failed
        
        start_time = datetime.now().isoformat()
        
        # enter ha pair as higherserial_lowerserial


        self.cur.execute('''
            INSERT INTO reservations (serial, start_time, duration)
            VALUES (?, ?, ?)
        ''', (serial if not ha_fw else f"{max(serial, ha_peer_sn)}_{min(serial, ha_peer_sn)}", start_time, self.reservation_expiration_hours))
        self.conn.commit()
        
        return True

    def fetch_reservations(self, serial):
        self.cur.execute('''
            SELECT * FROM reservations
            WHERE serial = ? AND datetime(start_time, '+' || duration || ' hours') > datetime('now')
        ''', (serial,))
        rows = self.cur.fetchall()
        return rows
    
    def fetch_vsys(self, serial):
        self.cur.execute('''
            SELECT * FROM vsys
            WHERE serial = ? 
        ''', (serial,))
        rows = self.cur.fetchall()
        return rows
    
    def calculate_vsys_free(self, serial):
        self.cur.execute('''
            SELECT vsys_max, vsys_used FROM vsys
            WHERE serial = ?
        ''', (serial,))
        row = self.cur.fetchone()
        if row:
            vsys_max, vsys_used = row
            reservations = self.fetch_reservations(serial)
            # Check if reservations have expired
            active_reservations = 0
            now = datetime.now()
            for reservation in reservations:
                start_time = datetime.fromisoformat(reservation[2])
                duration = timedelta(hours=reservation[3])
                if now < start_time + duration:
                    active_reservations += 1
            
            vsys_free = vsys_max - vsys_used - active_reservations
            return vsys_free
        else:
            return None
        
    def close_connection(self):
        self.conn.close()