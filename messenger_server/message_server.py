from socket import SOCK_STREAM as tcp
from socket import AF_INET as ipv4
import socket as netcom
import threading as task
import datetime

port = 45454
ip = "0.0.0.0"

linky = "none" #perma link like for a discord, youtube channel, etc or an IP or something
cont = "none" #contact information
server = netcom.socket(ipv4, tcp)
server.bind((ip, port))

with open("config/missed.txt", "w") as file:
    file.write("$\n")

users = []
users_name = {}
clients_lock = task.Lock()

def contact(client_socket, msg):
    return f"server.message.from.server.{cont}"

def link(client_socket, msg):
    return f"server.message.from.server.{linky}"

def helpy(client_socket, msg):
    return "server.message.from.server.bug-report\nlist-users\nhelp"

def bug_report(client_socket, msg):
    if msg:
        with open("config/reports.txt", "a") as file:
            file.write(f"{datetime.datetime.now()} report: {msg}\n")
        return "server.message.from.server.Submitted!"

def list_users(client_socket, msg):
    if msg:
        msg = ""
        for i in users_name.values():
            msg += f"{i}\n"
        return f"server.message.from.server. {msg}"


commands = {"bug-report":bug_report,"get-users": list_users,"get-link": link, "get-contact": contact, "help":helpy}

def log(client_socket, msg):
    if msg:
        with open("config/log.txt", "a") as file:
            file.write(f"from {client_socket}: {msg}\n")

def messenger(client_socket, addr):
    addr_id = str(addr)
    user_id, user_ip = addr_id.split(",")
    user_ip = user_ip.strip("(").strip("'").strip(")")
    user_id = user_ip.strip("(").strip("'").strip(")")
    
    username = client_socket.recv(128)
    users_name.update({str(user_id): username.decode("utf-8")})

    print(f"user connected: {addr}")
    with clients_lock:
        users.append(client_socket)
    for user in users:
        msg = f"server.message.from.server.users: {len(users)} !\n###########\nSYSTEM MESSAGE: user connected: {addr}\n###########\n"
        user.sendall(msg.encode("utf-8"))
    try:
        while True:
            msg = client_socket.recv(2048)
            if not msg:
                break
            message = f"{msg.decode('utf-8')}\n"
            if "server.main." in message and '"' not in message:
                cmd = message.strip("server.main.")
                log(client_socket, cmd)
                if "bug-report" in message:
                    cmd, message = cmd.split(":")
                print(cmd)
                print(message)
                xcute = commands.get(cmd.strip())
                if cmd:
                     message = xcute(client_socket, message)
                else:
                    message = "server.message.from.server.invalid"
                log(client_socket, message)
                client_socket.sendall(message.encode("utf-8"))
                continue
            else:
                message = f"\n@{users_name.get(user_id)}: {msg.decode('utf-8')}\n"
            if len(users) <= 1:
                with open("config/missed.txt", "a") as file:
                    file.write(f"{message}\n")
            print(message)        
            with clients_lock:
                for other_client in users:
                    if other_client != client_socket:
                        try:
                            other_client.sendall(message.encode("utf-8"))
                        except Exception as e:
                            print(f"message send failed: {e}")
    except Exception as e:
        print(f"message recv failed: {e}")
    finally:
        for user in users:
            #del users_name[user_id]
            user.sendall(f"server.message.from.server.users: -1 !\n###########\nSYSTEM MESSAGE: user DISconnected: {addr}\n###########\n".encode("utf-8"))
            
        print("connection closed")
        with clients_lock:
            users.remove(client_socket)
        client_socket.close()






while True:
    try:
        server.listen(3)
        print(f"server listening on ip: {ip} and port {port}")
        client_socket, addr = server.accept()
        client_thread = task.Thread(target=messenger, args=(client_socket, addr))
        client_thread.start()
    except Exception as e:
        print(f"threading failed: {e}")
