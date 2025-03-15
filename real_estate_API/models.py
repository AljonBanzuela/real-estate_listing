from django.db import models
from django.contrib.auth.hashers import make_password


#Authentication
class General_Info(models.Model):
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=128, unique=True)
    email_address = models.EmailField(unique=True)
    location = models.CharField(max_length=500)
    is_agent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)


#Non-Agent Users

class Regular_User(models.Model):
    #preference
    general_info = models.OneToOneField(General_Info, on_delete=models.CASCADE, related_name='user_preference', default=None)
    lot_size_ideal = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    room_no_ideal = models.IntegerField(default=1)
    floor_no_ideal = models.IntegerField(default=1)
    location_ideal = models.CharField(max_length=500, default=None)
    price_rent_ideal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_full_ideal = models.DecimalField(max_digits=10, decimal_places=2, default=1)


#Real-Estate Agents
class Agent_User(models.Model):
    general_info = models.OneToOneField(General_Info, on_delete=models.CASCADE, related_name='agent_details', default=None)
    agent_description = models.TextField (default="No description")
    years_of_exp = models.PositiveIntegerField(default="0")
    is_available = models.BooleanField(default=True)

