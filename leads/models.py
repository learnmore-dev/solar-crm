from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ('new', 'New'),
    ('contacted', 'Contacted'),
    ('quote', 'Quote'),
    ('converted', 'Converted'),
]

from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ('new', 'New'),
    ('contacted', 'Contacted'),
    ('quote', 'Quote'),
    ('converted', 'Converted'),
]

CUSTOMER_TYPE_CHOICES = [
    ('Residential', 'Residential'),
    ('Commercial', 'Commercial'),
    ('Industrial', 'Industrial'),
]

class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )

    customer_type = models.CharField(
        max_length=20,
        choices=CUSTOMER_TYPE_CHOICES,
        default='Residential'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




class LeadNote(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="notes")
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.lead.name}"


class LeadImage(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='lead_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Installation(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    installed_on = models.DateField()
    installed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    kwh_generated = models.FloatField(default=0)

    def __str__(self):
        return f"Installation for {self.lead.name}"
