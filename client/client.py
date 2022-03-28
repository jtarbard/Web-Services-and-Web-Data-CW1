import sys
import pickle
import requests

def list():
    url = root+"module/"
    get = requests.get(url, headers={"Authorization": "Token {}".format(token)})
    for module in get.json():
        print(module.values())


def view():
    global header
    url = root+"rating/view"
    get = requests.get(url, headers={"Authorization": "Token {}".format(token)})
    if get.ok:
        for rating in get.json():
            print(rating.values())
    else:
        print(get.json())


def average(args):
    url = root+"rating/average"

    obj = {"module_code": args[0], "professor_id": args[1]}
    get = requests.get(url, obj, headers={"Authorization": "Token {}".format(token)})

    print(get.json())


def module(professor_id, moduleCode, year, semester):
    query = "code=" + moduleCode + "&professor_id=" + professor_id + "&year=" + year + "&semester=" + semester
    url = root+"module?"+query
    get = requests.get(url, headers={"Authorization": "Token {}".format(token)})

    if get.ok:
        return get.json()
    else:
        return -1


def rate(args):
    global module
    if len(args) < 5:
        return "Missing arguments."
    
    module_result = module(args[0], args[1], args[2], args[3])
    if module_result == -1:
        print("Module not found.")
        return -1

    url = root+"rating/"

    obj = {
        "user": -1,
        "professor": args[0], 
        "module": module_result[0]["id"],
        "value": args[4]
    }
    print(obj)

    post = requests.post(url, obj, headers={"Authorization": "Token {}".format(token)})
    json = post.json()
    print(json)


def logout():
    try:
        with open("token.pkl", "wb") as file:
            pickle.dump(None, file)
        print("Logout Sucsessful.")
    except:
        print("Logout Failed.")


def login(args):
    global token
    
    if len(args) < 2:
        print("Missing arguments.")
        return -1

    url = root+"api-token-auth/"

    obj = {"username": args[0], "password": args[1]}

    try:
        post = requests.post(url, json = obj)

        if post.ok:
            json = post.json()
            with open("token.pkl", "wb") as file:
                pickle.dump(json["token"], file)

            print("Login Successful")
        else:
            print("Login Failed, HTTPs Error:", post.status_code)

    except requests.exceptions.RequestException as e:
        print("Exception Occured: ", e)


def register(username, email, password):
    
    if len(args) < 3:
        return "Missing arguments."

    url = root+"user/register"

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
def main(args):
    command = args[0]
    args = args[1:]

    if command == "exit":
        exit()
    elif command == "token":
        print(token)
    elif command == "register":
        register(args)
    elif command == "login":
        login(args)
    elif command == "logout":
        logout()
    elif command == "list":
        list()
    elif command == "view":
        view()
    elif command == "average":
        average(args)
    elif command == "rate":
        rate(args)
    else:
        print("Error: Command not found.")


if __name__ == "__main__":
    root = "http://127.0.0.1:8000/"
    commands = ["register", "login", "logout", "list", "view", "average", "rate", "exit"]
    token = None

    try:
        with open("token.pkl", "rb") as file:
            token = pickle.load(file)
    except:
        token = None

    if len(sys.argv) > 1:
        args = sys.argv[1:]
        main(args)
    else:
        print("Command not provided. Options:", commands)