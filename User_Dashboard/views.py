from django.shortcuts import render

def index(request):
    return render(request, "index.html")

def menu(request):
    return render(request, "menu.html")

def reservations(request):
    return render(request, "reservations.html")

def gallery(request):
    return render(request, "gallery.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")
