from django.shortcuts import render,redirect
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required 

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        cartproduct_count=CartModel.objects.filter(host=request.user).count()
    else:
        cartproduct_count=False

     
    print(request.method)
    print(request.GET)
    no_match=False
    offer=False
    trend=False
    if 'q' in request.GET:
        q=request.GET['q']
        print(q)
        all_products=Product.objects.filter(Q(pname__icontains=q) | Q(pdesc=q))
        if len(all_products)==0:
            no_match='True'
    elif 'cat' in request.GET:
        cat=request.GET['cat']
        all_products=Product.objects.filter(pcategory=cat)
    elif 'trending' in request.GET:
        all_products=Product.objects.filter(trending=True)
        trend=True
       
    elif 'offer' in request.GET:
        all_products=Product.objects.filter(offer=True)
        offer=True
        
    else:

        all_products=Product.objects.all()


    #category
    category=[]
    a=Product.objects.all()
    for i in a:
        print(i.pcategory)
        if i.pcategory not in category:
            category+=[i.pcategory]
    print(category)
    return render(request,'home.html',{'all_products':all_products,'no_match':no_match,'category':category,'home':True,'cartproduct_count':cartproduct_count ,'trend':trend,'offer':offer})
@login_required(login_url='login_')
def addtocart(request,id):
    
    product=Product.objects.get(id=id)
    try:
        cp=CartModel.objects.get(pname=product.pname,host=request.user)#it will thorw error when the particuler product is not precsent in db
        #if produt in not peresent in cart model the prod need to be created 
        # if gett is not returing error that time we need to upadte qiantity and total price
        cp.quantity+=1
        cp.totalprice+=product.price
        cp.save()
        
    except:

        CartModel.objects.create(
            pname=product.pname,
            price=product.price,
            pcategory=product.pcategory,
            quantity=1,
            totalprice=product.price,
            host =request.user
            )
    
    return redirect('home')

def cart(request):
    cartproduct_count = CartModel.objects.filter(host=request.user).count()
    print(cartproduct_count)
    
    cartproduct=CartModel.objects.filter(host=request.user)
    TA=0
    for i in cartproduct:
        TA+=i.totalprice

    return render(request,'cart.html',{'cartproduct':cartproduct,'TA':TA,'cartproduct_count':cartproduct_count})

def  remove(request,id):
    cartproduct=CartModel.objects.get(id=id)
    cartproduct.delete()
    return redirect('cart')


def increment(request,id):
    cartproduct=CartModel.objects.get(id=id)
    cartproduct.quantity+=1
    cartproduct.totalprice+=cartproduct.price
    cartproduct.save()
    return redirect('cart')

def decrement(request,id):
    cartproduct=CartModel.objects.get(id=id)
    if cartproduct.quantity>1:
        cartproduct.quantity-=1
        cartproduct.totalprice-=cartproduct.price
        cartproduct.save()
    else:
         cartproduct.delete()
    return redirect('cart')
