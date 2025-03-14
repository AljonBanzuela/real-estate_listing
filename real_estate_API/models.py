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
    general_info = models.OneToOneField(General_Info, on_delete=models.CASCADE, related_name='user_preference')
    lot_size_ideal = models.DecimalField(max_digits=10, decimal_places=2)
    room_no_ideal = models.IntegerField()
    floor_no_ideal = models.IntegerField()
    location_ideal = models.CharField(max_length=500)
    price_rent_ideal = models.DecimalField(max_digits=10, decimal_places=2)
    price_full_ideal = models.DecimalField(max_digits=10, decimal_places=2)


#Real-Estate Agents
class Agent_User(models.Model):
    general_info = models.OneToOneField(General_Info, on_delete=models.CASCADE, related_name='agent_details')
    description_agent = models.TextField(max_length=10000)
    years_of_exp = models.PositiveIntegerField()  # Changed to PositiveIntegerField for better representation
    is_available = models.BooleanField(default=True)

