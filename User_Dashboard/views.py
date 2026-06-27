from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm, LoginForm

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

def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("index")

        form.add_error(None, "Invalid username or password.")

    return render(request, "login.html", {
        "form": form
    })

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login_view(request, user)

            return redirect("index")

    else:

        form = RegisterForm()

    return render(request, "register.html", {
        "form": form
    })
