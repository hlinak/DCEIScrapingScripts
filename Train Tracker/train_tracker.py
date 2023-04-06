import os, requests, json, time, sys, traceback, csv
import sqlite3

#https://www.mta.maryland.gov/marc-tracker
#https://www.vre.org/service/status/

def export_table_to_csv(table_name, csv_file, connection, write_header=True):
    dbcur = connection.execute("SELECT * FROM " + table_name)
    cols = dbcur.description
    cf = open(csv_file, 'w', newline='')

    cw = csv.writer(cf)
    row_count = 0
    if write_header:
        names = [col[0] for col in cols]
        cw.writerow(names)
    for row in dbcur:
        cw.writerow(row)
        row_count += 1

def log_stack(filename):
    logfile = open(filename, 'w')
    exc = sys.exc_info()[0]
    stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
    trc = 'Traceback (most recent call last):\n'
    stackstr = trc + ''.join(traceback.format_list(stack))
    if exc is not None:
         stackstr += '  ' + traceback.format_exc().lstrip(trc)
    print(stackstr, file=logfile)
    logfile.close()
    
dbconn = None
folder = r"""\\ddoefile01\AQDDATA2\Air Quality Planning Branch\Emission Inventories & Modeling\Mobile Nonroad and MAR Source EIs\Train Trackers"""

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Accept-Encoding": "*",
        "Connection": "keep-alive"
    }
try:   
    sql_database = folder +  r"""\marc.sqlite"""
    content = requests.get("https://www.mta.maryland.gov/marc-tracker/fetchvehicles", headers=headers)
    if content.status_code == 200:
        jcontent = json.loads(content.content)
        dbconn = sqlite3.connect(sql_database)
        if(not os.path.isfile(sql_database)):
            dbconn.execute("""CREATE TABLE trains
                (datetime DATETIME,
                entity_id TEXT NOT NULL COLLATE NOCASE,
                trip_id TEXT NOT NULL COLLATE NOCASE,
                trip_name TEXT,
                trip_headsign TEXT,
                destination TEXT,
                route_name TEXT,
                lat REAL,
                lon REAL,
                delay REAL,
                PRIMARY KEY (datetime, entity_id, trip_id),
                UNIQUE (datetime, entity_id, trip_id));""")
            dbconn.commit()

        if "vehicleArr" in jcontent and "trains" in jcontent["vehicleArr"]:
            for train in jcontent["vehicleArr"]["trains"]:
                dbconn.execute("""INSERT INTO trains (datetime, entity_id, trip_id, trip_name, trip_headsign, destination, route_name, lat, lon, delay)
                    SELECT datetime('now', 'localtime'), ?, ?, ?, ?, ?, ?, ?, ?, ?""",
                    (train['entity_id'], train['trip_id'], train['trip_name'], train['trip_headsign'], train['destination'], train['route_name'], train['lat'], train['lon'], train['delay']))
            dbconn.commit()               
        dbconn.close()
except Exception:
    log_stack(folder +  r"""\marc_error_log_"""+str(time.time())+".txt")
    if(dbconn):
        dbconn.close()
    
try:   
    sql_database = folder +  r"""\vre.sqlite"""
    content = requests.get("https://www.vre.org/sites/vre/datasets/trains.cfc?method=delays", headers=headers)
    if content.status_code == 200:
        jcontent = json.loads(content.content)
                                 
        dbconn = sqlite3.connect(sql_database)
        if(not os.path.isfile(sql_database)):
            dbconn.execute("""CREATE TABLE trains
                (datetime DATETIME,
                vehicleid TEXT NOT NULL COLLATE NOCASE,
                stopid TEXT NOT NULL COLLATE NOCASE,
                trip TEXT NOT NULL COLLATE NOCASE,
                route TEXT NOT NULL COLLATE NOCASE,
                vehiclelabel TEXT,
                status TEXT,
                stopsequence TEXT,
                time REAL,
                lat REAL,
                long REAL,
                delay REAL,
                PRIMARY KEY (datetime, vehicleid, stopid, trip, route),
                UNIQUE (datetime, vehicleid, stopid, trip, route));""")
            dbconn.commit()

        if "entity" in jcontent:
            for train in jcontent["entity"]:
                for col in ['vehicleid', 'stopid', 'trip', 'route']:
                    if (col not in train): train[col] = 'X'
                for col in ['vehiclelabel', 'status', 'stopsequence', 'time', 'lat', 'long', 'delay']:
                    if (col not in train): train[col] = None
                dbconn.execute("""INSERT INTO trains (datetime, vehicleid, stopid, trip, route, vehiclelabel, status, stopsequence, time, lat, long, delay)
                    SELECT datetime('now', 'localtime'), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?""",
                    (train['vehicleid'], train['stopid'],train['trip'], train['route'], train['vehiclelabel'], train['status'], train['stopsequence'], train['time'], train['lat'], train['long'], train['delay']))
            dbconn.commit()
        dbconn.close()
except Exception:
    log_stack(folder +  r"""\vre_error_log_"""+str(time.time())+".txt")
    if(dbconn):
        dbconn.close()




