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
        clientexist = endConnectionMenu()
    server_socket.close()



if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
