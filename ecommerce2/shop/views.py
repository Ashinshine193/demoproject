from django.shortcuts import render,redirect
from .models import Category,Product
from . forms import Register_Form
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout as logouts
from django.contrib import messages


def index(request):
    return render(request,'index.html')


def home(request):
    return render(request,'home.html')

def categories(request):
    c = Category.objects.all()
    return render(request,'categories.html',{'c':c})


def products(request,id):
    c = Category.objects.get(id=id)
    p = Product.objects.filter(p_category=id)
    return render(request,'products.html',{'c':c,'p':p})


def product_details(request,id):
    pd = Product.objects.get(id=id)
    return render(request,'product_details.html',{'pd':pd})


def user_register(request):
    if (request.method=='POST'):
        form = Register_Form(request.POST)
        if(form.is_valid()):
            usr = form.cleaned_data['username']
            p = form.cleaned_data['password']
            cp = form.cleaned_data['confirm_password']
            if(p==cp):
                user = form.save(commit=False)
                user.set_password(p)
                user.save()
                return redirect('shop:user_login')
    form = Register_Form()
    return render(request,'user_register.html',{'form':form})


def user_login(request):
    if(request.method=="POST"):
        usr_name=request.POST['usr_name']
        pwd=request.POST['pwd']
        user=authenticate(username=usr_name,password=pwd)
        if user:
            login(request,user)
            return redirect('shop:home')
        else:
            messages.error(request,"Invalid Credentials")
    return render(request,'login.html',{})


def logout(request):
    logouts(request)
    return index(request)