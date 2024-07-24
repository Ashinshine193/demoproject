from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from shop.models import Product
from django.contrib.auth.models import User
from .models import Cart,Payment,Order_details
import razorpay


def add_to_cart(request,id):
    p = Product.objects.get(id=id)
    user = request.user
    try:
        cart = Cart.objects.get(user=user,product=p)
        if(p.p_stock>0):
            cart.quantity +=1
            cart.save()
            p.p_stock -= 1
            p.save()
    except:
        if (p.p_stock):
            cart = Cart.objects.create(user=user, product=p, quantity=1)
            cart.save()
            p.p_stock -= 1
            p.save()
    return redirect('cart:view_cart')


def view_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    total = 0
    for i in cart:
        total = total + i.quantity*i.product.p_price
    return render(request,'cart.html',{'cart':cart,'total':total})


def cart_minus(request,id):
    u = request.user
    p = Product.objects.get(id=id)
    try:
        cart = Cart.objects.get(user=u, product=p)
        if(cart.quantity>1):
            cart.quantity -= 1
            cart.save()
            p.p_stock += 1
            p.save()
        else:
            cart.delete()
            p.p_stock += 1
            p.save()
    except:
        pass
    return redirect('cart:view_cart')


def cart_trash(request,id,c_id):
    user=request.user
    p = Product.objects.get(id=id)
    cart = Cart.objects.get(user=user, product=p)
    q = cart.quantity

    p.p_stock=p.p_stock+q
    p.save()

    c = Cart.objects.get(id=c_id)
    c.delete()
    return redirect('cart:view_cart')


def place_order(request):
    if(request.method=="POST"):
        name = request.POST.get('Name')
        phone = request.POST.get('phone')
        addr = request.POST.get('addr')
        city = request.POST.get('city')
        pin = request.POST.get('pin')
        user = request.user
        c = Cart.objects.filter(user=user)
        total = 0
        for i in c:
            total = (total + (i.quantity * i.product.p_price))
        total = int(total*100)
        client = razorpay.Client(auth=('rzp_test_ewqx1AO2HVa4Ca','jMuPKMzFDXvCimCrAhfbSl2v'))

        response_payment = client.order.create(dict(amount=total,currency="INR"))

        print(response_payment)
        order_id = response_payment['id']
        order_status = response_payment['status']
        if order_status=='created':
            p = Payment.objects.create(name=name,amount=total,order_id=order_id)
            p.save()
            for i in c:
                o=Order_details.objects.create(user=user,product=i.product,address=addr,phone=phone,pin=pin,no_of_items=i.quantity,order_id=i.quantity)
                o.save()
        response_payment['name']=user.username
        return render(request,'place_order2.html',{'payment':response_payment})

    return render(request,'place_order.html')


@csrf_exempt
def payment_done(request,u):
    # print(request.user.is_authenticated) #false
    # if not request.user.is_authenticated:
    #     user= User.objects.get(username=u)
    #     login(request,user)
    #     print(request.is_authenticated) #true
    if(request.method=="POST"):
        response = request.POST
        print(response)
        print (u)
        param_dict = {
            'razorpay_order_id':response['razorpay_order_id'],
            'razorpay_payment_id':response['razorpay_payment_id'],
            'razorpay_signature':response['razorpay_signature']
        }
        client = razorpay.Client(auth=('rzp_test_ewqx1AO2HVa4Ca','jMuPKMzFDXvCimCrAhfbSl2v'))
        try:
            status = client.utility.verify_payment_signature(param_dict)
            print(status)

            #After successful payment

            #Retrieve a payment record with particular order_id
            ord = Payment.objects.get(order_id = response['razorpay_order_id'])
            ord.razorpay_payment_id = response['razorpay_payment_id'] #Edits payment id response['razorpay_payment_id']
            ord.paid = True #Edit paid to True
            ord.save()

            u=User.objects.get(username=u)
            c=Cart.objects.filter(user=u)

            #Filter the order_details for particular user with order_id =response['razorpay_order_id']
            o=Order_details.objects.filter(user=u,order_id=response['razorpay_order_id'])
            for i in c:
               i.payment_status="paid" #Edit payment_status="paid"
               i.save()
            c.delete()
            return render(request, 'payment_done.html', {'status': True})
        except:
            return render(request,'payment_done.html',{'status': False})

    return render(request,'payment_done.html')



@login_required
def orderview(request):
    u=request.user
    order=Order_details.objects.filter(user=u,payment_status="paid")

    return render(request,'orderview.html',{'customer':customer,'u':u})
