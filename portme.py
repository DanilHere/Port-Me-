import socket 
import os
import threading
import time


if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")

GREEN = "\033[92m"
RESET = "\033[0m"


# User interfaces


logo = r"""
  ____            _     __  __             
 |  _ \ ___  _ __| |_  |  \/  | ___     
 | |_) / _ \| '__| __/ | |\/| |/ _ \ 
 |  __/ (_) | |  | ||  | |  | |  __/
 |_|   \___/|_|   \__\ |_|  |_|\___|  

        Simple Python Port Scanner
"""
print(logo)

print("Author : Danil")
print("Version: 1.0")
print("-" * 50)

print("Mode Menu")
print("1.Single Port")
print("2.Multiple Port")

mode = input("Users> ")
start_time = time.time() #start time for scanning

found = False
lock = threading.Lock() #Threading feature

# scan port Function
def scan_port(ip, port):
    global found

    s = socket.socket()
    s.settimeout(1) # set timeout if target not responding
    
    result = s.connect_ex((ip,port)) # Validate Target / Knock Target
    service_name = services.get(port, "Unknown") # services detection
    
    # compare results variabel
    if result == 0:
        message = f"{GREEN}[OPEN]{RESET} {port} {service_name}" # Create message variabel for display results
        with lock:
            print(message)
            file.write(message + "\n")
            found = True
    s.close()


# Service Dictionary
services = {
    21 : "(FTP)",
    22 : "(SSH)",
    25 : "(SMTP)",
    53 : "(DNS)",
    80 : "(HTTP)",
    443 : "(HTTPS)"
}


if mode == "1":
    ip = input("IP Address : ")

    try:
        ip = socket.gethostbyname(ip)
    except socket.gaierror:
        print("Invalid hostname or IP")
        exit()

    try:
        port = int(input("Port : "))
    except ValueError:
        print("Bro wtf, just number please")
        exit()

    if port < 0 or port > 65535: # Validate port
        print("Invalid port")
        exit()

    file = open("results.txt", "w")
    scan_port(ip, port)
 
elif mode == "2":
    ip = input("IP Address : ")

    try:
        ip = socket.gethostbyname(ip)
    except socket.gaierror:
        print("Invalid hostname or IP")
        exit()

    try:
        start_port = int(input("Start Port : "))
        end_port = int(input("End Port : "))
    except ValueError:
        print("Bro wtf, just number please")
        exit()
    
    if start_port > end_port:
        print("Start Port must be smaller than End Port")
        exit()

    if start_port < 0 or end_port > 65535: # Validate port
        print("Invalid port")
        exit()

    file = open("results.txt", "w")

    threads = []
    
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    

else:
    print("Invalid mode")
    exit()


if found:
    print("Scan complete. Results saved to results.txt")
else:
    print("No open ports found")

end_time = time.time()

duration = end_time - start_time
print(f"Scan took {duration:.2f} seconds")

file.close()