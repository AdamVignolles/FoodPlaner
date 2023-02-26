from django.shortcuts import redirect, render

def acceuil(request):
    return render(request, "FoodPlaner/Acceuil/index.html")

def loggin(request):
    return render(request, "FoodPlaner/Loggin/index.html")