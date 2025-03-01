from django.db import models


#Authentication
class General_Info(models.Model):
    username: models.CharField(max_length=250)
    password: models.CharField(unique=True)
    email_address: models.EmailField(unique=True)
    location: models.CharField(max_length=500)
    is_agent: models.BooleanField(default=False)


#Real-Estate Agents
class Agent_User(models.Model):
    description_agent: models.TextField(max_length=10000)
    years_of_exp: models.DateTimeField()
    is_available: models.BooleanField(default=True)

#https://docs.google.com/spreadsheets/d/1g5NRadCcwRiSz3KC4VnhUvgXIa8uAVaVUxsbZi-Rfx4/edit?gid=0#gid=0
