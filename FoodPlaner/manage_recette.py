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

def get_relative_img(recettes:dict, recettes_favorites:dict, recettes_creation:dict, link_image:str) -> str:
    """Return the relative path of the image"""
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

def retirer_path_img(recettes:dict, recettes_favorites:dict, recettes_creation:dict) -> str:
    """Return the relative path of the image"""
    for recette in recettes:
        if "static/img/recettes/" in recettes[recette]["img"]:
            recettes[recette]['img'] = recettes[recette]["img"].split("/")[-1]

    for recette in recettes_favorites:
        if "static/img/recettes/" in recettes_favorites[recette]["img"]:
            recettes_favorites[recette]['img'] = recettes_favorites[recette]["img"].split("/")[-1]

    for recette in recettes_creation:
        if "static/img/recettes/" in recettes_creation[recette]["img"]:
            recettes_creation[recette]['img'] = recettes_creation[recette]["img"].split("/")[-1]


def sup_fav(username:str, recette:str, users:dict, file:str):
    """Remove the recipe from the favorites"""
    users[username]["recettes_favorites"].pop(recette)
    if recette in users[username]["recettes_creation"]:
        users[username]["recettes_creation"][recette]["liked"] = False
    save_json(file, users)

def add_fav(username:str, recette:str, recettes:dict, users:dict, users_file):
    """Add the recipe to the favorites"""
    users[username]["recettes_favorites"][recette] = recettes[recette]
    users[username]["recettes_favorites"][recette]["liked"] = True
    if recette in users[username]["recettes_creation"]:
        users[username]["recettes_creation"][recette]["liked"] = True
    save_json(users_file, users)

def sup_recette(username:str, recette:str, users_file:str, recettes_file:str):
    """Remove the recipe"""
    users = open_json(users_file)
    recettes = open_json(recettes_file)
    del users[username]["recettes_creation"][recette]
    del recettes[recette]
    save_json(users_file, users)
    save_json(recettes_file, recettes)

def add_planning(recette, day, username:str, users_file:str, recettes_file:str):
    """Add the recipe to the planning"""
    users = open_json(users_file)
    if recette not  in users[username]["planning"][day]:
        users[username]["planning"][day].append(recette)
    save_json(users_file, users)

def cree_recette(nom, author, ingredients, derouler, img, users_file:str, recettes_file:str):
    """cree une nouvelle recette"""
    recettes = open_json(recettes_file)
    users = open_json(users_file)
    # get the last id of the recettes dict and add 1
    len_recettes = len(recettes)
    id = str(int(list(recettes.keys())[len_recettes-1]) + 1)
    
    recette = {
        "id": id,
        "nom": nom,
        "author": author,
        "ingredients": ingredients,
        "derouler": derouler,
        "img": img
    }
    recettes[id] = recette
    users[author]["recettes_creation"][id] = recette
    save_json(recettes_file, recettes)
    save_json(users_file, users)

