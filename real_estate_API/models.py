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
    general_info = models.OneToOneField(General_Info, on_delete=models.CASCADE, related_name='user_preference',
                                        default=None)
    lot_size_ideal = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    room_no_ideal = models.IntegerField(default=1)
    floor_no_ideal = models.IntegerField(default=1)
    location_ideal = models.CharField(max_length=500, default=None)
    price_rent_ideal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_full_ideal = models.DecimalField(max_digits=10, decimal_places=2, default=1)


#Real-Estate Agents
class Agent_User(models.Model):
    general_info = models.OneToOneField(General_Info, on_delete=models.CASCADE, related_name='agent_details',
                                        default=None)
    agent_description = models.TextField(default="No description")
    years_of_exp = models.PositiveIntegerField(default="0")
    is_available = models.BooleanField(default=True)


#property descriptions

class Property(models.Model):
    lot_size = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    room_no = models.IntegerField(default=1)
    floor_no = models.IntegerField(default=1)
    location = models.CharField(max_length=500, default=None)
    is_full = models.BooleanField(default=False)
    is_rent = models.BooleanField(default=False)
    price_rent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_full = models.DecimalField(max_digits=10, decimal_places=2, default=1)


class Feedback(models.Model):
    property = models.ForeignKey(Property, related_name='feedbacks', on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(default=1)  # Example: 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.property.location}"


class Images(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    exterior = models.ImageField


class Request(models.Model):
    user = models.ForeignKey(General_Info, related_name='requests', on_delete=models.CASCADE)
    property = models.ForeignKey(Property, related_name='requests', on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent_User, related_name='property_requests', on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    meeting_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('declined', 'Declined')],
        default='pending'
    )

    def __str__(self):
        return f"Request by {self.user.username} for {self.property.location} with Agent {self.agent.general_info.username}"
