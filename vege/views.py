from django.shortcuts import render , redirect
from .models import *

from django.contrib.auth.models import User


from django.contrib import messages

from django.contrib.auth import authenticate , login , logout


from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="/login/")
def receipes(request):
    # print("*"*50)
    if request.method == "POST":
        # print("method was a post")
        data = request.POST
        receipe_image = request.FILES.get('receipe_image')
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        # print("*"*30)
        # print(receipe_name)
        # print(receipe_description)

        Receipe.objects.create (
            receipe_image = receipe_image,
            receipe_name = receipe_name,
            receipe_description = receipe_description,
            )
        return redirect('/')
    
    queryset = Receipe.objects.all()
    
    if request.GET.get('search'):
        queryset = queryset.filter(receipe_name__icontains = request.GET.get('search'))
    
    
    context = {'receipes' : queryset}
    return render(request,'receipes.html',context)



def delete_receipe(request,id):
    queryset = Receipe.objects.get(id=id)
    queryset.delete()
    return redirect('/')



def update_receipe(request,id):
    queryset = Receipe.objects.get(id=id)

    if request.method == "POST":
        data = request.POST
        receipe_image = request.FILES.get('receipe_image')
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description
        if receipe_image : 
            queryset.receipe_image = receipe_image
        queryset.save()
        return redirect('/')
    context = {'receipe':queryset}
    return render(request,'update_receipe.html',context)




def login_page(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        username = request.POST.get('username')

        if not User.objects.filter(username=username).exists():
            messages.add_message(request, messages.INFO, "Invalid Username")
            return redirect('/login')
        
        user = authenticate(username = username , password = password)
        if user is None:
            messages.add_message(request, messages.INFO, "Invalid Password")
            return redirect('/login')
        else:
            login(request,user)
            return redirect('/')
    return render(request,'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login')



def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(first_name,username,password)

        user = User.objects.filter(username = username)
        if user.exists():

            messages.add_message(request, messages.INFO, "User Name Already exists")
            return redirect('/register')

        user = User.objects.create(
            first_name = first_name,
            username = username      
        )
        user.set_password(password)
        user.save()
        messages.add_message(request, messages.INFO, "Successfully created user")
        return redirect('/login')

    return render(request,'register.html')