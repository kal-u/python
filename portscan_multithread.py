from threading import *
from termcolor import colored
import socket
import os
import sys
import pyfiglet 

os.system('clear')
ascii_banner = pyfiglet.figlet_format("Port Scanner")
print(ascii_banner) 

if len(sys.argv) !=2 :
    print ("Usage: " + sys.argv[0] +" <host>")
    sys.exit(1)

try:
    host = socket.gethostbyname(sys.argv[1])
except:
    print(colored("Nom ou Adresse IP incorrecte\n",'red'))
    print ("Usage: " + sys.argv[0] +" <host>")
    sys.exit(1)


screenLock = Semaphore(value=1)
debug = 0
port_min = 1
port_max = 1024
open_ports = []

def scan(ip,port):

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        if debug:
            screenLock.acquire()
            print ('Scanning ', ip , 'on port',  port)
            print("Port",port, "is open")
        s.close()
        summary(port)

    except:
        if debug:
            screenLock.acquire()
            print ('Scanning ', ip , 'on port',  port)
            print("Port",port,"is closed")

    finally:
        screenLock.release()
        s.close()

def loop():
    threads = []
    ip = host
    for i in range(port_min,port_max):
        port = int(i)
        t = Thread(target=scan, args=(ip,int(port)))
        t.start()
        threads.append(t)
    [t.join() for t in threads]
    return

def summary(port):
    global open_ports
    open_ports.append(port)
    return      

def main():
    print(colored('Adresse IP scannée : ' + host,'yellow'))
    loop()
    finish()

def finish():
    print('Les ports suivants sont ouverts :',open_ports) 


main()
