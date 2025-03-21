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
    general_info = models.OneToOneField(
        General_Info,
        on_delete=models.CASCADE,
        related_name='agent_profile',
        default=None
    )
    agent_description = models.TextField(default="No description provided")
    years_of_exp = models.PositiveIntegerField(default=0, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Agent {self.general_info.username}"


#property descriptions

class Property_Description(models.Model):
    prop_name = models.CharField(max_length=200)
    lot_size = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    room_no = models.IntegerField(default=1)
    floor_no = models.IntegerField(default=1)
    location = models.CharField(max_length=500, default=None)
    is_full = models.BooleanField(default=False)
    is_rent = models.BooleanField(default=False)
    sample_image = models.ImageField


#Property Price
class Property_Price(models.Model):
    property_description = models.ForeignKey(Property_Description, related_name='prices', on_delete=models.CASCADE)
    price_rent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_full = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    price_rent_next = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_full_next = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    rent_duration_months = models.PositiveIntegerField(default=1, help_text="Duration of rent in months."
    )

    def __str__(self):
        return f"Price details for {self.property_description.prop_name}"


class Feedback(models.Model):
    property_description = models.ForeignKey(Property_Description, related_name='feedbacks', on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(default=1)  # Example: 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.property_description}: {self.comment[:30]}"  # Returns a preview of the comment
    request_date = models.DateTimeField(auto_now_add=True)
    meeting_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('declined', 'Declined')],
        default='pending'
    )


class Images(models.Model):
    property_description = models.ForeignKey(
        Property_Description,
        related_name='images',
        on_delete=models.CASCADE
    )
    exterior = models.ImageField(upload_to='property_images/exterior/', blank=True, null=True)
    interior = models.ImageField(upload_to='property_images/interior/', blank=True, null=True)
    floor_plan = models.ImageField(upload_to='property_images/floor/', blank=True, null=True)

    def __str__(self):
        return f"Images for {self.property_description.prop_name}"


class Request(models.Model):
    user = models.ForeignKey('General_Info', related_name='requests', on_delete=models.CASCADE)
    property_description = models.ForeignKey('Property_Description', related_name='requests', on_delete=models.CASCADE)
    agent = models.ForeignKey(
        'Agent_User', related_name='agent_requests', on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    meeting_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('declined', 'Declined')
        ],
        default='pending'
    )

    def __str__(self):
        return f"Request by {self.user.username} for property {self.property_description.prop_name} at {self.property_description.location} with Agent {self.agent.general_info.username}"


class PaymentRecord(models.Model):
    user = models.ForeignKey('General_Info', related_name='payment_records', on_delete=models.CASCADE)
    property = models.ForeignKey('Property_Description', related_name='payment_records', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)  # When the payment was made
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('paid', 'Paid')],
        default='pending'
    )

    def __str__(self):
        return f"Payment for {self.user.username} on {self.property.prop_name}"


class PropertyNotification(models.Model):
    user = models.ForeignKey('General_Info', related_name='notifications', on_delete=models.CASCADE)
    property = models.ForeignKey('Property_Description', related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)  # Indicates whether the user has viewed the notification
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.property.prop_name}"
