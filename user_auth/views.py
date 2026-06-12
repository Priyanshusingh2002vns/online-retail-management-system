from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from base.models import CartModel
# Create your views here.

def login_(request):

    print(request.method)
    print(request.POST)

    if request.method =='POST':
        user=request.POST['username']

        password=request.POST['password']

        u=authenticate(username=user,password=password)
        print(u)
        if u:
            login(request,u)
            return redirect('home')
        else:
            return render(request,'login_.html',{'error':'incorrect password or username'})



    return render(request,'login_.html')


def register(request):

    print(request.method)
    print(request.POST)

    if request.method == 'POST':
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        try:
            v=User.objects.get(username=username)
            return render(request,'register.html',{'status':'username is already exists'})
        except:
            u=User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username
                                
                    )
            u.set_password(password)
            u.save()


    return render(request,'register.html')

@login_required(login_url='login_')
def profile(request):
    cartproduct_count=CartModel.objects.filter(host=request.user).count()
    return render(request,'profile.html',{'cartproduct_count':cartproduct_count})





@login_required(login_url='login_')
def logout_(request):
    logout(request)
    return redirect('login_')
@login_required(login_url='login_')
def reset(request):
    if 'oldpass' in request.POST:
        oldpass=request.POST['oldpass']
        e=authenticate(username=request.user.username,password=oldpass)
        if e:
            return render(request,'reset.html',{'new_pass':True})
        else:
            return render(request,'reset.html',{'error':'incorrect old password'})
    if 'newpass' in request.POST:
        newpass=request.POST['newpass']
        if request.user.check_password(newpass):
            return render(request,'reset.html',{'error':'old pass and new pass csnnot be same'})
        request.user.set_password(newpass)
        request.user.save()
        return redirect('login_')
    
    return render(request,'reset.html')

def forget(request):
    if request.method=='POST':
        username=request.POST['fuser']
        try:
            u=User.objects.get(username=username)
            request.session['fp_user']= u.username
            print(u)
            return redirect('new_password')
        except:
            return render(request,'forget.html',{'error':'user not found'})

    return render(request,'forget.html')
def new_password(request):
    username=request.session.get('fp_user')
    if username is None:
        return redirect('forget')
    user=User.objects.get(username=username)
    if request.method == 'POST':
        new =request.POST['new_password']
        if user.check_password(new):
            return render(request,'new_password.html',{'error':True})
        user.set_password(new)
        user.save()
        print(new)
        del request.session['fp_user']
        return redirect('login_')
    

    return render(request,'new_password.html')


'''
wrute the logic page
register
login
profile
logout
reset password
forgot password
'''



