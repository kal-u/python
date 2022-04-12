from threading import *
from termcolor import colored
import socket
import os
import sys
import pyfiglet 

# Effacement de l'écran
os.system('cls')

# Affichage du banner "Port Scanner"
ascii_banner = pyfiglet.figlet_format("Port Scanner")
print(ascii_banner) 

# Vérification qu'il y a bien une cible en argument
if len(sys.argv) !=2 :
    print ("Usage: " + sys.argv[0] +" <host>")
    sys.exit(1)

# Vérification qu'un nom ou une IP correcte a été indiquée
try:
    # Récupération de l'IP à partir du nom ou de l'IP
    host = socket.gethostbyname(sys.argv[1])

# Exception si impossible de résoudre le nom en adresse IP
except:
    print(colored("Nom ou Adresse IP incorrecte\n",'red'))
    print ("Usage: " + sys.argv[0] +" <host>")
    sys.exit(1)

# Initialisation d'unun objet screenlock avec une semaphore à 1 (qui sera incrémentée à chaque release et décrémentée à chaque acquire)
screenLock = Semaphore(value=1)

# Mode debug pour afficher plus d'informations
debug = 0

# Définition des ports mix et max pour le scan
port_min = 1
port_max = 1024

# Création d'un tableau vide qui contiendra les ports ouverts
open_ports = []

# Fonction pour scanner un port sur une IP
def scan(ip,port):

    # Tentative de connexion
    try:
        # Création d'un objet socket pour une connexion TCP IP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Indication de l'IP et du port
        s.connect((ip, port))

        # Affichage des informations de connexion
        if debug:
            screenLock.acquire()
            print ('Scanning ', ip , 'on port',  port)
            print("Port",port, "is open")
        
        # Fermeture de la socket
        s.close()

        # Appel de la fonction summary pour ajouter le port à la liste des ports ouverts
        summary(port)

    # En cas d'échec de connexion
    except:
        # Affichage du port fermé
        if debug:
            screenLock.acquire()
            print ('Scanning ', ip , 'on port',  port)
            print("Port",port,"is closed")
    
    # Libération de l'object semaphore et fermeture de la socket
    finally:
        screenLock.release()
        s.close()

# Création d'une boucle pour créer un thread par port
def loop():
    # Définition du tableau de threads
    threads = []

    # Affectation de l'IP
    ip = host

    # Pour chaque port entre min et max
    for i in range(port_min,port_max):
        # Définition du port en entier
        port = int(i)

        # Création d'un thread faisant appel à la fonciton scan avec l'ip et le port en arguments
        t = Thread(target=scan, args=(ip,int(port)))

        # Lancement de l'exécution du thread
        t.start()

        # Ajout du thread au tableau des threads
        threads.append(t)
    
    # On attend que tous les threads se terminent puis on quitte la boucle
    [t.join() for t in threads]
    return

# Fonction d'ajout des ports ouverts dans un tablea
def summary(port):
    global open_ports
    open_ports.append(port)
    return      

# Fonction d'affichage des ports ouverts
def finish():
    print('Les ports suivants sont ouverts :',open_ports) 

# Fonction principale
def main():
    print(colored('Adresse IP scannée : ' + host,'yellow'))
    # Lancement du scan des ports
    loop()
    # Affichage des ports ouverts
    finish()

# Lancement de la fonction principale
main()
