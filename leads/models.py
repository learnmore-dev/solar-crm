from django.db import models
from django.contrib.auth.models import User
from datetime import date, time, datetime


# ===============================
# LEAD MODEL
# ===============================
class Lead(models.Model):

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

    INSTALLATION_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('offgrid', 'Off Grid'),
    ]

    ROOF_TYPE_CHOICES = [
        ('rcc', 'RCC'),
        ('sheet', 'Sheet'),
        ('tile', 'Tile'),
        ('metal', 'Metal'),
        ('other', 'Other'),
    ]

    FINANCING_CHOICES = [
        ('cash', 'Cash'),
        ('loan', 'Loan'),
        ('emi', 'EMI'),
    ]

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

    # BASIC INFO
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    # SOLAR DETAILS
    roof_type = models.CharField(max_length=20, choices=ROOF_TYPE_CHOICES, blank=True, null=True)
    average_monthly_bill = models.IntegerField(blank=True, null=True)
    sanctioned_load = models.FloatField(blank=True, null=True)
    financing_preference = models.CharField(max_length=20, choices=FINANCING_CHOICES, blank=True, null=True)
    installation_type = models.CharField(max_length=50, choices=INSTALLATION_TYPE_CHOICES, blank=True, null=True)

    # CRM TRACKING
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new')
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, blank=True, null=True)
    medium = models.CharField(max_length=50, choices=MEDIUM_CHOICES, blank=True, null=True)
    campaign = models.CharField(max_length=50, choices=CAMPAIGN_CHOICES, blank=True, null=True)

    remarks = models.TextField(blank=True, null=True)
    follow_up_date = models.DateField(blank=True, null=True)
    follow_up_time = models.TimeField(blank=True, null=True)

    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.status}"

    # FOLLOWUP HELPERS
    @property
    def is_followup_today(self):
        return self.follow_up_date == date.today() if self.follow_up_date else False

    @property
    def is_overdue(self):
        return self.follow_up_date < date.today() if self.follow_up_date else False


# ===============================
# ATTENDANCE MODEL
# ===============================
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)

    # 🔥 NEW FIELDS (ADD THIS)
    photo = models.ImageField(upload_to='attendance_photos/', null=True, blank=True)
    latitude = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.CharField(max_length=100, null=True, blank=True)

    # ✅ WORKING HOURS
    @property
    def working_hours(self):
        if self.check_in and self.check_out:
            start = datetime.combine(self.date, self.check_in)
            end = datetime.combine(self.date, self.check_out)
            return end - start
        return None

    # ✅ STATUS LOGIC
    @property
    def status(self):
        if not self.check_in:
            return "Absent"

        late_time = time(10, 0)

        if self.check_in > late_time:
            return "Late"

        return "On Time"

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    
# ===============================
# LEAVE MODEL
# ===============================
class Leave(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    LEAVE_TYPE_CHOICES = [
        ('sick', 'Sick'),
        ('casual', 'Casual'),
        ('paid', 'Paid'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_date = models.DateField()
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.leave_date} - {self.status}"