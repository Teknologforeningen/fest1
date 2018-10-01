from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from fest1_reg.models import *
from django.core.validators import validate_email
from django.core.mail import send_mail
from django import forms
from django.contrib.auth import login, authenticate
from django.db import IntegrityError
import time

# Create your views here.
def homepage(request):
    return render(request, "homepage.html")

def register(request):
    current_time = int(time.time())
    if current_time > 1539032100:
        return render(request, "closed.html")
    elif current_time > 1537520400:
        if request.method == 'POST':
            price = 20
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            try:
                validate_email(email)
            except forms.ValidationError:
                return HttpResponse("<p>Din e-postadress är inte giltig, vänligen försök på nytt</p><p><a href='./'>Tillbaka</a></p>")

            organization_code = request.POST['organization']
            organization = Organization.objects.get(pk=organization_code)
#            if request.POST.get('halarmarke', False) != 'on':
#                halarmarke = False
#                halarmarke_sv = "Nej"
#            else:
#                halarmarke = True
#                halarmarke_sv = "Ja"
#                price += 2
            halarmarke = False
            halarmarke_sv = "Nej"
            avec = request.POST['avec']
            if request.POST.get('alcoholfree', False) != 'on':
                alcoholfree = False
                alcoholfree_sv = "Nej"
            else:
                alcoholfree = True
                alcoholfree_sv = "Ja"
                price -= 2
            diet = ""
            if request.POST.get('vegetarian', False) == 'on':
                diet += "Vegetarian "
            if request.POST.get('vegan', False) == 'on':
                diet += "Vegan "
            if request.POST.get('glutenfree', False) == 'on':
                diet += "Glutenfri "
            if request.POST.get('lactosefree', False) == 'on':
                diet += "Laktosfri "
            if request.POST.get('milkfree', False) == 'on':
                diet += "Mjölkfri "
            if request.POST.get('apple', False) == 'on':
                diet += "Äppel "
            if request.POST.get('nuts', False) == 'on':
                diet += "Nötter "
            comment = request.POST['comment']
            new_participant = Participant(first_name=first_name, last_name=last_name, email=email, organization=organization, avec=avec, alcoholfree=alcoholfree, diet=diet, comment=comment, halarmarke=halarmarke)
            try:
                new_participant.save()
            except IntegrityError:
                return render(request, "emailused.html")
            
            subject, sender, recipient = 'Anmälan till Fest 1', 'Axel Cedercreutz <phuxmastare@teknologforeningen.fi>', email
            if (Participant.objects.filter(organization=organization_code).count() > Organization.objects.get(pk=organization_code).quota):
                content = "Hej " + first_name + " " + last_name + ",\n\nDin anmälning till Fest 1 har registrerats. Du är ännu på reservplats och vi meddelar efter sista anmälningsdagen om du ryms med på festen!"
            else:
                content = "Hej " + first_name + " " + last_name + ",\n\nDin anmälning till Fest 1 har registrerats:" + \
                     "\nOrganisation: " + organization.name + "\nHalarmärke: " + halarmarke_sv + "\nAvec: " + avec + "\nAlkoholfri: " + alcoholfree_sv + "\nAllergier/Specialdieter: " + diet + "\nKommentarer: " + comment + \
                     "\n\nVänligen betala för din sitz på förhand senast 8.10 (kontrollera från http://www.fest1.fi/participants/ att du inte står på reservkön!).\nKonto: FI79 5788 5920 0095 82\nMottagare: Axel Cedercreutz\nMeddelande: Fest1, " + first_name + " " + last_name + "\nSumma: " + \
                     str(price) + "€\n\nVar beredd på att kunna bestyrka din identitet!\nVälkommen!"

            send_mail(subject, content, sender, [email], fail_silently=False)
            return render(request, "confirm.html")
        else:
            organizations_list = {}
            for i in range(0, Organization.objects.count()):
                if Participant.objects.filter(organization=i+1).count() > Organization.objects.get(pk=i+1).quota:
                    organizations_list[i+1] = Organization.objects.get(pk=i+1).name + " (RESERVPLATS)"
                else:
                    organizations_list[i+1] = Organization.objects.get(pk=i+1).name
            return render(request, "register.html", {"organizations_list": organizations_list, })
    else:
        return render(request, "soon.html")

