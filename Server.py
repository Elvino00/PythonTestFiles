import json
import string
import time
from pathlib import Path
from pprint import pprint as prettyprint
import os
import socket
import logging
import signal

def socketCreation() -> bool:
    global server_socket
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return True
    except socket.error as e:
        print("socket creation failed")
        server_socket.close()
        return False


def socketBinding():
    global server_socket
    try:
        server_socket.bind(("127.0.0.1", 9091))
    except socket.error as e:
        server_socket.close()
        print("failed to create bind")
        logging.error(e)
        exit(1)

def socketListen():
    global server_socket
    try:
        print("Now in listening...")
        server_socket.listen(5)
        client, address = server_socket.accept()
        print(f"Connection accepted with {client.getpeername()}")
        return client, address
    except Exception as e:
        print("Listening error")
        server_socket.close()
        exit(1)

def scanPaths(client_object):
    path_dict = client_object.recv(1092).decode()
    print("Scegliere quale dei seguenti percorsi scannerizzare:")
    print(path_dict)
    choice = int(input())
    lines = {}
    path_dict = path_dict.replace('{', '')
    path_dict = path_dict.replace('}', '')
    index = 1
    for i in path_dict.splitlines():
        if i != '':
            mod_string = i[3:-1]
            mod_string = mod_string.split(f'"{index})')
            result = '"'.join(mod_string)
            result = result.split(":")
            result[0] = result[0].replace('"','')
            result[1] = result[1].replace('"','')
            lines[str(result[0])] = str(result[1])
            index += 1

    path = list(lines.values())[choice-1]

    return json.dumps(path,indent=4).encode("utf-8")

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
def downloadMenu(client_object):
    choice = 0

    found_files = client_object.recv(8192).decode()
    found_files = json.loads(found_files)
    found_files_number = []
    counter = 1
    index = 0
    for i in found_files:
        found_files_number.insert(index,f"{counter}) {found_files[index]}")
        counter += 1
        index += 1



    print("File trovati:\n")
    print(found_files_number)

    print("\nVuoi scaricare qualcosa? \n1) Sì\n2) No")

    choice = int(input())

    if choice == 1:
        print("Indicare con i numeri quali file scaricare. "
              "Per scaricare file consecutivamente scrivere '1-10' mentre per più file specifici, separarli con la virgola '1,3,5'.\n")
        choice2 = input()
        file_list = filteredList(choice2)

        return json.dumps(found_files,indent=4).encode("utf-8"),json.dumps(file_list).encode("utf-8")
    else:
        server_socket.close()
        exit(1)





def endConnectionMenu():
    print("Do you want to accept other connections?")
    print("1)Yes")
    print("2)No")
    risposta = input()
    if risposta == '1':
        return False
    elif risposta == '2':
        return True
    else:
        return endConnectionMenu()

def signal_handler(signal, frame):
    print("Keyboard Interrupt received: closing connection...")
    server_socket.close()
    exit(0)

def main():
    clientexist = False
    socketCreation()
    socketBinding()

    while not clientexist:
        client_object, _ = socketListen()
        chosen_path = scanPaths(client_object)
        client_object.send(chosen_path)
        time.sleep(5)
        found_files,files_by_number = downloadMenu(client_object)
        client_object.send(found_files)
        time.sleep(3)
        client_object.send(files_by_number)
        clientexist = endConnectionMenu()
    server_socket.close()



if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
