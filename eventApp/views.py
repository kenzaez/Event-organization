from django.db.models import Sum, Avg, F, ExpressionWrapper, FloatField
from datetime import date,timedelta, datetime
from typing import OrderedDict
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import authenticated_user
from django.utils import timezone
from .models import Client, Evenement, Fournisseur, Paiement, Ressource
from .forms import  LoginForm, RegisterForm, RessourceForm, clientCreation, eventCreation, paymentRegistration, supplierCreation
# Create your views here.
# ---------------------------LOGIN/REGISTRATION/LOGOUT

#  START LOGOUT VIEW
def logout_view(request):
    logout(request)  
    return redirect('login')  

# END LOGOUT VIEW



@authenticated_user
# START REGISTRATION
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # hash password
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


# END REGISTRATION

@authenticated_user
# START LOGIN
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'loginUser.html', {'form': form})


# END LOGIN 


# ---------------------------------------DASHBOARD note : it's kinda big, scroll down for the rest
#of the functionalities
@login_required
def dashboard(request):

    # 1. Dates setup
    today = timezone.now().date()
    last_month = today - timedelta(days=30)
    previous_month_start = last_month - timedelta(days=30)

    # 2. Total payments (all time)
    total_payments = Paiement.objects.aggregate(total=Sum('montant'))['total'] or 0

    # 3. Payments 30–60 days ago (previous period)
    previous_total = Paiement.objects.filter(
        date_paiement__gte=previous_month_start,
        date_paiement__lt=last_month
    ).aggregate(total=Sum('montant'))['total'] or 0

    # 4. Potential growth percentage
    potential_growth_percent = (
        ((total_payments - previous_total) / previous_total) * 100
        if previous_total > 0 else 0
    )

    # 5. Current revenue (last 30 days)
    current_revenue = Paiement.objects.filter(
        date_paiement__gte=last_month
    ).aggregate(total=Sum('montant'))['total'] or 0

    # 6. Previous revenue (30–60 days ago)
    previous_revenue = previous_total  # already calculated

    # 7. Revenue growth percentage
    revenue_growth_percent = (
        ((current_revenue - previous_revenue) / previous_revenue) * 100
        if previous_revenue > 0 else 0
    )

    # 8. Daily income (average over last 7 days)
    last_week = today - timedelta(days=7)
    daily_income = Paiement.objects.filter(
        date_paiement__gte=last_week
    ).aggregate(total=Sum('montant'))['total'] or 0
    daily_avg = daily_income / 7

    # 9. Previous week daily income average
    previous_week_start = last_week - timedelta(days=7)
    previous_daily = Paiement.objects.filter(
        date_paiement__gte=previous_week_start,
        date_paiement__lt=last_week
    ).aggregate(total=Sum('montant'))['total'] or 0
    previous_daily_avg = previous_daily / 7

    # 10. Daily income growth %
    daily_growth_percent = (
        ((daily_avg - previous_daily_avg) / previous_daily_avg) * 100
        if previous_daily_avg > 0 else 0
    )

    #//////////TABLE OF THIS MONTH's EVENTS
    now = date.today()
    events = Evenement.objects.filter(date_evenement__month=now.month)
    #//////////END TABLE OF THIS MONTH's EVENTS
    
    #//////////PAYEMENTS CHART
   
    cheque_count = Paiement.objects.filter(type='cheque').aggregate(Sum('montant'))['montant__sum'] or 0
    virement_count = Paiement.objects.filter(type='virement').aggregate(Sum('montant'))['montant__sum'] or 0
    cash_count = Paiement.objects.filter(type='cash').aggregate(Sum('montant'))['montant__sum'] or 0

    #//////////END PAYEMENTS CHART



    #//////////LAST PAYMENTS
    # ORDER THE PAYMENTS
    all_pays = Paiement.objects.order_by('-id')

    # Delete redundancy
    unique_pays = OrderedDict()

    # Store the 3 last payments (unique by type)
    for pay in all_pays:
        if pay.type not in unique_pays:
            unique_pays[pay.type] = pay
        if len(unique_pays) == 3:
            break

    pays = list(unique_pays.values())
    #//////////END LAST PAYMENTS

    context =  {'events': events, 'pays': pays,
                'cheque_count': cheque_count,
                'virement_count': virement_count,
                'cash_count': cash_count,
                'potential_amount': total_payments,
                'potential_growth': potential_growth_percent,
                'revenue_amount': current_revenue,
                'revenue_growth': revenue_growth_percent,
                'daily_amount': daily_avg,
                'daily_growth': daily_growth_percent,
                }
    return render(request, 'dashboard.html', context)


# ---------------------------------EVENTS--------------------------------------------------------
@login_required
def events_list(request):
    events = Evenement.objects.all()
    return render(request,"events/events.html",{"events":events})
@login_required
def event_form(request, id=0):

    mode = "Edit" if id != 0 else "Add"
    
    if request.method == "GET":
        if id != 0:
            event = get_object_or_404(Evenement, pk=id)
            form = eventCreation(instance=event)
        else:
            form = eventCreation()

    else:  # POST
   
        if id != 0:
            event = get_object_or_404(Evenement, pk=id)
            form = eventCreation(request.POST, instance=event)
            if form.errors:
               print(form.errors)
            else : 
                print('ok')

        else:
            form = eventCreation(request.POST)

        if form.is_valid():
            form.save()
            return redirect('events')

    return render(request, "events/createEvent.html", {'form': form, 'mode': mode})
