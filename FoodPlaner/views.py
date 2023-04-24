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
            users[username] = {"email": email, "password": password, 'loggin': True, "username": username, "avatar": "basic.png", "planning": {"lundi": [], "mardi": [], "mercredi": [], "jeudi": [], "vendredi": [], "samedi": [], "dimanche": []},"recettes_favorites": {}, "recettes_creation":{}}

            with open(f"{BASE_DIR}\\static\\json\\users.json", "w") as file:
                json.dump(users, file)

            response = redirect("/planning")
            response.set_cookie("username", user["username"])
            
            return response
                    
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

                        response = redirect("/planning")
                        response.set_cookie("username", user["username"])
                    
                        return response
                    

                return render(request, "FoodPlaner/Loggin/index.html", {"error_loggin": "Email or password incorrect", "email": email})
            
    else:
        return render(request, "FoodPlaner/Loggin/index.html")
    
def user(request, user=None):

    user = request.COOKIES['username']

    with open(f"{BASE_DIR}\\static\\json\\users.json", "r") as file:
        users = json.load(file)

    if request.method == "POST":
               
        
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

    

    return render(request, "FoodPlaner/User/index.html", {"username": user, "email": users[user]["email"], "error": False})

def planning(request, user=None):

    with open(f"{BASE_DIR}\\static\\json\\users.json", "r") as file:
        users = json.load(file)

    with open(f"{BASE_DIR}\\static\\json\\recettes.json", "r") as file:
        recettes = json.load(file)

    username = request.COOKIES['username']


    


    for user in users:
        if users[user]["username"] == username:
            user = users[user]

            path = settings.STATIC_URL + "img/avatar"
            img_list = os.listdir(BASE_DIR + path + "/")
            base_image = "http://127.0.0.1:8000/static/img/avatar/" + img_list[1]
            link_image = "http://127.0.0.1:8000/static/img/"
            recettes_favorites = user["recettes_favorites"]
            recettes_creation = user["recettes_creation"]
            lundi=[]
            mardi=[]
            mercredi=[]
            jeudi=[]
            vendredi=[]
            samedi=[]
            dimanche=[]


            for recette in recettes:
                if not "static/img/" in recettes[recette]["img"]:
                    recettes[recette]['img'] = link_image + recettes[recette]["img"]

                if recette in recettes_favorites:recettes[recette]["liked"] = True
                else:recettes[recette]["liked"] = False

            for recette in recettes_favorites:
                if not "static/img/" in recettes_favorites[recette]["img"]:
                    recettes_favorites[recette]['img'] = link_image + recettes_favorites[recette]["img"]
            for recette in recettes_creation:
                if not "static/img/" in recettes_creation[recette]["img"]:
                    recettes_creation[recette]['img'] = link_image + recettes_creation[recette]["img"]

                if recette in recettes_favorites:recettes_creation[recette]["liked"] = True
                else:recettes_creation[recette]["liked"] = False
            

            for jour in user["planning"] : 
                if user["planning"][jour] != []:
                    for i in user["planning"][jour]:
                        if i in recettes:
                            if jour == "lundi": lundi.append(recettes[i])
                            elif jour == "mardi": mardi.append(recettes[i])
                            elif jour == "mercredi": mercredi.append(recettes[i])
                            elif jour == "jeudi": jeudi.append(recettes[i])
                            elif jour == "vendredi": vendredi.append(recettes[i])
                            elif jour == "samedi": samedi.append(recettes[i])
                            elif jour == "dimanche": dimanche.append(recettes[i])
                print(lundi)



            if request.method == "POST":
                    if "supfav" in request.POST:
                        recette = request.POST.get("supfav")
                        
                        del user["recettes_favorites"][str(recette)]
                        if recette in user["recettes_creation"]:
                            recettes_creation[recette]["liked"] = False
                        with open(f"{BASE_DIR}\\static\\json\\users.json", "w") as file:
                            json.dump(users, file)
                    if "addfav" in request.POST:
                        recette = request.POST.get("addfav")
                        user["recettes_favorites"][str(recette)] = user["recettes_creation"][str(recette)]

                        print(user["recettes_favorites"])
                        with open(f"{BASE_DIR}\\static\\json\\users.json", "w") as file:
                            json.dump(users, file)

                    if "cree_recette" in request.POST:
                        nom_recette = request.POST.get("nom_recette")
                        author = user["username"]
                        ingredients = request.POST.get("ingredients").split("\r\n")
                        derouler = request.POST.get("derouler").split("\r\n")
                        img = request.POST.get("img")

                        # download image
                        if img != "":
                            image_file = request.FILES.get("img")
                            with open(f'{BASE_DIR}\\static\\img', 'w') as destination:
                                for chunk in image_file.chunks():
                                    destination.write(chunk)
                            img = image_file.name

                        else:
                            img = "meal.png"
                        id =str(int(recettes[str(len(recettes))]["id"]) + 1)
                        recette = {"id": id, "nom": nom_recette, "author": author, "ingredients": ingredients, "derouler": derouler, "img": img}
                        recettes[id] = recette
                        recettes_creation[id] = recette
                        with open(f"{BASE_DIR}\\static\\json\\users.json", "w") as file:
                            json.dump(users, file)
                        with open(f"{BASE_DIR}\\static\\json\\recettes.json", "w") as file:
                            json.dump(recettes, file)
                    if "sup_recette" in request.POST:
                        recette = request.POST.get("sup_recette")
                        del recettes[recette]
                        del recettes_creation[recette]
                        with open(f"{BASE_DIR}\\static\\json\\recettes.json", "w") as file:
                            json.dump(recettes, file)
                        with open(f"{BASE_DIR}\\static\\json\\users.json", "w") as file:
                            json.dump(users, file)
                    if "search_recette" in request.POST:
                        search = request.POST.get("search")
                        recettes = {}
                        for recette in recettes_creation:
                            if search.lower() in recettes_creation[recette]["nom"].lower() or search.lower() in recettes_creation[recette]["author"].lower():
                                recettes[recette] = recettes_creation[recette]
                    if "add_planning" in request.POST:
                        recette = request.POST.get("add_planning")
                        # add key att dict
                        user["planning"][request.POST.get("day")].append(recette)
                        with open(f"{BASE_DIR}\\static\\json\\users.json", "w") as file:
                            json.dump(users, file)


            for recette in recettes:
                if not "static/img/" in recettes[recette]["img"]:
                    recettes[recette]['img'] = link_image + recettes[recette]["img"]

                if recette in recettes_favorites:recettes[recette]["liked"] = True
                else:recettes[recette]["liked"] = False

            for recette in recettes_favorites:
                if not "static/img/" in recettes_favorites[recette]["img"]:
                    recettes_favorites[recette]['img'] = link_image + recettes_favorites[recette]["img"]
            for recette in recettes_creation:
                if not "static/img/" in recettes_creation[recette]["img"]:
                    recettes_creation[recette]['img'] = link_image + recettes_creation[recette]["img"]

                if recette in recettes_favorites:recettes_creation[recette]["liked"] = True
                else:recettes_creation[recette]["liked"] = False
                    


            content =  {"base_image": base_image, "username": user, "recettes_favorites": recettes_favorites, "recettes_creation": recettes_creation, "recette_recherche": recettes, "Lundi":lundi, "Mardi":mardi, "Mercredi":mercredi,"Jeudi":jeudi, "Vendredi":vendredi, "Samedi":samedi, "Dimanche":dimanche} 
            return render(request, "FoodPlaner/Planning/index.html", content)
            
            
            
