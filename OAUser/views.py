from OAUser.models import OAUser
from django.shortcuts import render, HttpResponseRedirect
import hashlib

# Create your views here.
def index(request):
    return render(request, "index.html")

def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    password = md5.hexdigest()
    return str(password)

def register(request):
    if request.method=="POST" and request.POST:
        data=request.POST
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        OAUser.objects.create(
            username=username,
            email=email,
            password=setPassword(password)
        )
        return HttpResponseRedirect('/login/')
    return render(request, 'register.html')

def login(request):
    if request.method=="POST" and request.POST:
        data = request.POST
        email = data.get("email")
        password = data.get("password")
        e = OAUser.objects.filter(email=email).first()
        if e:
            now_password = setPassword(password)
            true_password = e.password
            if now_password==true_password:
                respone=HttpResponseRedirect('/index/')
                respone.set_cookie("username", e.username)
                print("密码正确")
                return respone
            else:
                print("Password error.")
        else:
            print("{} is not registered.".format(email))
    return render(request, "login.html")

def userValid(fun):
    def inner(request, *args, **kwargs):
        username = request.COOKIES.get("username")
        if username:
            return fun(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/login/')
    return inner

def logout(request):
    response = HttpResponseRedirect('/login/')
    response.delete_cookie("username")
    return response