# ------------------------------------------------END EVENTS

# ---------------------------------------------------CLIENTS
@login_required
def client_form(request, id=0):

    mode = "Edit" if id != 0 else "Add"
    
    if request.method == "GET":
        if id != 0:
            client = get_object_or_404(Client, pk=id)
            form = clientCreation(instance=client)
        else:
            form = clientCreation()

    else:  # POST
   
        if id != 0:
            client = get_object_or_404(Client, pk=id)
            form = clientCreation(request.POST,request.FILES, instance=client)
            if form.errors:
               print(form.errors)
            else : 
                print('ok')

        else:
            form = clientCreation(request.POST,request.FILES)

        if form.is_valid():
            form.save()
            return redirect('clients')

    return render(request, "clients/addClient.html", {'form': form, 'mode': mode})
@login_required
def clients(request):
    clients = Client.objects.all()
    context = {'clients': clients}
    return render(request,'clients/clients.html',context)
@login_required
def deleted_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    client.deleted = True
    client.save()
    return redirect('clients') 
    
# -------------------------------FOURNISSEUR
@login_required
def choose(request):
    return render(request,"suppliers/choose.html")
@login_required
def supplier_form(request, id=0):

    mode = "Edit" if id != 0 else "Add"
    
    if request.method == "GET":
        if id != 0:
            event = get_object_or_404(Fournisseur, pk=id)
            form = supplierCreation(instance=event)
        else:
            form = supplierCreation()

    else:  # POST
   
        if id != 0:
            event = get_object_or_404(Fournisseur, pk=id)
            form = supplierCreation(request.POST, instance=event)
            if form.errors:
               print(form.errors)
            else : 
                print('ok')

        else:
            form = supplierCreation(request.POST)

        if form.is_valid():
            form.save()
            return redirect('clients_list')
    return render(request, "suppliers/addSupplier.html", {'form': form, 'mode': mode})
@login_required
def FoodFourn(request):
    fourns = Fournisseur.objects.filter(type='Food')
    return render(request,"suppliers/supFood.html",{'fourns':fourns})
@login_required
def MaterialFourn(request):
    fourns = Fournisseur.objects.filter(type='materiel')
    return render(request,"suppliers/supMaterial.html",{'fourns':fourns})
@login_required
def EnterFourn(request):
    fourns = Fournisseur.objects.filter(type='entertainment')
    return render(request,"suppliers/supFood.html",{'fourns':fourns})
@login_required
def fournDelete(request, fourn_id):
    fourn = get_object_or_404(Fournisseur, pk=fourn_id)
    fourn.deleted = True
    fourn.save()
    if fourn.type=="Food":
         return redirect('supplier_food') 
    if fourn.type == "matriel":
        return redirect('supplier_food') 
    if fourn.type == "entertainment" :
        return redirect('supplier_food') 

# --------------------------------END FOURNISSEUR

# ------------------------------------PAYMENTS
@login_required
def payForm(request,id=0):
    mode = "Edit" if id != 0 else "Add"
    
    if request.method == "GET":
        if id != 0:
            pay = get_object_or_404(Paiement, pk=id)
            form = paymentRegistration(instance=pay)
        else:
            form = paymentRegistration()

    else:  # POST
   
        if id != 0:
            pay = get_object_or_404(Paiement, pk=id)
            form = paymentRegistration(request.POST, instance=pay)
            if form.errors:
               print(form.errors)
            else : 
                print('ok')

        else:
            form = paymentRegistration(request.POST)

        if form.is_valid():
            form.save()
            return redirect('payement')

    return render(request, "payments/Registerpayment.html", {'form': form, 'mode': mode})
@login_required
def payement(request):
    now = date.today()
    pays = Paiement.objects.all()
    for p in pays:
        p.is_overdue = p.deadline < now 
    context = {'pays': pays}
    return render(request, "payments/payments.html", context)

# --------------------------------------END PAYMENT----------------------------------------------------

# --------------------------------RESSOURCE
@login_required
def ressources(request):
    ressources = Ressource.objects.all()
    return render(request,'ressources/ressources.html',{'ressources':ressources})
@login_required
def ressource_form(request, id=0):

    mode = "Edit" if id != 0 else "Add"
    
    if request.method == "GET":
        if id != 0:
            ressou = get_object_or_404(Ressource, pk=id)
            form = RessourceForm(instance=ressou)
        else:
            form = RessourceForm()

    else:  # POST
   
        if id != 0:
            event = get_object_or_404(Ressource, pk=id)
            form = RessourceForm(request.POST, instance=ressou)
            if form.errors:
               print(form.errors)
            else : 
                print('ok')

        else:
            form = RessourceForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('ressource_form')
    return render(request, "ressources/addRessource.html", {'form': form, 'mode': mode})
@login_required
def returnRess(request, ress_id):
    if request.method == 'POST':
        ress = get_object_or_404(Ressource, pk=ress_id)
        ress.returned = True
        ress.save()
        return redirect('ressources')
    return redirect('ressources') 
