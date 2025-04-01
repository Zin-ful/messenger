from socket import SOCK_STREAM as tcp
from socket import AF_INET as ipv4
import socket as netcom
import os
import threading as task
import time
import curses
from curses import wrapper
from curses.textpad import Textbox
import sys
username = ""
users = 0
network = ""
security = ""
port = 45454
ip = ""
msg = ''
y = 0

def main(stdscr):
    global msg, HIGHLIGHT_1, HIGHLIGHT_2, HIGHLIGHT_3, HIGHLIGHT_4, FROM_SERVER, height, width, network, security, users, message_thread, update_thread

    height, width = stdscr.getmaxyx()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLUE)
    HIGHLIGHT = curses.color_pair(1)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLUE)
    HIGHLIGHT_1 = curses.color_pair(2)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    HIGHLIGHT_2 = curses.color_pair(3)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_WHITE)
    HIGHLIGHT_3 = curses.color_pair(4)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
    HIGHLIGHT_4 = curses.color_pair(5)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_WHITE)
    FROM_SERVER = curses.color_pair(6)

    stdscr.clear()
    stdscr.refresh()
    top_win = curses.newwin(0, width, 0, 0)
    show_chat = curses.newwin(height - 5, width, 2, 0)
    user_input = curses.newwin(1, width - 1, height - 1, 1)
    tbox = Textbox(user_input)
    security = "CHATS ARE NOT ENCRYPTED"
    i = 0
    while i < width:
        top_win.addstr(0, i, " ", HIGHLIGHT)
        i += 1
    top_win.refresh()
    time.sleep(1)
    update_thread = task.Thread(target=update, args=(stdscr, top_win, show_chat, user_input,))
    message_thread = task.Thread(target=message_recv, args=(show_chat,), daemon=True)
    update_thread.start()
    message_thread.start()
    message(tbox, user_input, top_win, show_chat, stdscr)

def update(stdscr, top_win, show_chat, user_input):
    global security, network, users, inp, msg
    time.sleep(2)
    top_win.addstr(0, 110, security, HIGHLIGHT_2)
    top_win.addstr(0, 200, "              ", HIGHLIGHT_1)
    top_win.addstr(0, 200, network, HIGHLIGHT_2)
    top_win.addstr(0, 10, str(users), HIGHLIGHT_1)
    top_win.refresh()

def config_init():
    global ip, server, network, users, username
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
            print("IP Address ID's found. would you like to select one? (y or n)")
            inp = input(">>> ")
            if "y" in inp:
                with open("config/connections.txt", "r") as file:
                    alias = file.readlines()
                    inp = input("Type in ID:\n>>> ")
                    for id in alias:
                        if inp in id:
                            junk, ip = id.split("&")
                            ip = ip.strip("\n")
            else:
                ip = input("Type in IP Address:\n>>> ")
        else:
            if not ip:
                 ip = input("Type in IP Address:\n>>> ")
        try:
            print(f"connecting to {ip}:{port}")
            server = netcom.socket(ipv4, tcp)
            server.connect((ip, port))
            server.sendall(username.encode("utf-8"))
            network = "connected!    "
            break
        except Exception as e:
            network = "disconnected  "
            print(f"Connection failed, server may be down. Try again? Error: {e}")
            inp = input(">>> ")
            if "y" in inp:
                continue
            else:
                exit()

def message_recv(show_chat):
    global y, msg, users
    x = 0
    while True:
        msg = server.recv(2048)
        if msg:
            if y >= height - 5:
                show_chat.erase()
                y = 0
                show_chat.refresh()
            msg = msg.decode("utf-8")
            if "server.message.from.server" in msg:
                msg = msg.replace("server.message.from.server", "")
                response, msg = msg.split(".", 1)
                if "users:" in msg:
                    response, msg = msg.split("!")
                    response = response.strip("users:")
                    users += int(response.strip())

                show_chat.addstr(y, x, msg, FROM_SERVER)
            else:
                show_chat.addstr(y, x, msg, HIGHLIGHT_3)
            for i in msg:
                if i == '\n':
                    y += 1
            if y >= height - 5:
                show_chat.erase()
                y = 0
            show_chat.refresh()


#$
def message(tbox, user_input, top_win, show_chat, stdscr):
    global y
    x = 0
    while True:
        try:
            inp = tbox.edit().strip()
            y += 2
            if inp:
                if y >= height - 5:
                    show_chat.erase()
                    y = 0
                    show_chat.refresh()

                if "#" in inp and '"' not in inp:
                    if inp == "#exit":
                        update_thread.join()
                        stdscr.clear()
                        stdscr.addstr(height // 2, width // 2, "    exiting...", HIGHLIGHT_3)
                        stdscr.refresh()
                        message_thread.join(timeout=1)
                        curses.nocbreak()
                        stdscr.keypad(False)
                        curses.echo()
                        curses.endwin()
                        server.close()
                        sys.exit()
                    elif inp == "#help":
                        inp = "#help: prints this message\n#exit: disconnects and quits the prograrm\n"
                    show_chat.addstr(y, x, inp, HIGHLIGHT_4)
                    user_input.erase()
                    user_input.refresh()
                    show_chat.refresh()
                    for i in inp:
                        if i == '\n':
                            y += 1
                    inp = None
                    continue
                
                if "server.main." not in inp or '"' in inp:
                    show_chat.addstr(y, x, inp, HIGHLIGHT_4)
                user_input.erase()
                user_input.refresh()
                show_chat.refresh()
                server.sendall(inp.encode("utf-8"))
                inp = None
        except KeyboardInterrupt:
                server.close()
                exit()
        except Exception as e:
            stdscr.clear()
            stdscr.addstr(height // 2, width // 2, str(e))
            stdscr.refresh()
config_init()
wrapper(main)
