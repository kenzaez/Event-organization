from django import forms
from eventApp.models import Client, Evenement, Fournisseur, Paiement, Ressource
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class eventCreation(forms.ModelForm): 
    class Meta:
        model = Evenement
        fields = ['date_evenement', 'type', 'date_contrat', 'client', 'fournisseurs']
        widgets = {
            'date_evenement': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_contrat': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'fournisseurs': forms.CheckboxSelectMultiple(),
        }
class clientCreation(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'type', 'num_tel', 'email', 'adresse', 'image']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'num_tel': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class supplierCreation(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['nom', 'type', 'num_tel', 'email', 'adresse']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'num_tel': forms.NumberInput(attrs={'class': 'form-control'}),  
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
        }
class paymentRegistration(forms.ModelForm):
    class Meta : 
        model = Paiement
        fields = ['client','type','date_paiement','montant','reste','evenement','deadline']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'date_paiement': forms.NumberInput(attrs={'class': 'form-control','type':'date'}),  
            'montant': forms.NumberInput(attrs={'class': 'form-control','placeholder':'montant'}),
            'reste': forms.NumberInput(attrs={'class': 'form-control','placeholder':'reste'}),
            'evenement': forms.Select(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
class RessourceForm(forms.ModelForm):
    class Meta:
        model = Ressource
        fields = [
            'nom', 'type', 'quantite_disponible', 'cout_unitaire', 'disponible', 
            'fournisseur',  'date_acquisition', 'damaged', 'evenement'
        ]
        
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la ressource'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'quantite_disponible': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantité disponible'}),
            'cout_unitaire': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Coût unitaire'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'fournisseur': forms.Select(attrs={'class': 'form-control'}),

            'date_acquisition': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'damaged': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantité endommagée'}),
            'evenement': forms.Select(attrs={'class': 'form-control'}),
        }

