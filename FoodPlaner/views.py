from django.http import HttpResponse
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
            users[username] = {"email": email, "password": password, 'loggin': True, "username": username, "avatar": "basic.png", "recettes_favorites": {}, "recettes_creation":{}}

            with open(f"{BASE_DIR}\\static\\json\\users.json", "w") as file:
                json.dump(users, file)

            response = render(request, "FoodPlaner/Planning/index.html", {"username": username})
            response.set_cookie("username", user["username"])
            return redirect("/planning")
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

                    response = render(request, "FoodPlaner/Planning/index.html", {"username": user["username"]})
                    response.set_cookie("username", user["username"])
                    return redirect("/planning")
                    

                return render(request, "FoodPlaner/Loggin/index.html", {"error_loggin": "Email or password incorrect", "email": email})
            

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
            with open(f"{BASE_DIR}\\static\\json\\users.json", "r") as file:
                users = json.load(file)
            current_user = request.POST.get("user")
            return render(request, "FoodPlaner/User/index.html", {"username": current_user, "error": False,"email": users[current_user]["email"]})
        if "logout" in request.POST:
            return redirect("/")
        if "change_password" in request.POST:
            with open(f"{BASE_DIR}\\static\\json\\users.json", "r") as file:
                users = json.load(file)
            user = request.POST.get("change_password").split(" ")[1]
            if request.POST.get("old_password") == users[user]["password"]:
                if request.POST.get("new_password") != request.POST.get("new_password2"):
                    return render(request, "FoodPlaner/User/index.html", {"username": user, "email": users[user]["email"], "error": True, "error_password": "The new password is not the same"})
                else:
                    users[user]["password"] = request.POST.get("new_password")
                    with open(f"{BASE_DIR}\\static\\json\\users.json", "w") as file:
                        json.dump(users, file)
                return render(request, "FoodPlaner/User/index.html", {"username": user, "email": users[user]["email"], "error": False, "password_changed": True})
            else:
                return render(request, "FoodPlaner/User/index.html", {"username": user, "email": users[user]["email"], "error": True, "error_password": "The old password is incorrect"})
        if "delete_account" in request.POST:
            with open(f"{BASE_DIR}\\static\\json\\users.json", "r") as file:
                users = json.load(file)
            user = request.POST.get("delete_account")
            if request.POST.get("password") == users[user]["password"]:
                del users[user]
                with open(f"{BASE_DIR}\\static\\json\\users.json", "w") as file:
                    json.dump(users, file)
                return redirect("/")
            else:
                return render(request, "FoodPlaner/User/index.html", {"username": user, "email": users[user]["email"], "error": True, "error_password": "The password is incorrect"})
                
    return render(request, "FoodPlaner/User/index.html", {"username": user})

def planning(request, user=None):

    with open(f"{BASE_DIR}\\static\\json\\users.json", "r") as file:
        users = json.load(file)

    username = request.COOKIES['username']
    for user in users:
        if users[user]["username"] == username:
            user = users[user]
            if request.method == "POST":
                    if "supfav" in request.POST:
                        recette = request.POST.get("supfav")
                        
                        del user["recettes_favorites"][str(recette)]
                        with open(f"{BASE_DIR}\\static\\json\\users.json", "w") as file:
                            json.dump(users, file)

            path = settings.STATIC_URL + "img/avatar"

            img_list = os.listdir(BASE_DIR + path + "/")
            base_image = "http://127.0.0.1:8000/static/img/avatar/" + img_list[1]
            link_image = "http://127.0.0.1:8000/static/img/"
            recettes_favorites = user["recettes_favorites"]
            recettes_creation = user["recettes_creation"] 
            for recette in recettes_favorites:
                recettes_favorites[recette]['img'] = link_image + recettes_favorites[recette]["img"]
            for recette in recettes_creation:
               recettes_creation[recette]['img'] = link_image + recettes_creation[recette]["img"]
            content = {"base_image": base_image, "username": user, "recettes_favorites": recettes_favorites, "recettes_creation": recettes_creation}


            
            return render(request, "FoodPlaner/Planning/index.html", content)
            
            
            
