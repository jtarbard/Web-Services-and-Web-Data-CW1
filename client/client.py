import requests

root = "http://127.0.0.1:8000/"
commands = ["register", "login", "logout", "list", "view", "average", "rate", "exit"]
print("Client Commands: ", commands)

def register():
    url = root+"register/"
    
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
    except requests.exceptions.RequestException as e:
        print("Exception Occured: ", e)


# Main loop - command line interface
while(True):
    command = input("Command: ")
    command = command.lower().strip()

    if command == "exit":
        exit()
    elif command == "register":
        register()
