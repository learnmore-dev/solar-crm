# leads/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from django.db.models.functions import TruncMonth
from datetime import date

from .models import Lead  # ✅ Added Payment import
from .forms import LeadForm
from django.contrib.auth.decorators import login_required
from .forms import EnquiryForm, LeadForm


# ===============================
# DASHBOARD
# ===============================
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncMonth
from datetime import date
from .models import Lead
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    today = date.today()

    # ================= BASIC COUNTS =================
    total_leads = Lead.objects.count()
    converted_leads = Lead.objects.filter(status='converted').count()
    created_today = Lead.objects.filter(created_at__date=today).count()
    not_followed_up = Lead.objects.filter(follow_up_date__isnull=True).count()

    # ================= STATUS COUNTS =================
    status_counts = (
        Lead.objects
        .values('status')
        .annotate(count=Count('id'))
        .order_by()
    )

    # ================= SOURCE COUNTS =================
    source_counts = (
        Lead.objects
        .values('source')
        .annotate(count=Count('id'))
        .order_by()
    )

    # ================= RECENT LEADS =================
    recent_leads = Lead.objects.order_by('-created_at')[:5]

    # ================= FOLLOWUPS =================
    today_followups = Lead.objects.filter(follow_up_date=today)
    overdue_followups = Lead.objects.filter(follow_up_date__lt=today)

    # ================= MONTHLY LEADS (FIXED) =================
    monthly_leads = (
        Lead.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    context = {
        'total_leads': total_leads,
        'converted_leads': converted_leads,
        'created_today': created_today,
        'not_followed_up': not_followed_up,
        'status_counts': status_counts,
        'source_counts': source_counts,
        'recent_leads': recent_leads,
        'today_followups': today_followups,
        'overdue_followups': overdue_followups,
        'monthly_leads': monthly_leads,
    }

    return render(request, 'leads/dashboard.html', context)

# ===============================
# LEAD PAGES
# ===============================
@login_required
def enquiry(request):
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.status = 'new'
            lead.save()
            return redirect('leads:lead_list')
    else:
        form = EnquiryForm()

    return render(request, 'leads/enquiry.html', {'form': form})

@login_required
def lead_list(request):
    query = request.GET.get("q", "").strip()
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    leads = Lead.objects.all()

    # Search filter
    if query:
        leads = leads.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )

    # Date filter
    if start_date and end_date:
        leads = leads.filter(created_at__date__range=[start_date, end_date])

    leads = leads.order_by("-created_at")

    return render(request, "leads/lead_list.html", {
        "leads": leads,
        "query": query,
        "start_date": start_date,
        "end_date": end_date
    })
@login_required
def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    return render(request, "leads/lead_detail.html", {"lead": lead})


@login_required

def add_lead(request):
    if request.method == "POST":
        form = LeadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Lead added successfully!")
            return redirect("leads:lead_list")
    else:
        form = LeadForm()

    return render(request, "leads/add_lead.html", {"form": form})

@login_required
def lead_edit(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == "POST":
        form = LeadForm(request.POST, request.FILES, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, "Lead updated successfully!")
            return redirect('leads:lead_list')
    else:
        form = LeadForm(instance=lead)

    return render(request, 'leads/lead_edit.html', {'form': form})

@login_required
def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    lead.delete()
    messages.success(request, "Lead deleted successfully!")
    return redirect("leads:lead_list")


# ===============================
# FOLLOW-UPS PAGE (NEW)
# ===============================
def followups(request):
    today = date.today()

    followups = Lead.objects.filter(follow_up_date__isnull=False).order_by("follow_up_date")

    return render(request, "leads/followups.html", {
        "followups": followups,
        "today": today
    })


# ===============================
# OTHER TOP MENU PAGES (DUMMY PAGES)
# ===============================
def tasks(request):
    return render(request, "leads/tasks.html")


def appointments(request):
    return render(request, "leads/appointments.html")


def calls(request):
    return render(request, "leads/calls.html")


def support_tickets(request):
    return render(request, "leads/support_tickets.html")


def mails(request):
    return render(request, "leads/mails.html")


def webpages(request):
    return render(request, "leads/webpages.html")


def webforms(request):
    return render(request, "leads/webforms.html")


def employee_time_tracking(request):
    return render(request, "leads/time_tracking.html")


# ===============================
# INVOICE
# ===============================
def generate_invoice(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)

    invoice_data = {
        "invoice_number": f"INV-{lead.id:05d}",
        "date": lead.created_at,
        "lead_name": lead.name,
        "lead_email": lead.email,
        "lead_phone": lead.phone,
        "status": lead.status,
    }

    return render(request, "leads/invoice.html", {"invoice": invoice_data})


# ===============================
# RECORD PAYMENT
# ===============================
def record_payment(request):
    if request.method == "POST":
        lead_id = request.POST.get("lead_id")
        amount = request.POST.get("amount")

        lead = get_object_or_404(Lead, id=lead_id)
        Payment.objects.create(lead=lead, amount=amount)

        messages.success(request, "Payment recorded successfully!")
        return redirect("leads:dashboard")

    leads = Lead.objects.all()
    return render(request, "leads/record_payment.html", {"leads": leads})


# leads/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Lead
from .forms import ConvergentLeadForm
from django.contrib import messages
@login_required
def convergent_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == "POST":
        form = ConvergentLeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, "Lead stages updated successfully!")
            return redirect('leads:convergent_lead', pk=lead.pk)
    else:
        form = ConvergentLeadForm(instance=lead)

    return render(request, 'leads/convergent_lead.html', {
        'lead': lead,
        'form': form,
    })
