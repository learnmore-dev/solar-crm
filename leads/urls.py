from django.urls import path
from . import views

app_name = 'leads'

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("enquiry/", views.enquiry_view, name="enquiry"),
    path("list/", views.lead_list, name="lead_list"),
    path("detail/<int:pk>/", views.lead_detail, name="lead_detail"),
    path("edit/<int:pk>/", views.lead_edit, name="lead_edit"),
    path("delete/<int:pk>/", views.lead_delete, name="lead_delete"),
    path("add/", views.add_lead, name="add_lead"),
    path("invoice/<int:lead_id>/", views.generate_invoice, name="generate_invoice"),
    path("record_payment/", views.record_payment, name="record_payment"),

   
]
