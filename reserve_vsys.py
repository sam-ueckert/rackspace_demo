from db import vsysdb

vsys_db = vsysdb()

reserved = vsys_db.reserve_vsys('026701009424_026701009351')

vsys_db.close_connection()

if reserved: 
    print("Vsys Reserved!")
else:
    print("No VSYS Available to reserve.")