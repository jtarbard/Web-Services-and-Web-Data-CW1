import requests

root = "http://127.0.0.1:8000/"
commands = ["register", "login", "logout", "list", "view", "average", "rate", "exit"]
print("Client Commands: ", commands)
token = None

def checkToken():
    print(token)

def register():
    url = root+"user/"
    
    username = input("Username: ")
    email = input("Email: ")
    password = input("Password: ")

    obj = {"username": username, "email": email, "password": password}

    try:
        post = requests.post(url, json = obj)
        if post.status_code != 201:
            print("Error Occured: ", post.text)
        else:
            print("Registration Successful")
            login(obj)

            
    except requests.exceptions.RequestException as e:
        print("Exception Occured: ", e)


def login(obj = None):
    global token
    url = root+"login/"
    
    if obj == None:
        username = input("Username: ")
        password = input("Password: ")

        obj = {"username": username, "password": password}

    try:
        post = requests.post(url, json = obj)
        json = post.json()
        if "token" in json.keys():
            token = json["token"]
            print("Login Successful")
        else:
            print("Login Failed", post)

    except requests.exceptions.RequestException as e:
        print("Exception Occured: ", e)

def logout():
    global token
    token = None
    print("Logout Successful")

def list():
    url = root+"module/"
    post = requests.get(url)
    for module in post.json():
        print(module.values())

# Main loop - command line interface
while(True):
    command = input("Command: ")
    command = command.lower().strip()

    if command == "exit":
        exit()
    elif command == "token":
        checkToken()
    elif command == "register":
        register()
    elif command == "login":
        login()
    elif command == "logout":
        logout()
    elif command == "list":
        list()
    else:
        print("Error: Command not found.")
