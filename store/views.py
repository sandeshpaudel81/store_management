from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url="/account/login")
def index(request):
    productList = Product.objects.all()
    context = {'products':productList}
    return render(request, 'dashboard.html', context)


@login_required(login_url="/account/login")
def add_product(request):
    if request.method=="POST":
        product_name = request.POST['product_name']
        product_description = request.POST['product_description']
        product_quantity = int(request.POST['product_quantity'])
        product_company = request.POST['product_company']
        product_sp = float(request.POST['product_sp'])
        product_cp = float(request.POST['product_cp'])
        if (product_quantity<0 or product_sp<0):
            messages.error(request, "Negative value is not allowed.")
        else:
            
            Product.objects.create(product_name=product_name, product_description=product_description, product_quantity=product_quantity, product_company=product_company, product_cp=product_cp, product_sp=product_sp)
            messages.success(request, "Product added successfully!")
            return redirect('/add-product')
    x = Product.objects.latest('id')
    y = x.id+1
    return render(request, 'add-product.html', {'y':y})


@login_required(login_url="/account/login")
def update_product(request):
    if request.method=="POST":
        p_id = request.POST['product_id']
        
        toupdate = Product.objects.get(id=p_id)
        
        toupdate.product_name = request.POST['product_name']
        toupdate.product_company = request.POST['product_company']
        toupdate.product_description = request.POST['product_description']
        toupdate.product_cp = request.POST['product_cp']
        toupdate.product_sp = request.POST['product_sp']
        toupdate.product_quantity = request.POST['product_quantity']
        toupdate.save()
        return redirect('/update-product')
    return render(request, 'update-product.html')


@login_required(login_url="/account/login")
def search_product(request):
    query = request.GET['prod_id']
    product_id = int(query)
    try:
        toupdate = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise messages.error(request, "Product Not Found!")
    return render(request, 'update-product.html', {'product': toupdate})
    


@login_required(login_url="/account/login")
def billing(request):
    context = {}
    return render(request, 'billing.html', context)


@login_required(login_url="/account/login")
def add_new_bill(request):
    if request.method == "POST":
        customer_name = request.POST['customer_name']
        Bill.objects.create(customer_name= customer_name)
        return redirect('/add-product-to-bill')


@login_required(login_url="/account/login")
def existing_bills(request):
    allBills = Bill.objects.all()
    context = {'bills':allBills}
    return render(request, 'existing-bill.html', context)


@login_required(login_url="/account/login")
def add_product_to_bill(request):
    if request.method == "POST":
        billID = request.POST['bill']
        prodID = request.POST['product_id']
        quantity = request.POST['quantity']

        # to decrease the quantity in stock
        p = Product.objects.get(id=prodID)
        p.product_quantity = int(p.product_quantity) - int(quantity)
        p.save()

        BillItems.objects.create(bill_id= billID, product_id=prodID, quantity=quantity)
        return redirect('/add-product-to-bill')
    return render(request, 'add-product-to-bill.html')


@login_required(login_url="/account/login")
def get_product(request):
    query = request.GET['prod_id']
    product_id = int(query)
    product = Product.objects.get(id=product_id)
    bills = Bill.objects.all()[:5]
    allBills = reversed(bills)
    context = {'product': product, 'bills': allBills}
    return render (request, 'add-product-to-bill.html', context)


@login_required(login_url="/account/login")
def final_bill(request, id):
    billItems = BillItems.objects.filter(bill=Bill.objects.get(id=id))
    context = {'items': billItems, 'billId': id}
    return render(request, 'final-bill.html', context)


@login_required(login_url="/account/login")
def print_bill(request, id):
    billItems = BillItems.objects.filter(bill=Bill.objects.get(id=id))
    grandTotal = 0
    for i in billItems:
        grandTotal += int(i.quantity)*float(i.product.product_sp)
    bill = Bill.objects.get(id=id)
    context = {'bill': bill, 'items':billItems, 'g_total':grandTotal}
    return render(request, 'invoice.html', context)
