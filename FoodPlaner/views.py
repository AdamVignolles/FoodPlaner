from django.shortcuts import redirect, render
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
            return redirect("/user")
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
                    return redirect("/user")
                
            return render(request, "FoodPlaner/Loggin/index.html", {"error_loggin": "Email or password incorrect"})

        

    else:
        return render(request, "FoodPlaner/Loggin/index.html")
    
def user(request):
    return render(request, "FoodPlaner/User/index.html")