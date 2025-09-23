from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse
from .models import Report
from .forms import ReportForm, AdminUpdateForm

def is_superuser(user):
    return user.is_active and user.is_superuser

@login_required
def report_create(request):
    """User submits a report/bug."""
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            rpt = form.save(commit=False)
            rpt.reporter = request.user
            rpt.save()
            messages.success(request, 'Report submitted — thank you! The admin will review it.')
            # Optionally email admin(s) here
            return redirect('report_user_list')
    else:
        form = ReportForm()
    return render(request, 'reports/report_form.html', {'form': form, 'title': 'Submit a Bug / Issue'})

@login_required
def report_user_list(request):
    """List of reports submitted by the current user."""
    reports = Report.objects.filter(reporter=request.user).order_by('-created_at')
    return render(request, 'reports/report_user_list.html', {'reports': reports})

@login_required
def report_user_detail(request, pk):
    """Detail view for a user's own report (read-only except for attachments)."""
    report = get_object_or_404(Report, pk=pk, reporter=request.user)
    return render(request, 'reports/report_user_detail.html', {'report': report})

# --------------------------
# Admin / superuser views
# --------------------------
@user_passes_test(is_superuser)
def admin_report_list(request):
    """Superuser: view all reports with basic filters via GET params (status/priority)."""
    status = request.GET.get('status')
    priority = request.GET.get('priority')

    qs = Report.objects.all()

    if status:
        qs = qs.filter(status=status)
    if priority:
        qs = qs.filter(priority=priority)

    qs = qs.select_related('reporter', 'resolved_by').order_by('-created_at')
    return render(request, 'reports/admin_report_list.html', {'reports': qs})

@user_passes_test(is_superuser)
def admin_report_detail(request, pk):
    """Superuser: view and update a particular report."""
    report = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        form = AdminUpdateForm(request.POST, instance=report)
        if form.is_valid():
            updated = form.save()
            messages.success(request, 'Report updated.')
            # Optionally notify reporter by email here
            return redirect(reverse('admin_report_detail', args=[report.pk]))
    else:
        form = AdminUpdateForm(instance=report)
    return render(request, 'reports/admin_report_detail.html', {'report': report, 'form': form})
