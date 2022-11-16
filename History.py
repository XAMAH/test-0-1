import json
import time
import pyodbc


cnxn = pyodbc.connect("Driver={SQL Server Native Client 18.0};"
                      "Server=root;"
                      "Database=Basketbol;"
                      "Trusted_Connection=yes;")
cursor = cnxn.cursor()



def History(ser, UserID):
    cursor.execute('''SELECT * FROM "Matches" WHERE UserID = '%s' ''' % (UserID))
    for i in cursor:
        js = json.dumps(
            {'UserID': UserID, 'ResultGame': i[2], 'ScoreOneTeams': i[3], 'ScoreTwoTeams': i[4], 'NumberTeam': i[5],
             'NumberTwoTeam': i[5]})
        ser.send(js.encode('UTF-16'))
        time.sleep(0.02)

