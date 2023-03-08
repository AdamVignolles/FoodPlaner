from django.shortcuts import redirect, render
from django.conf import settings
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def acceuil(request):
    return render(request, "FoodPlaner/Acceuil/index.html")

def loggin(request):
    if request.method == "POST":

        if "txt" in request.POST.keys():
            username = str(request.POST["txt"])
            email = str(request.POST["email"])
            password = str(request.POST["pswd"])

            # create a new account in json file
            with open(f"{BASE_DIR}\\static\\json\\users.json", "r") as file:
                users = json.load(file)
            # check email and username are not already used
            for user in users:
                user = users[user]
                if user["email"] == email or user["username"] == username:
                    return render(request, "FoodPlaner/Loggin/index.html", {"error_sign_up": "Email or username already used"})
            # add the new user
            users[username] = {"email": email, "password": password, 'loggin': True, "username": username, "avatar": "basic.png"}

            with open(f"{BASE_DIR}\\static\\json\\users.json", "w") as file:
                json.dump(users, file)

            return planning(request, user=username)
        else : 
            if "email" in request.POST.keys() and "pswd" in request.POST.keys():
                email = str(request.POST["email"])
                password = str(request.POST["pswd"])

                # check if the email and password are correct
                with open(f"{BASE_DIR}\\static\\json\\users.json", "r") as file:
                    users = json.load(file)

                for user in users:
                    user = users[user]
                    if user["email"] == email and user["password"] == password:
                        user["login"] = True
                    return planning(request, user=user["username"])
                    
                return render(request, "FoodPlaner/Loggin/index.html", {"error_loggin": "Email or password incorrect"})

    else:
        return render(request, "FoodPlaner/Loggin/index.html")
    
def user(request, user=None):

    if request.method == "POST":
        if user != None:
            if request.POST.get("logout") == "logout":
                with open(f"{BASE_DIR}\\static\\json\\users.json", "r") as file:
                    users = json.load(file)
                users[user]["loggin"] = False
                with open(f"{BASE_DIR}\\static\\json\\users.json", "w") as file:
                    json.dump(users, file)
                return redirect("/")
        if "user" in request.POST:
            current_user = request.POST.get("user")
            return render(request, "FoodPlaner/User/index.html", {"username": current_user})

    return render(request, "FoodPlaner/User/index.html", {"username": user})

def planning(request, user=None):

    with open(f"{BASE_DIR}\\static\\json\\users.json", "r") as file:
        users = json.load(file)

    if user != None and users[user]["loggin"]:

        path = settings.STATIC_URL + "img/avatar"

        img_list = os.listdir(BASE_DIR + path + "/")
        base_image = "http://127.0.0.1:8000/static/img/avatar/" + img_list[1]
        content = {"base_image": base_image, "username": user}
        return render(request, "FoodPlaner/Planning/index.html", content)
    
    
    else:
        return redirect("/loggin")
    
