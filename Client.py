import socket
import time
from pprint import pprint as prettyprint
from pathlib import Path
import os
import json
import sys

def socketCreation() -> bool:
    global client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return True
    except socket.error as e:
        print("socket creation failed")
        return False


def socketConnection():
    connected = False
    while not connected:
        try:
            client_socket.connect(("127.0.0.1", 9091))
            print("Socket successfully created and connected")
            connected = True
        except socket.error as se:
            print("Error connecting the socket. Trying again every 5s")
            time.sleep(5)


def getPaths():
    Relative_path = str(Path.home()) + '/.config/user-dirs.dirs'  #/home/$USER/.config/user-dirs.dirs
    print(Relative_path)  #secondo print
    count = 1
    with open(Relative_path ,'r') as file: #open file and when scope is ended, automatically close it
        path_dict = {}
        for i  in file.read().splitlines():   #read file row by row
            if i.startswith("XDG"):   #if string starts with XDG...
                x = i.split("$HOME/")  #only get second part of "$HOME/..."  (gets the final " too)
                path_dict[f"{count}) {x[1][:-1]}"] =  str(Path.home()) + "/" + x[1][:-1]
                count += 1

    return json.dumps(path_dict,indent=4).encode("utf-8")



def scanDir():
    input = client_socket.recv(1092).decode()
    input = input.replace('"','')
    input = input.replace(" ", "")
    count = 1
    file_number = []
    for root, dir, files in os.walk(input):
        for file in files:
            file_number.append(os.path.join(root,file))
            count += 1

    return json.dumps(file_number).encode("utf-8")

def uploaderFunction():
   found_files = client_socket.recv(8192).decode()
   found_files = json.loads(found_files)

   time.sleep(3)

   files_by_number = client_socket.recv(1092).decode()
   files_by_number = json.loads(files_by_number)




def main():
    socketCreation()
    socketConnection()
    info = getPaths()
    client_socket.send(info)
    time.sleep(5)
    file_numbers = scanDir()
    client_socket.send(file_numbers)
    uploaderFunction()


if __name__ == "__main__":
    main()
