from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from restoapp.models import dish,Cart,Order,Contact

from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail
# Create your views here
def home(request):
     
     return render(request,"index.html")

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method=="POST":
       uname=request.POST['uname']
       uemail=request.POST['uemail']
       umsgs=request.POST['umsgs']
       context={}
       if uname=="" or uemail=="" or umsgs=="":
            context['errmsg']="Feilds cannot be empty"
            return render(request,"contact.html",context)
       else:
            u=Contact.objects.create(uname=uname,uemail=uemail,umsgs=umsgs)
            u.save()
            context['success']="your feedback submitted sucessfully"
            return render(request,"contact.html",context)
            #return HttpResponse("Data fetched")
    else:  
       return render(request,'contact.html')

def dish_details(request,did):
    context={}
    d=dish.objects.filter(id=did)
    context['dishes']=d
    return render(request,"dishdetails.html",context)

def viewcart(request):
    c=Cart.objects.filter(uid=request.user.id)
    print(c)
    context={}
    context['data']=c
    s=0
    for x in c:
        s=s+x.did.price * x.qty
    print(s)
    context['total']=s
    nd=len(c)
    context['items']=nd
    return render(request,"viewcart.html",context)

def register(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        #print(uname)
        context={}
        if uname=="" or ucpass=="" or ucpass=="":
            context['errmsg']="fields must not be empty"
            return render(request,"register.html",context)
        elif upass!=ucpass:
            context['errmsg']="password didn't match"
            return render(request,"register.html",context)
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['success']="registered successfully"
                return render (request,'register.html',context)
            except Exception:
                context['errmsg']="already exsists try to login"
                return render(request,"register.html",context) 
    else:
        return render(request,"register.html")


def ulogin(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        context={}
        if uname=="" or upass=="" :
            context['errmsg']="Fields cannot be empty"
            return render(request,"login.html",context)
            
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect("/home")
            else:
                context['errmsg']="Invalid Username/password"
                return render(request,"login.html",context)   
    else:
        return render(request,"login.html")

def ulogout(request):
    logout(request)
    return redirect('/home')

def catfilter(request,cv):
    d1=Q(is_active=True)
    d2=Q(cat=cv)
    d=dish.objects.filter(d1 & d2)
    print(d)
    context={}
    context['dishes']=d 
    return render(request,"menu.html",context)

def sort(request,sv):
    if sv=='0':
        col='price'
    else:
        col='-price'
    d=dish.objects.filter(is_active=True).order_by(col)
    context={}
    context['dishes']=d
    return render(request,"menu.html",context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    d1=Q(price__gte=min)
    d2=Q(price__lte=max)
    d3=Q(is_active=True)
    d=dish.objects.filter(d1 & d2 & d3)
    context={}
    context['dishes']=d 
    return render(request,"menu.html",context)

def addtocart(request,did):
    if request.user.is_authenticated:
        userid=request.user.id
        u=User.objects.filter(id=userid)
        print(u)
        d=dish.objects.filter(id=did)
        print(d)
        q1=Q(uid=u[0])
        q2=Q(did=d[0])
        c=Cart.objects.filter(q1 & q2)
        print(c)
        context={}
        n=len(c)
        if n==1:
            context['errmsg']="dish already exists in cart"
            context['dishes']=d
            return render(request,"dishdetails.html",context)
        else:
            c=Cart.objects.create(uid=u[0],did=d[0])
            c.save()
            context['success']="dish added to cart!!"
            context['dishes']=d
            return render(request,'dishdetails.html',context)
    else:
        return redirect('/login')

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    if qv== '1':
        t=c[0].qty+1
        c.update(qty=t) 
    else:
        t=c[0].qty-1
        c.update(qty=t)
    return redirect('/viewcart')

def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print(oid)
    for x in c:
        o=Order.objects.create(order_id=oid,did=x.did,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    context={}
    context['data']=orders
    s=0
    for x in orders:
        s=s+x.did.price * x.qty
    context['total']=s
    nd=len(orders)
    context['items']=nd
    return render(request,"placeorder.html",context)

def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np=len(orders)
    for x in orders:
        s=s+x.did.price * x.qty
        oid=x.order_id
    
    client = razorpay.Client(auth=("rzp_test_xCLid0aJwqGm4n", "PrFHSF5J48Kssx5KADqsLFI7"))
    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    context={}
    context['data']=payment
    uemail=request.user.username
    print(uemail)
    context['uemail']=uemail
    #return HttpResponse("In payment pg!!")
    return render(request,'pay.html',context)

def sendusermail(request):
    send_mail(
    "Ecart-Order Placed Successfully",
    "Order Completed!! Thanks for ordering.",
    "netradesai2000@gmail.com",
    ["dnetra884@gmail.com"],
    fail_silently=False,
    )
    #print(uemail)
    return HttpResponse("EMail Sent!!")

def menu(request):
     userid=request.user.id
     context={}
     d=dish.objects.filter(is_active=True)
     context['dishes']=d
     return render(request,"menu.html",context)


