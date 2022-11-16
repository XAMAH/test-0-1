import json
import socket
import time
from threading import Thread
import pyodbc

import GlavnoeMenu
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server.bind(('127.0.0.1', 2000))

server.listen()


cnxn = pyodbc.connect("Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.0.so.1.1};"
                      "Server=root;"
                      "Database=Basketbol;"
                      "Trusted_Connection=yes;")
cursor = cnxn.cursor()
print('Сервер запущен')




def listen():
    try:
        dann = ser.recv(5120).decode('UTF-16')
        try:
            msg = json.loads(dann)




            if msg['Result'] == 'Autme':
                cursor.execute(
                    '''SELECT * FROM "User" WHERE Login = '%s' and Password = '%s' ''' % (
                    msg['Login'], msg['Password']))
                ns = cursor
                for i in cursor:
                    js = json.dumps({'UserID': i[0], 'ResultAutme': True, 'LicenseTime': i[7]})
                    ser.send(js.encode('UTF-16'))
                    thes = Thread(target=GlavnoeMenu.start, args=(ser, i[0], ))
                    thes.start()
                if ns.fetchall() == 0:
                    js = json.dumps({'UserID': 'Null', 'ResultAutme': 'False', 'LicenseTime': 'Null'})
                    ser.send(js.encode('UTF-16'))




            if msg['Result'] == 'Registr':
                cursor.execute('''SELECT * FROM "User" WHERE Login = '%s' ''' % (msg['Login']))
                if cursor.rowcount == -1:
                    js = json.dumps({'UserID': 'Null', 'ResultRegistr': 'False', 'LicenseTime': 'Null'})
                    ser.send(js.encode('UTF-16'))
                else:
                    cursor.execute('''INSERT INTO "User" (Login, Password, MacAdressUser, UserName, Mail, Phone, LicenseTime) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', Null) ''' % (msg['Login'], msg['Password'], msg['MacAdressUser'], msg['UserName'], msg['Mail'], msg['Phone']))
                    cnxn.commit()
                    js = json.dumps({'UserID': 'Null', 'ResultRegistr': 'True', 'LicenseTime': 'Null'})
                    ser.send(js.encode('UTF-16'))


            if msg['Result'] == 'Reset':
                cursor.execute('''SELECT * FROM "User" WHERE Login = '%s' ''' % (msg['Login']))
                if cursor.rowcount != 0:
                    cursor.execute('''UPDATE "User" SET Password = '%s' WHERE Login = '%s' ''' % (msg['Password'], msg['Login']))
                    cnxn.commit()
                    js = json.dumps({'UserID': 'Null', 'ResultReset': 'True', 'LicenseTime': 'Null'})
                    ser.send(js.encode('UTF-16'))
                else:
                    js = json.dumps({'UserID': 'Null', 'ResultReset': 'False ', 'LicenseTime': 'Null'})
                    ser.send(js.encode('UTF-16'))



        except:
            listen()
    except:
        print('')



def connect(ser):
    thes = Thread(target=listen(), args=())
    thes.start()

while True:
    ser, con = server.accept()
    connect(ser)

