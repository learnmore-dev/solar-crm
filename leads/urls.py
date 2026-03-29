from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
app_name = "leads"

urlpatterns = [

    # ===============================
    # DASHBOARD
    # ===============================
    path('', login_required(views.dashboard), name='dashboard'),

    # ===============================
    # LEADS
    # ===============================
    path('leads/', login_required(views.lead_list), name='lead_list'),
    path('leads/add/', login_required(views.add_lead), name='add_lead'),
    path('leads/<int:pk>/', login_required(views.lead_detail), name='lead_detail'),
    path('leads/<int:pk>/edit/', login_required(views.lead_edit), name='lead_edit'),
    path('leads/<int:pk>/delete/', login_required(views.lead_delete), name='lead_delete'),

    # ===============================
    # CONVERGENT LEAD PAGE
    # ===============================
    path('leads/<int:pk>/convergent/', login_required(views.convergent_lead), name='convergent_lead'),

    # ===============================
    # ENQUIRY FORM
    # ===============================
    path('enquiry/', login_required(views.enquiry), name='enquiry'),

    # ===============================
    # FOLLOW-UPS
    # ===============================
    path('followups/', login_required(views.followups), name='followups'),

    # ===============================
    # OTHER TOP MENU PAGES
    # ===============================
    path('tasks/', login_required(views.tasks), name='tasks'),
    path('appointments/', login_required(views.appointments), name='appointments'),
    path('calls/', login_required(views.calls), name='calls'),
    path('support-tickets/', login_required(views.support_tickets), name='support_tickets'),
    path('mails/', login_required(views.mails), name='mails'),
    path('webpages/', login_required(views.webpages), name='webpages'),
    path('webforms/', login_required(views.webforms), name='webforms'),
    path('time-tracking/', login_required(views.employee_time_tracking), name='time_tracking'),

    # ===============================
    # INVOICE & PAYMENT
    # ===============================
    path('invoice/<int:lead_id>/', login_required(views.generate_invoice), name='generate_invoice'),
    path('record-payment/', login_required(views.record_payment), name='record_payment'),

    # ===============================
    # CONVERSION LISTS
    # ===============================
    path('conversions/', login_required(views.convergent_list), name='convergent_list'),
    path('conversions/today/', login_required(views.today_followups), name='today_followups'),
    path('conversions/overdue/', login_required(views.overdue_followups), name='overdue_followups'),

    # ===============================
    # ATTENDANCE
    # ===============================
    path('attendance/', login_required(views.attendance), name='attendance'),
    path('attendance/admin/', login_required(views.attendance_admin), name='attendance_admin'),
    path('attendance/report/', login_required(views.attendance_report), name='attendance_report'),
    path('check-in/', login_required(views.check_in), name='check_in'),
    path('check-out/', login_required(views.check_out), name='check_out'),
    path('apply-leave/', login_required(views.apply_leave), name='apply_leave'),
    path('leave-admin/', login_required(views.leave_admin), name='leave_admin'),
    path('approve-leave/<int:pk>/', login_required(views.approve_leave), name='approve_leave'),
    path('reject-leave/<int:pk>/', login_required(views.reject_leave), name='reject_leave'),
    path('attendance/download/', login_required(views.download_attendance_excel), name='download_attendance_excel'),
]