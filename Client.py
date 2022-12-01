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
    print("\nFile trovati:\n")
    count = 1
    file_number = []
    for root, dir, files in os.walk(input):
        for file in files:
            print(f"{count})  {file}")  # for file with full path   os.path.join(root,file)
            file_number.append(os.path.join(root, file))
            # print(os.path.join(root,file))
            count += 1

    return json.dumps(file_number).encode("utf-8")

def downloadMenu():
        choice = 0

        print("\nVuoi scaricare qualcosa? \n1) Sì\n2) No")

        choice = int(input())

        if choice == 1:
            print("Indicare con i numeri quali file scaricare. "
                  "Per scaricare file consecutivamente scrivere '1-10' mentre per più file specifici, separarli con la virgola '1,3,5'.\n")
            choice2 = input()
            file_list = filteredList(choice2)
            downloaderFunction(file_list)
        else:
            pass

def calculate_range_number(start: int, end: int, list: list):
    for i in range(start, end+1):
        if not i in list:
            list.append(i)

def is_str_correct(str):
    if str[len(str)-1] == "-" or str[len(str)-1] == ",":
        return False

    for i in range(0, len(str)):
        if i == len(str)-1:
            return True
        if(str[i] == str[i+1]):
            return False

    return False

def filteredList(rawList):
    single_file_index = []
    if is_str_correct(rawList):
        first_split_str = rawList.split(",")

        for i in first_split_str:
            if not '-' in i:
                if not int(i) in single_file_index:
                    single_file_index.append(int(i))
            else:
                range = i.split('-')
                calculate_range_number(int(range[0]), int(range[len(range) - 1]), single_file_index)
        return single_file_index
    else:
        print("La stringa non è valida")

def downloaderFunction():
    pass

def main():
    socketCreation()
    socketConnection()
    info = getPaths()
    client_socket.send(info)
    time.sleep(5)
    file_numbers = scanDir()


if __name__ == "__main__":
    main()
