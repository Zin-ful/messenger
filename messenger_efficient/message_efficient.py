from socket import SOCK_STREAM as tcp
from socket import AF_INET as ipv4
import socket as netcom
import os
import threading as task
import id_importer as importer
import time
import sys


print("\nCHATS ARE NOT ENCRYPTED\n")

attempt_count = 0
port = 45454
ip = ""

while True:
    if "user.txt" in os.listdir("config"):
        with open("config/user.txt", "r") as file:
            username = file.read()
    else:
        inp = input("enter username: ")
        with open("config/user.txt", "w") as file:
            file.write(inp)
        username = inp

    if "connections.txt" in os.listdir("config"):
        print("IP Address ID's found. would you like to select one?")
        inp = input(">>> ")
        if "y" in inp:
            with open("config/connections.txt", "r") as file:
                alias = file.readlines()
                inp = input("type in ID\n>>> ")
                for id in alias:
                    if inp in id:
                        junk, ip = id.split("&")
                        ip = ip.strip("\n")
                        print(ip)
        else:
            ip = input("enter IP address: ")
    else:
        if not ip:
            ip = input("enter IP address: ")
    try:
        print(f"connecting to {ip}:{port}")
        server = netcom.socket(ipv4, tcp)
        server.connect((ip, port))
        server.sendall(username.encode("utf-8"))

        break
    except Exception as e:
        attempt_count += 1
        print(f"Connection failed (attempt #{attempt_count}, server may be down. Try again?\nError: {e}")
        inp = input(">>> ")
        if "y" in inp:
            continue
        else:
            exit()

def message_recv():
    while True:
        msg = server.recv(2048)
        msg = msg.decode("utf-8")
        if msg:
            time.sleep(0.1)
            if "server.message.from.server" in msg:
                msg = msg.replace("server.message.from.server", "")
                response, msg = msg.split(".", 1)
                if "users:" in msg:
                    response, msg = msg.split("!")
                    print(f"{response}\n>>> \0")
                else:                
                    print(f"{msg}\n>>> \0")



def messenger():
    print("\n\nconnected! type #help for commands.\n")
    while True:
        try:
            time.sleep(0.2)
            inp = input(">>> ")
            if inp == "#exit":
                print("exiting...")
                message_thread.join(timeout=1)
                server.close()
                sys.exit()
                continue
            elif inp == "#import":
                importer.import_ip()
                continue
            elif inp == "#help":
                print("#help: prints this message\n#exit: disconnects and quits the prograrm\n#import: runs the import program allowing you to assign an IP to an alias")
                continue
            server.sendall(inp.encode("utf-8"))
        except KeyboardInterrupt:
            server.close()

message_thread = task.Thread(target=message_recv, args=(), daemon=True)
message_thread.start()
messenger()
message_thread.join()
