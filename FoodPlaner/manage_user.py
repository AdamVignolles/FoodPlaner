# programer par Adam
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

def logout_user(request):
    """Logout the user"""
    request.COOKIES["username"] = ""

def change_password(request, username:str, users:dict, file:str) -> bool or str:
    """Change the password of the user"""
    old_password = request.POST.get("old_password")
    new_password = request.POST.get("new_password")
    new_password_repeat = request.POST.get("new_password2")
    if old_password == users[username]["password"]:
        if new_password == new_password_repeat:
            users[username]["password"] = new_password
            save_json(file, users)
            return True
        else:
            return "The passwords are not the same"
    else:
        return "The old password is wrong"

def delete_account(request, username:str, users:dict, file:str):
    """Delete the account of the user"""
    password = request.POST.get("password")
    if password == users[username]["password"]:
        del users[username]
        save_json(file, users)
        return True
    else:
        return "The password is wrong"