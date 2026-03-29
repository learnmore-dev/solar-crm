from django.urls import path
from . import views

app_name = "leads"

urlpatterns = [

    # ===============================
    # DASHBOARD
    # ===============================
    path('', views.dashboard, name='dashboard'),

    # ===============================
    # LEADS
    # ===============================
    path('leads/', views.lead_list, name='lead_list'),
    path('leads/add/', views.add_lead, name='add_lead'),
    path('leads/<int:pk>/', views.lead_detail, name='lead_detail'),
    path('leads/<int:pk>/edit/', views.lead_edit, name='lead_edit'),
    path('leads/<int:pk>/delete/', views.lead_delete, name='lead_delete'),

    # ===============================
    # CONVERGENT LEAD PAGE
    # ===============================
    path('leads/<int:pk>/convergent/', views.convergent_lead, name='convergent_lead'),

    # ===============================
    # ENQUIRY FORM
    # ===============================
    path('enquiry/', views.enquiry, name='enquiry'),

    # ===============================
    # FOLLOW-UPS
    # ===============================
    path('followups/', views.followups, name='followups'),

    # ===============================
    # OTHER TOP MENU PAGES
    # ===============================
    path('tasks/', views.tasks, name='tasks'),
    path('appointments/', views.appointments, name='appointments'),
    path('calls/', views.calls, name='calls'),
    path('support-tickets/', views.support_tickets, name='support_tickets'),
    path('mails/', views.mails, name='mails'),
    path('webpages/', views.webpages, name='webpages'),
    path('webforms/', views.webforms, name='webforms'),
    path('time-tracking/', views.employee_time_tracking, name='time_tracking'),

    # ===============================
    # INVOICE & PAYMENT
    # ===============================
    path('invoice/<int:lead_id>/', views.generate_invoice, name='generate_invoice'),
    path('record-payment/', views.record_payment, name='record_payment'),

    # ===============================
    # CONVERSION LISTS
    # ===============================
    path('conversions/', views.convergent_list, name='convergent_list'),
    path('conversions/today/', views.today_followups, name='today_followups'),
    path('conversions/overdue/', views.overdue_followups, name='overdue_followups'),
    path('attendance/', views.attendance, name='attendance'),
path('attendance/admin/', views.attendance_admin, name='attendance_admin'),
path('attendance/report/', views.attendance_report, name='attendance_report'),
path('check-in/', views.check_in, name='check_in'),
path('check-out/', views.check_out, name='check_out'),
path('apply-leave/', views.apply_leave, name='apply_leave'),
path('leave-admin/', views.leave_admin, name='leave_admin'),
path('approve-leave/<int:pk>/', views.approve_leave, name='approve_leave'),
path('reject-leave/<int:pk>/', views.reject_leave, name='reject_leave'),
path('attendance/download/', views.download_attendance_excel, name='download_attendance_excel'),
]