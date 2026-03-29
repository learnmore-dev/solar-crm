from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Lead(models.Model):

    # ---------------- STATUS ----------------
    STATUS_CHOICES = [
        ('new', 'New'),
        ('site_survey_scheduled', 'Site Survey Scheduled'),
        ('site_survey_done', 'Site Survey Done'),
        ('proposal_sent', 'Proposal/Quotation Sent'),
        ('negotiation', 'Negotiation'),
        ('order_confirmed', 'Order Confirmed'),
        ('installation_scheduled', 'Installation Scheduled'),
        ('installation_completed', 'Installation Completed'),
        ('converted', 'Converted'),
    ]

    # ---------------- INSTALLATION ----------------
    INSTALLATION_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('offgrid', 'Off Grid'),
    ]

    # ---------------- ROOF TYPE ----------------
    ROOF_TYPE_CHOICES = [
        ('rcc', 'RCC'),
        ('sheet', 'Sheet'),
        ('tile', 'Tile'),
        ('metal', 'Metal'),
        ('other', 'Other'),
    ]

    # ---------------- FINANCE ----------------
    FINANCING_CHOICES = [
        ('cash', 'Cash'),
        ('loan', 'Loan'),
        ('emi', 'EMI'),
    ]

    # ---------------- LEAD SOURCE ----------------
    MEDIUM_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('whatsapp', 'WhatsApp'),
        ('social_media', 'Social Media'),
        ('referral', 'Referral'),
    ]

    SOURCE_CHOICES = [
        ('chat', 'Chat'),
        ('website', 'Website'),
        ('walkin', 'Walk-in'),
    ]

    CAMPAIGN_CHOICES = [
        ('summer_sale', 'Summer Sale'),
        ('referral_program', 'Referral Program'),
        ('social_media_ad', 'Social Media Ad'),
        ('offline_event', 'Offline Event'),
    ]

    # ================= BASIC INFO =================
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    # ================= SOLAR DETAILS =================
    roof_type = models.CharField(
        max_length=20,
        choices=ROOF_TYPE_CHOICES,
        blank=True,
        null=True
    )

    average_monthly_bill = models.IntegerField(
        blank=True,
        null=True,
        help_text="Enter electricity bill in ₹"
    )

    sanctioned_load = models.FloatField(
        blank=True,
        null=True,
        help_text="Enter load in kW"
    )

    financing_preference = models.CharField(
        max_length=20,
        choices=FINANCING_CHOICES,
        blank=True,
        null=True
    )

    installation_type = models.CharField(
        max_length=50,
        choices=INSTALLATION_TYPE_CHOICES,
        blank=True,
        null=True
    )

    # ================= CRM TRACKING =================
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='new'
    )

    source = models.CharField(
        max_length=50,
        choices=SOURCE_CHOICES,
        blank=True,
        null=True
    )

    medium = models.CharField(
        max_length=50,
        choices=MEDIUM_CHOICES,
        blank=True,
        null=True
    )

    campaign = models.CharField(
        max_length=50,
        choices=CAMPAIGN_CHOICES,
        blank=True,
        null=True
    )

    remarks = models.TextField(blank=True, null=True)

    follow_up_date = models.DateField(blank=True, null=True)
    follow_up_time = models.TimeField(blank=True, null=True)

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_leads'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # ================= DISPLAY =================
    def __str__(self):
        return f"{self.name} - {self.status}"

    # ================= FOLLOWUP HELPERS =================
    @property
    def is_followup_today(self):
        return self.follow_up_date == date.today() if self.follow_up_date else False

    @property
    def is_overdue(self):
        return self.follow_up_date < date.today() if self.follow_up_date else False