# ===============================
# CONVERGENT DASHBOARD + EDIT
# ===============================
from django.db.models import Count
from datetime import date
from .forms import ConvergentLeadForm

@login_required
def convergent_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    today = date.today()

    # Only leads that moved beyond 'new'
    convergent_leads = Lead.objects.exclude(status='new')

    # ===== Summary Cards =====
    total_convergent = convergent_leads.count()
    today_followups = convergent_leads.filter(follow_up_date=today)
    overdue_followups = convergent_leads.filter(follow_up_date__lt=today)

    # ===== Charts Data =====
    status_counts = convergent_leads.values("status").annotate(count=Count("id"))

    # ===== Recent Leads =====
    recent_convergent = convergent_leads.order_by("-created_at")[:5]

    # ===== Form Handling =====
    if request.method == "POST":
        form = ConvergentLeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, "Lead stages updated successfully!")
            return redirect('leads:convergent_lead', pk=lead.pk)
    else:
        form = ConvergentLeadForm(instance=lead)

    context = {
        "lead": lead,
        "form": form,
        "total_convergent": total_convergent,
        "today_followups": today_followups,
        "overdue_followups": overdue_followups,
        "status_counts": status_counts,
        "recent_convergent": recent_convergent,
    }

    return render(request, "leads/convergent_lead.html", context)
@login_required
def convergent_list(request):
    leads = Lead.objects.exclude(status='new').order_by('-created_at')

    context = {
        'leads': leads
    }
    return render(request, 'leads/convergent_list.html', context)
from datetime import date

# All Converted Leads
@login_required
def convergent_list(request):
    leads = Lead.objects.exclude(status='new').order_by('-created_at')
    return render(request, 'leads/convergent_list.html', {'leads': leads})


# Today's Followups
@login_required
def today_followups(request):
    today = date.today()
    leads = Lead.objects.filter(follow_up_date=today).exclude(status='new')
    return render(request, 'leads/convergent_list.html', {
        'leads': leads,
        'title': "Today's Followups"
    })


# Overdue Followups
def overdue_followups(request):
    today = date.today()
    leads = Lead.objects.filter(follow_up_date__lt=today).exclude(status='new')
    return render(request, 'leads/convergent_list.html', {
        'leads': leads,
        'title': "Overdue Followups"
    })
def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    return render(request, 'leads/lead_detail.html', {'lead': lead})

from datetime import datetime, date
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import Attendance
from django.contrib.auth.decorators import login_required

# ✅ Check In
@login_required
def check_in(request):
    today = date.today()

    attendance, created = Attendance.objects.get_or_create(
        user=request.user,
        date=today
    )

    if not attendance.check_in:
        attendance.check_in = datetime.now().time()
        attendance.save()

    return redirect('leads:attendance')


# ✅ Check Out
@login_required
def check_out(request):
    today = date.today()

    attendance = Attendance.objects.filter(
        user=request.user,
        date=today
    ).first()

    if attendance and not attendance.check_out:
        attendance.check_out = datetime.now().time()
        attendance.save()

    return redirect('leads:attendance')


from datetime import date
from django.contrib.auth.decorators import login_required
from .models import Attendance

# ✅ Attendance (User)
@login_required
def attendance(request):
    records = Attendance.objects.filter(user=request.user)

    # ✅ Date filter
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        records = records.filter(date__range=[start_date, end_date])

    records = records.order_by('-date')

    # ❌ REMOVE STATUS LOGIC HERE (IMPORTANT)

    return render(request, "leads/attendance.html", {
        "records": records,
        "start_date": start_date,
        "end_date": end_date
    })


# ✅ Admin Attendance (All Users)
@login_required
def attendance_admin(request):
    records = Attendance.objects.all().order_by('-date')

    # ❌ REMOVE STATUS LOOP HERE

    return render(request, "leads/attendance_admin.html", {
        "records": records
    })



# ✅ Monthly Report
@login_required
def attendance_report(request):
    report = (
        Attendance.objects
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )

    return render(request, "leads/attendance_report.html", {
        "report": report
    })
from .models import Leave
from .forms import LeaveForm

# ===============================
# APPLY LEAVE
# ===============================
@login_required
def apply_leave(request):

    if request.method == "POST":
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.save()

            messages.success(request, "Leave applied successfully!")
            return redirect('leads:apply_leave')

    else:
        form = LeaveForm()

    return render(request, "leads/apply_leave.html", {
        "form": form
    })
def leave_admin(request):
    return render(request, "leads/leave_admin.html")
def leave_admin(request):
    from .models import Leave
    leaves = Leave.objects.all()
    return render(request, "leads/leave_admin.html", {"leaves": leaves})
from .models import Leave

def approve_leave(request, pk):
    leave = get_object_or_404(Leave, pk=pk)
    leave.status = "approved"
    leave.save()
    return redirect('leads:leave_admin')


def reject_leave(request, pk):
    leave = get_object_or_404(Leave, pk=pk)
    leave.status = "rejected"
    leave.save()
    return redirect('leads:leave_admin')
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(lambda u: u.is_superuser)
def leave_admin(request):
    leaves = Leave.objects.all()
    return render(request, "leads/leave_admin.html", {"leaves": leaves})
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Attendance
from django.contrib.auth.decorators import login_required

@login_required
def download_attendance_excel(request):

    # 🔒 Admin only
    if not request.user.is_superuser:
        return HttpResponse("❌ Not allowed")

    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance Report"

    # Header
    ws.append(["User", "Date", "Check In", "Check Out"])

    records = Attendance.objects.all()

    for r in records:
        ws.append([
            r.user.username,
            str(r.date),
            str(r.check_in),
            str(r.check_out)
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=attendance_report.xlsx'

    wb.save(response)
    return response