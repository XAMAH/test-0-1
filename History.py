import json
import time
import pyodbc


cnxn = pyodbc.connect("Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.0.so.1.1};"
                      "Server=XAMAH;"
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

