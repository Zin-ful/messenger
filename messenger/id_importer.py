def import_ip():
    global inp
    print("this tool is made for you to assign an ID to an ip address for easier connections.\nfor example, if i want to connect to 192.168.10.1 i can assign that as Home-1 and connect to it that way\ninstead of typing out the entire IP address")
    while True:
        count = 1
        print("\ntype #exit to return to the chat\n")
        print("enter in the IP youd like to add to the list of connections")
        inp = input(">>> ")
        if "#exit" in inp:
            return
        ip = inp
        for char in ip:
            if char == ".":
                count += 1
        if count != 4:
            print("\n#######################\ninvalid ip format. it should look like this: xxx.xxx.x.x\n#######################")
            continue
        print("what ID would you like to use for that IP address?")
        inp = input(">>> ")
        if "#exit" in inp:
            return
        id = inp
        print(f"the alias for {ip} will be {id}, is this correct?")
        inp = input(">>> ")
        if "#exit" in inp:
            return
        if "y" in inp:
            with open("connections.txt", "a") as file:
                file.write(f"{id}&{ip}\n")
            print("id written to file. exiting...\n\n")
            return
        else:
            continue
import_ip()
