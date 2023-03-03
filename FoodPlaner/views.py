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
            users[username] = {"email": email, "password": password}

            with open(f"{BASE_DIR}\\static\\json\\users.json", "w") as file:
                json.dump(users, file)

            # retourner a la page d'acceuil
            return redirect("/planning")
        else : 
            email = str(request.POST["email"])
            password = str(request.POST["pswd"])

            # check if the email and password are correct
            with open(f"{BASE_DIR}\\static\\json\\users.json", "r") as file:
                users = json.load(file)

            for user in users:
                user = users[user]
                if user["email"] == email and user["password"] == password:
                    # retourner a la page d'acceuil
                    return redirect("/planning")
                
            return render(request, "FoodPlaner/Loggin/index.html", {"error_loggin": "Email or password incorrect"})

        

    else:
        return render(request, "FoodPlaner/Loggin/index.html")
    
def user(request):
    return render(request, "FoodPlaner/User/index.html")

def planning(request):
    path = settings.STATIC_URL + "img/avatar"

    img_list = os.listdir(BASE_DIR + path + "/")
    print(img_list[0])
    base_image = "http://127.0.0.1:8000/static/img/avatar/" + img_list[1]
    content = {"base_image": base_image}
    return render(request, "FoodPlaner/Planning/index.html", content)

def recette(request):
    return render(request, "FoodPlaner/Recette/index.html")