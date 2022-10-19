from math import ceil
from turtle import update
from urllib import response
from django.http import HttpResponse
from django.shortcuts import render
from .models import OrderUpdates, product
from .models import Contact
from.models import Orders
import json

# def index(request):
    #return HttpResponse("index shop")
    # showing all the data in the index page data that we inserted in admin page through models
    # products=product.objects.all()# fetching all the product we had 
    # print(products)
    # n=len(products)
    # nslides=n//4 +ceil((n/4)-(n//4))
    # parms={'no_of_slides':nslides,'range':range(1,nslides),'product':products}
    
    #getting new slides show and bring product according to their categoey 
    
    # allProds=[[products, range(1, len(products)), nSlides],[products, range(1, len(products)), nSlides]]
    # params={'allProds':allProds }
    
    
    
    # WORKING WITH MULTIPLE SLIDE SHOW
def index(request):
        allProds = []
        catprods = product.objects.values('category', 'id')
        cats = {item['category'] for item in catprods}
        for cat in cats:
            prod = product.objects.filter(category=cat)
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])
    
    
        params = {'allProds':allProds}
        return render(request,'shop/index.html',params)


def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    thank=False
    if request.method=='POST':
        name =request.POST.get('txtName','')
        email=request.POST.get('txtEmail','')
        number=request.POST.get('txtPhone','')
        message=request.POST.get('txtMsg','')
        contact = Contact(name=name, email=email,number=number ,message=message )
        contact.save()
        thank=True
    return render(request, 'shop/contact.html', {'thank':thank})
        
    

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdates.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')



def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params) 

def productView(request, myid):
    
    # FETCHING THE PRODUCT USING THE ID
    
    products=product.objects.filter(id=myid)
    #print(product)
    return render(request,'shop/prodView.html',{'product':products[0]})


def checkout(request):
        if request.method=="POST":
            items_json = request.POST.get('itemsJson', '')
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
            city = request.POST.get('city', '')
            state = request.POST.get('state', '')
            zip_code = request.POST.get('zip_code', '')
            phone = request.POST.get('phone', '')
            order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone)
            order.save()
            update = OrderUpdates(order_id=order.order_id, update_desc="The order has been placed")
            update.save()
            thank = True
            id = order.order_id
            return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        return render(request, 'shop/checkout.html')

