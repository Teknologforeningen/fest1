from django.db import models

# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=64)
    quota = models.PositiveIntegerField()

class Participant(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, db_column='participants')
    email = models.EmailField(unique=True)
    avec = models.CharField(max_length=128)
    diet = models.CharField(max_length=128)
    alcoholfree = models.BooleanField()
    comment = models.TextField()
    halarmarke = models.BooleanField()

class AfterpartyParticipant(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    halarmarke = models.BooleanField()
    vip = models.BooleanField()