def afterparty(request):
    current_time = int(time.time())
    if current_time > 1539349200:
        return render(request, "closed.html")
    elif current_time > 1537520400:
        if request.method == 'POST':
            price = 5
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            try:
                validate_email(email)
            except forms.ValidationError:
                return HttpResponse("<p>Din e-postadress är inte giltig, vänligen försök på nytt</p><p><a href='./'>Tillbaka</a></p>")

#            if request.POST.get('halarmarke', False) != 'on':
#                halarmarke = False
#                details = "Halarmärke: Nej\nVIP: Nej"
#            else:
#                halarmarke = True
#                details = "Halarmärke: Ja\nVIP: Nej"
#                price += 2
            halarmarke = False
            details = "Halarmärke: Nej\nVIP: Nej"

            if request.POST.get('vip', False) != 'on':
                vip = False
            else:
                vip = True
                halarmarke = True
                details = "VIP: Ja"
                price = 15 #Overwrites the price += 2 above
                
            if vip and AfterpartyParticipant.objects.filter(vip=True).count() >= 50:
              return HttpResponse("<p>Alla VIP-biljetter har redan sålts.</p><p><a href='./'>Tillbaka</a></p>")

            new_participant = AfterpartyParticipant(first_name=first_name, last_name=last_name, email=email, halarmarke=halarmarke, vip=vip)
            try:
                new_participant.save()
            except IntegrityError:
                return render(request, "emailused.html")

            subject, sender, recipient = 'Anmälan till Fest 1', 'Axel Cedercreutz <phuxmastare@teknologforeningen.fi>', email
            content = "Hej " + first_name + " " + last_name + ",\n\nDin anmälning till Fest1 efterfesten har registrerats:\n" + details + "\n\nVänligen betala festen på förhand senast 8.10\nKonto: FI79 5788 5920 0095 82\nMottagare: Axel Cedercreutz\nMeddelande: Fest1, " + first_name + " " + last_name + \
                     "\nSumma: " + str(price) + "€\n\nFör att få festen till förköpspris ska du ha med ett kvitto från nätbanken på att du har betalat (om vi inte kan se din betalning kostar efterfesten 8€). Var också beredd att bestyrka din identitet!\nVälkommen!"

            send_mail(subject, content, sender, [email], fail_silently=False)
            return render(request, "confirm.html")
        else:
            vipleft = AfterpartyParticipant.objects.filter(vip=True).count() < 50
            return render(request, "afterparty.html", {"vipleft": vipleft, })
    else:
        return render(request, "soon.html")

def list_page(request):
    lists = {}
    quotas = {}
    reserve = []
    for i in range(0, Organization.objects.count()):
        quota = Organization.objects.get(pk=i+1).quota
        participants = Participant.objects.filter(organization=i+1).order_by('id')
        lists[Organization.objects.get(pk=i+1)] = participants[:quota]
        reserve += participants[quota:]
        reserve.sort(key = lambda x: x.id)
        quotas[i+1] = quota
    return render(request, "list.html", {"lists": lists, "quotas": quotas, "reserve": reserve, })

def phuxk(request):
    if request.user.is_authenticated:
        participant_list = Participant.objects.all().order_by('id')
        afterparty_list = AfterpartyParticipant.objects.all().order_by('id')
        return render(request, "phuxk.html", {"participant_list": participant_list, "afterparty_list": afterparty_list, })
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/i/")
            else:
                return HttpResponse("Fel i inloggningsuppgifterna")
        else:
            return render(request, "login.html")
