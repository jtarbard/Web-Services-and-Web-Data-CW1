import sys
import pickle
import requests


# Register is used to allow a user to register to the service using a username, email and a password.
def register():

    if token is not None:
        print("You are currently logged in, logging you out.")
        logout()

    url = root+"user/"

    username = input("Username: ")
    email = input("Email: ")
    password1 = input("Password: ")
    password2 = input("Repeat Password: ")
    while(password1 != password2):
        password2 = input("Passwords do not match, repeat password: ")

    obj = {
        "username": username, 
        "email": email, 
        "password": password1
    }

    try:
        post = requests.post(url, obj)
        if post.ok:
            with open("url.pkl", "wb") as file:
                pickle.dump(root, file)

            print("Registration Successful, use the command 'login' to log in to the api.")
        else:
            print("Error: Request failed, status code:", post.status_code, post.reason)

    except requests.exceptions.RequestException as e:
        print("Exception Occured: ", e)


# Login is used to log in to the service.
def login():
    global token

    url = root+"api-token-auth/"

    obj = {
        "username": input("Username: "),
        "password": input("Password: ")
    }

    try:
        post = requests.post(url, obj)

        if post.ok:
            json = post.json()
            with open("token.pkl", "wb") as file:
                pickle.dump(json["token"], file)

            with open("url.pkl", "wb") as file:
                pickle.dump(root, file)

            print("Login Successful")
        else:
            print("Error: Request failed, status code:", post.status_code, post.reason)

    except requests.exceptions.RequestException as e:
        print("Exception Occured: ", e)


# Logout causes the user to logout from the current session.
def logout():
    try:
        with open("token.pkl", "wb") as file:
            pickle.dump(None, file)
        print("Logout Sucsessful.")
    except:
        print("Logout Failed.")


# List is used to view a list of all module instances and the professor(s) teaching each of them.
def list():
    url = root+"module/"
    get = requests.get(url, headers={"Authorization": "Token {}".format(token)})
    if get.ok:
        for module in get.json():

            professors = []
            for professor in module["professor"]:
                professors.append(("Professor {0}. {1} ({2})".format(professor["first_name"][0], professor["last_name"], professor["id"])))
            

            print("{:<3} {:^40} {:^4} {:^9} {:<30}".format(module["code"], module["title"], module["year"], module["semester"], professors[0]))
            
            for professor in professors[1:]:
                print("{:<3} {:^40} {:^4} {:^9} {:<30}".format("", "", "", "", professor))

    else:
        print("Error: Request failed, status code:", get.status_code, get.reason)
    

# View is used to view the rating of all professors
def view():
    global header
    url = root+"rating/view"
    get = requests.get(url, headers={"Authorization": "Token {}".format(token)})
    if get.ok:
        for rating in get.json():
            print("The rating of Professor {0}. {1} ({2}) is {3}".format(rating["first_name"][0], rating["last_name"], rating["id"], rating["avg"]["value__avg"]))
    else:
        print("Error: Request failed, status code:", get.status_code, get.reason)


# Average is used to view the average rating of a certain professor in a certain module
def average(args):

    if len(args) < 2:
        print("Missing arguments.")
        return -1

    url = root+"rating/average/"

    obj = {"module_code": args[0], "professor": args[1]}
    post = requests.post(url, obj, headers={"Authorization": "Token {}".format(token)})
    if post.ok:
        json = post.json()
        print("The raing of Professor {}. {} ({}) in module {} ({}) is {}".format(json["first_name"][0], json["last_name"], json["professor_id"], json["module_title"], json["module_code"], json["avg"]))    
    else:
        print("Error: Request failed, status code:", post.status_code, post.reason)


# Rate is used to rate the teaching of a certain professor in a certain module instance
def rate(args):
    global module

    module_result = module(args[0], args[1], args[2], args[3])
    if module_result == -1:
        return -1

    url = root+"rating/"

    obj = {
        "user": -1,
        "professor": args[0],
        "module": module_result[0]["id"],
        "value": args[4]
    }

    post = requests.post(url, obj, headers={
                         "Authorization": "Token {}".format(token)})
    if post.ok:
        print(post.json)
    else:
        print("Error: Request failed, status code:", post.status_code, post.reason)


# Module is a helper function used to obtain a module instance.
def module(professor_id, moduleCode, year, semester):
    query = "code=" + moduleCode + "&professor_id=" + \
        professor_id + "&year=" + year + "&semester=" + semester
    url = root+"module?"+query
    get = requests.get(
        url, headers={"Authorization": "Token {}".format(token)})

    if get.ok:
        return get.json()
    else:
        print("Error: Request failed, status code:", get.status_code, get.reason)
        return -1


# Ratings is a helper function to view ratings for administration purposes.
def ratings():

    url = root+"rating/"
    get = requests.get(
        url, headers={"Authorization": "Token {}".format(token)})
    if get.ok:
        print("Rating added.")
    else:
        print("Error: Request failed, status code:", get.status_code, get.reason)


# Main loop - command line interface
def main(args):
    global root
    command = args[0]
    args = args[1:]

    if root is None and not (command == "register" or command == "login"):
        print("You must login or register before using other commands.")
        return -1

    if command == "exit":
        exit()

    elif command == "commands":
        print(commands)

    elif command == "token":
        print(token)

    elif command == "register":
        if len(args) == 1:
            root = args[0]
            register()
        else:
            print("Error: Arguments incorrect for command register, 1 expected: url")

    elif command == "login":
        if len(args) == 1:
            root = args[0]
            login()
        else:
            print("Error: Arguments incorrect for command login, 1 expected: url.")

    elif command == "logout":
        logout()

    elif command == "list":
        list()

    elif command == "view":
        view()

    elif command == "average":
        if len(args) == 2:
            average(args)
        else:
            print(
                "Error: Arguments incorrect for command average, 2 expected: professor_id, module_code.")

    elif command == "rate":
        if len(args) == 5:
            rate(args)
        else:
            print("Error: Arguments incorrect for command rate, 5 expected: professor_id, module_code, year, semester, rating.")

    elif command == "ratings":
        ratings()

    else:
        print("Error: Command not found.")


if __name__ == "__main__":
    root = "http://127.0.0.1:8000/"
    commands = ["register", "login", "logout",
                "list", "view", "average", "rate", "exit"]
    token = None

    try:
        with open("token.pkl", "rb") as file:
            token = pickle.load(file)
    except:
        token = None

    try:
        with open("url.pkl", "rb") as file:
            root = pickle.load(file)
    except:
        root = None


    if len(sys.argv) > 1:
        args = sys.argv[1:]
        main(args)
    else:
        print("Command not provided. Options:", commands)
