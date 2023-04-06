import os, time, sys, traceback, csv
import sqlite3


def export_table_to_csv(table_name, csv_file, connection, write_header=True):
    dbcur = connection.execute("SELECT * FROM " + table_name)
    cols = dbcur.description
    cf = open(csv_file, 'w', newline='', encoding="utf-8")

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
folder = r"""\\ddoefile01\AQDDATA2\Air Quality Planning Branch\Emission Inventories & Modeling\Mobile Nonroad and MAR Source EIs\Copter Tracker"""
  
sql_database = folder +  r"""\copters.sqlite"""
dbconn = sqlite3.connect(sql_database)        
export_table_to_csv("copters", folder +  r"""\copters.csv""", dbconn)
dbconn.close()

  
