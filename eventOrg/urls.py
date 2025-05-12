"""
URL configuration for eventOrg project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from eventApp.views import EnterFourn, FoodFourn, MaterialFourn, choose, client_form, clients, dashboard, deleted_client, event_form, events_list, fournDelete, login_view, logout_view, payForm, payement, register_view, ressource_form, ressources, returnRess, supplier_form
                
urlpatterns = [
    path("admin/", admin.site.urls),
    # DASHBOARD
    path("dashboard",dashboard,name="dashboard"),
    # EVENTS
    path('eventForm',event_form,name="eventForm"),
    path('events',events_list,name="events"),
    path('<int:id>/',event_form, name="eventEdit"),
    # CLIENTS
    path("clientForm/",client_form,name="clientForm"),
    path('<int:id>/',client_form, name="clientEdit"),
    path('clients/delete/<int:client_id>/', deleted_client, name='clientDelete'),  
    path("clients/",clients,name="clients"),
    #SUPPLIERS
    path("choose/",choose,name="choose"),
    path("supplierForm/",supplier_form,name="supplierForm"),
     path("/<int:id>/",supplier_form,name="supplierEdit"),
     path('supplier_food',FoodFourn,name="supplier_food"),
     path('supplier_mat',MaterialFourn,name="supplier_mat"),
     path('supplier_enter',EnterFourn,name="supplier_enter"),
     path('delete/<int:fourn_id>/', fournDelete, name='fournDelete'),

    # PAYMENTS
    path("payement/",payement,name="payement"),
    path('RegisterPay/',payForm,name="RegisterPay"),
    path('payement/<int:id>/',payForm, name="payEdit"),

    # RESSOURCES
     path("ressource_form/",ressource_form,name="ressource_form"),
     path("<int:ress_id>/",ressource_form,name="RessEdit"),
      path('ressourceReturned/<int:ress_id>/', returnRess, name='ressourceReturned'),
      path("ressources/",ressources,name="ressources"),
   #LOGIN
   path("",login_view,name="login"),
   #REGISTER
   path("register/",register_view,name="register"),
   #lOGOUT
   path('logout',logout_view,name='logout')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)