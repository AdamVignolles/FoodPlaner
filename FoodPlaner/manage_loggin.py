#Programer par Adam
import json

def open_json( file:str ) -> dict:
    """Open a json file and return the data as a dict"""
    with open(file, "r") as json_file:
        data = json.load(json_file)
    return data

def save_json( file:str, data:dict ):
    """Save a dict as a json file"""
    with open(file, "w") as json_file:
        json.dump(data, json_file)

def create_sign_up(request, file:str) -> bool or str:
    """sign up the new user"""
    username = str(request.POST["txt"])
    email = str(request.POST["email"])
    password = str(request.POST["pswd"])

    users = open_json(file)

    if username in users:
        return (False, "Username already exists")
    for user in users:
        if users[user]["email"] == email:
            return (False, "Email already exists")
    
    users[username] = {"email": email, "password": password, 'loggin': True, "username": username, "avatar": "basic.png", "planning": {"lundi": [], "mardi": [], "mercredi": [], "jeudi": [], "vendredi": [], "samedi": [], "dimanche": []},"recettes_favorites": {}, "recettes_creation":{}}

    save_json(file, users)
    return (True, username)

def login_user(request, file:str) -> bool or str:
    """Login the user"""
    email = str(request.POST["email"])
    password = str(request.POST["pswd"])

    users = open_json(file)

    for user in users:
        if users[user]["email"] == email:
            if users[user]["password"] == password:
                users[user]["loggin"] = True
                save_json(file, users)
                return (True, users[user]["username"])
            else:
                return (False, "Wrong password")
    return (False, "Wrong email")


