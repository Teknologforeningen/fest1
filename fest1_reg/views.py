from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from fest1_reg.models import *
from django.core.validators import validate_email
from django.core.mail import send_mail
from django import forms
from django.contrib.auth import login, authenticate
import time

# Create your views here.
def homepage(request):
    return render(request, "homepage.html")

def register(request):
    if int(time.time()) > 1443171600:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            try:
                validate_email(email)
            except forms.ValidationError:
                return HttpResponse("<p>Din e-postadress är inte giltig, vänligen försök på nytt</p><p><a href='./'>Tillbaka</a></p>")

            organization_code = request.POST['organization']
            organization = Organization.objects.get(pk=organization_code)
            avec = request.POST['avec']
            alcoholfree = request.POST.get('alcoholfree', False)
            alcoholfree_sv = "Nej"
            price = "20 €"
            if alcoholfree:
                alcoholfree_sv = "Ja"
                price = "18 €"
            diet = request.POST['diet']
            comment = request.POST['comment']
            new_participant = Participant(first_name=first_name, last_name=last_name, email=email, organization=organization, avec=avec, alcoholfree=alcoholfree, diet=diet, comment=comment)
            new_participant.save()
            subject, sender, recipient = 'Anmälan till Fest 1', 'Helena Hansson <phuxmastare@teknologforeningen.fi>', email

        else:
            organizations_list = {}
            for i in range(0, Organization.objects.count()):
                if Participant.objects.filter(organization=i+1).count() >= Organization.objects.get(pk=i+1).quota:
                    organizations_list[i+1] = Organization.objects.get(pk=i+1).name + " (RESERVPLATS)"
                else:
                    organizations_list[i+1] = Organization.objects.get(pk=i+1).name
            return render(request, "register.html", {"organizations_list": organizations_list, })
    else:
        return render(request, "soon.html")

def afterparty(request):
    if int(time.time()) > 1443171600:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            try:
                validate_email(email)
            except forms.ValidationError:
                return HttpResponse("<p>Din e-postadress är inte giltig, vänligen försök på nytt</p><p><a href='./'>Tillbaka</a></p>")

            new_participant = AfterpartyParticipant(first_name=first_name, last_name=last_name, email=email)
            new_participant.save()
            subject, sender, recipient = 'Anmälan till Fest 1', 'Helena Hansson <phuxmastare@teknologforeningen.fi>', email
            content = "Hej " + first_name + " " + last_name + ",\n\nDin anmälning till Fest1 efterfesten har registrerats.\nVänligen betala festen på förhand senast 7.10\nKonto: FI51 4055 1020 1726 92\nMottagare: Helena Hansson\nMeddelande: Fest1, " + first_name + " " + last_name + \
                      "\nSumma: 5 €\n\nFör att få festen till förköpspris ska du ha med ett kvitto från nätbanken på att du har betalat (om vi inte kan se din betalning kostar efterfesten 7€). Var också beredd att bestyrka din identitet!\nVälkommen!"
            send_mail(subject, content, sender, [email], fail_silently=False)
            return render(request, "confirm.html")
        else:
            return render(request, "afterparty.html")
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
        quotas[i+1] = quota
    return render(request, "list.html", {"lists": lists, "quotas": quotas, "reserve": reserve, })

def phuxk(request):
    if request.user.is_authenticated():
        participant_list = Participant.objects.all()
        afterparty_list = AfterpartyParticipant.objects.all()
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
