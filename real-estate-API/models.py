from django.db import models


#Authentication
class General_Info(models.Model):
    username: models.CharField(max_length=250)
    password: models.CharField(unique=True)
    email_address: models.EmailField(unique=True)
    location: models.CharField(max_length=500)
    is_agent: models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


#Non-Agent Users

class Regular_User(models.Model):
    #preference
    lot_size_ideal: models.DecimalField(decimal_places=2)
    room_no_ideal: models.IntegerField
    floor_no_ideal: models.IntegerField
    location_ideal: models.IntegerField(max_length=500)
    price_rent_ideal: models.DecimalField(decimal_places=2)
    price_full_ideal: models.DecimalField(decimal_places=2)


#Real-Estate Agents
class Agent_User(models.Model):
    description_agent: models.TextField(max_length=10000)
    years_of_exp: models.DateTimeField()
    is_available: models.BooleanField(default=True)

#https://docs.google.com/spreadsheets/d/1g5NRadCcwRiSz3KC4VnhUvgXIa8uAVaVUxsbZi-Rfx4/edit?gid=0#gid=0
