from django.shortcuts import redirect, render
from django.conf import settings
import os
import FoodPlaner.manage_user as mu
import FoodPlaner.manage_loggin as ml
import FoodPlaner.manage_recette as mr


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def acceuil(request):
    return render(request, "FoodPlaner/Acceuil/index.html")

def loggin(request):
    if request.method == "POST":

        user_file = f"{BASE_DIR}\\static\\json\\users.json"

        if "txt" in request.POST.keys():
            
            reponse = ml.create_sign_up(request, user_file)

            if reponse[0] == True:

                response = redirect("/planning")
                response.set_cookie("username", reponse[1])
                return response
        
            else:
                return render(request, "FoodPlaner/Loggin/index.html", {"error_sign_up": reponse[1]})
             
        else : 
            if "email" in request.POST.keys() and "pswd" in request.POST.keys():
                
                reponse = ml.login_user(request, user_file)

                if reponse[0] == True:

                    response = redirect("/planning")
                    response.set_cookie("username", reponse[1])
                    return response

                else:

                    return render(request, "FoodPlaner/Loggin/index.html", {"error_loggin": reponse[1]})
            
    else:
        return render(request, "FoodPlaner/Loggin/index.html")
    
def user(request, user=None):

    user = request.COOKIES['username']
    user_file = f"{BASE_DIR}\\static\\json\\users.json"
    users = mu.open_json(user_file)

    if request.method == "POST":
        
        if "logout" in request.POST:

            mu.logout_user(request)
            return redirect("/")
        
        if "change_password" in request.POST:

            reponse = mu.change_password(request, user, users, user_file)
            if reponse == True:
                return render(request, "FoodPlaner/User/index.html", {"username": user, "email": users[user]["email"], "error": False, "password_changed": True})
            else:
                return render(request, "FoodPlaner/User/index.html", {"username": user, "email": users[user]["email"], "error": True, "error_password": reponse})
            
        if "delete_account" in request.POST:
            
            reponse = mu.delete_account(request, user, users, user_file)
            if reponse == True:
                return redirect("/")
            else:
                return render(request, "FoodPlaner/User/index.html", {"username": user, "email": users[user]["email"], "error": True, "error_password": reponse})

    

    return render(request, "FoodPlaner/User/index.html", {"username": user, "email": users[user]["email"], "error": False})

def planning(request, user=None):

    username = request.COOKIES['username']

    user_file = f"{BASE_DIR}\\static\\json\\users.json"
    users = mu.open_json(user_file)

    recettes_file = f"{BASE_DIR}\\static\\json\\recettes.json"
    recettes = mr.open_json(recettes_file)

    user = users[username]
    
    # gestion des path vers les images
    path = "http://" + settings.ALLOWED_HOSTS[0] + ":8000" 
    path_static = settings.STATIC_URL + "img/avatar/"
    img_list = os.listdir(BASE_DIR + path_static + "/")
    base_image = path + "/static/img/avatar/" + img_list[1]
    link_image = path + "/static/img/"

    recettes_favorites = user["recettes_favorites"]
    recettes_creation = user["recettes_creation"]

    mr.retirer_path_img(recettes, recettes_favorites, recettes_creation)
    mr.get_relative_img(recettes, recettes_favorites, recettes_creation, link_image)
    

    lundi, mardi, mercredi, jeudi, vendredi, samedi, dimanche = {}, {}, {}, {}, {}, {}, {}

    for jour in user["planning"] : 
        if user["planning"][jour] != []:
            for i in user["planning"][jour]:
                if i in recettes:
                    if jour == "lundi": lundi[i] = recettes[i]
                    elif jour == "mardi": mardi[i] = recettes[i]
                    elif jour == "mercredi": mercredi[i] = recettes[i]
                    elif jour == "jeudi": jeudi[i] = recettes[i]
                    elif jour == "vendredi": vendredi[i] = recettes[i]
                    elif jour == "samedi": samedi[i] = recettes[i]
                    elif jour == "dimanche": dimanche[i] = recettes[i]

    if request.method == "POST":
            
            if "supfav" in request.POST:
                recette = request.POST.get("supfav")
                mr.sup_fav(username, recette, users, user_file)

            if "addfav" in request.POST:
                recette = request.POST.get("addfav")
                mr.add_fav(username, recette, recettes, users, user_file)

            if "cree_recette" in request.POST:
                nom_recette = request.POST.get("nom_recette")
                author = user["username"]
                ingredients = request.POST.get("ingredients").split("\r\n")
                derouler = request.POST.get("derouler").split("\r\n")
                img = request.POST.get("img")

                # download image
                if img != "":
                    image_file = request.FILES.get("img")
                    img = image_file.name
                    with open(f'{BASE_DIR}\\static\\img\\recettes\\{img}', 'wb+') as destination:
                        for chunk in image_file.chunks():
                            destination.write(chunk)
                    

                else:
                    img = "meal.png"

                mr.cree_recette(nom_recette, author, ingredients, derouler, img, user_file, recettes_file)

            if "sup_recette" in request.POST:
                recette = request.POST.get("sup_recette")
                mr.sup_recette(username, recette, user_file, recettes_file)

            if "search_recette" in request.POST:
                search = request.POST.get("search")
                recettes = {}
                for recette in recettes_creation:
                    if search.lower() in recettes_creation[recette]["nom"].lower() or search.lower() in recettes_creation[recette]["author"].lower():
                        recettes[recette] = recettes_creation[recette]

            if "add_planning" in request.POST:
                recette = request.POST.get("add_planning")
                jour = request.POST.get("day")
                print(recette, jour, username, user_file, recettes_file)
                mr.add_planning(recette, jour, username, user_file, recettes_file)

    
    #emepcher les formulaire de se renvoier quand on rafraichit la page
    if request.method == "POST":
        return redirect("/planning")

    mr.get_relative_img(recettes, recettes_favorites, recettes_creation, link_image)
            
    content =  {"base_image": base_image, "username": user, "recettes_favorites": recettes_favorites, "recettes_creation": recettes_creation, "recette_recherche": recettes, "Lundi":lundi, "Mardi":mardi, "Mercredi":mercredi,"Jeudi":jeudi, "Vendredi":vendredi, "Samedi":samedi, "Dimanche":dimanche} 
    return render(request, "FoodPlaner/Planning/index.html", content)
    
    
    
