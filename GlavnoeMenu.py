import json
import time
from threading import Thread
import History
import pyodbc

cnxn = pyodbc.connect("Driver={SQL Server Native Client 17.0};"
                      "Server=root;"
                      "Database=Basketbol;"
                      "Trusted_Connection=yes;")
cursor = cnxn.cursor()
def start(ser, UserID):
    cursor.execute('''SELECT * FROM "Matches" WHERE UserID = '%s' ''' % (UserID))
    n = cursor.fetchall()
    if len(n) > 3:
        js = json.dumps({'UserID': UserID, 'MontoGame': len(n), 'LastGame': 3})
        ser.send(js.encode('UTF-16'))
        n = 3
    else:
        js = json.dumps({'UserID': UserID, 'MontoGame': len(n), 'LastGame': len(n)})
        ser.send(js.encode('UTF-16'))
    g = 0
    cursor.execute('''SELECT * FROM "Matches" WHERE UserID = '%s' ''' % (UserID))
    for i in cursor:
        if g < 3:
            js = json.dumps({'UserID': UserID, 'ResultGame': i[2], 'ScoreOneTeams': i[3], 'ScoreTwoTeams': i[4], 'NumberTeam': i[5], 'NumberTwoTeam': i[5]})
            ser.send(js.encode('UTF-16'))
            g += 1
        else:
            continue
    while True:
        dann = ser.recv(5120).decode('UTF-16')
        msg = json.loads(dann)
        if msg['Action'] == 'History':
            thes = Thread(target=History.History, args=(ser, UserID, ))
            thes.start()
