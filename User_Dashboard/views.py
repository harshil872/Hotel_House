from django.shortcuts import render,redirect
from .froms import ContactForm


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
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact')   # or show success message
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})
