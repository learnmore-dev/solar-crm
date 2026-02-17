from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count

from .models import Lead, LeadNote, STATUS_CHOICES
from .forms import LeadForm


# ---------------------------
# Enquiry Form View
# ---------------------------
def enquiry_view(request):
    if request.method == "POST":

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        status = request.POST.get("status")
        customer_type = request.POST.get("customer_type")

        Lead.objects.create(
            name=name,
            phone=phone,
            email=email,
            status=status,
            customer_type=customer_type,
        )

        messages.success(request, "Enquiry submitted successfully!")
        return redirect("leads:enquiry")

    return render(request, "leads/enquiry.html")


# ---------------------------
# Lead List View (Search Filter)
# ---------------------------
def lead_list(request):
    query = request.GET.get("q", "").strip()
    leads = Lead.objects.all()

    if query:
        leads = leads.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )

    leads = leads.order_by("-created_at")

    return render(request, "leads/lead_list.html", {
        "leads": leads,
        "query": query,
    })


# ---------------------------
# Lead Detail View
# ---------------------------
def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == "POST":
        note_text = request.POST.get("note")
        if note_text:
            LeadNote.objects.create(lead=lead, note=note_text)
            messages.success(request, "Note added successfully!")
            return redirect("leads:lead_detail", pk=pk)

    return render(request, "leads/lead_detail.html", {
        "lead": lead,
        "notes": lead.notes.all().order_by("-created_at"),
    })


# ---------------------------
# Add Lead View
# ---------------------------
def add_lead(request):
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Lead added successfully!")
            return redirect("leads:lead_list")
    else:
        form = LeadForm()

    return render(request, "leads/add_lead.html", {"form": form})


# ---------------------------
# Edit Lead View
# ---------------------------
def lead_edit(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    if request.method == "POST":
        lead.name = request.POST['name']
        lead.email = request.POST['email']
        lead.phone = request.POST['phone']
        lead.status = request.POST['status']
        lead.save()

        messages.success(request, "Lead updated successfully!")
        return redirect('leads:lead_list')

    return render(request, 'leads/lead_edit.html', {
        'lead': lead,
        'status_choices': STATUS_CHOICES
    })


# ---------------------------
# Delete Lead View
# ---------------------------
def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    lead.delete()

    messages.success(request, "Lead deleted successfully!")
    return redirect("leads:lead_list")


# ---------------------------
# Dashboard View
# ---------------------------
def dashboard(request):
    total_leads = Lead.objects.count()

    status_data = (
        Lead.objects
        .values("status")
        .annotate(count=Count("id"))
    )

    status_counts = []
    for item in status_data:
        status_counts.append({
            "status": item["status"].capitalize(),
            "count": item["count"]
        })

    context = {
        "total_leads": total_leads,
        "status_counts": status_counts,
    }

    return render(request, "leads/dashboard.html", context)


# ---------------------------
# Generate Invoice
# ---------------------------
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


# ---------------------------
# Record Payment
# ---------------------------
def record_payment(request):
    if request.method == "POST":
        messages.success(request, "Payment recorded successfully!")
        return redirect("leads:dashboard")

    return render(request, "leads/record_payment.html")
