from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from .models import Complaint, OfficerProfile, ComplaintUpdate
from .forms import UserRegisterForm, ComplaintForm, StatusUpdateForm
from functools import wraps


# ─────────────────────────────────────────────
# Officer guard decorator
# ─────────────────────────────────────────────
def officer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('officer_login')
        if not hasattr(request.user, 'officer_profile'):
            messages.error(request, 'You do not have officer access.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


# ─────────────────────────────────────────────
# Public / Citizen Views
# ─────────────────────────────────────────────
def home_view(request):
    all_complaints = Complaint.objects.all()
    total    = all_complaints.count()
    pending  = all_complaints.filter(status='Pending').count()
    progress = all_complaints.filter(status='In Progress').count()
    resolved = all_complaints.filter(status='Resolved').count()

    status       = request.GET.get('status')
    municipality = request.GET.get('municipality')
    complaints   = all_complaints.order_by('-created_at')

    if status:
        complaints = complaints.filter(status=status)
    if municipality:
        complaints = complaints.filter(municipality=municipality)

    return render(request, 'home.html', {
        'complaints': complaints,
        'current_status': status,
        'current_municipality': municipality,
        'total': total, 'pending': pending,
        'progress': progress, 'resolved': resolved,
    })


@login_required
def submit_complaint_view(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            messages.success(request, 'Complaint submitted successfully!')
            return redirect('home')
    else:
        form = ComplaintForm()
    return render(request, 'submit_complaint.html', {'form': form})


def complaint_detail_view(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    updates   = complaint.updates.select_related('officer').all()
    return render(request, 'complaint_detail.html', {
        'complaint': complaint,
        'updates': updates,
    })


@login_required
def profile_view(request):
    user_complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'complaints': user_complaints})


# ─────────────────────────────────────────────
# Auth Views
# ─────────────────────────────────────────────
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


# ─────────────────────────────────────────────
# Officer Portal Views
# ─────────────────────────────────────────────
def officer_login_view(request):
    if request.user.is_authenticated and hasattr(request.user, 'officer_profile'):
        return redirect('officer_dashboard')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and hasattr(user, 'officer_profile'):
            login(request, user)
            return redirect('officer_dashboard')
        else:
            error = 'Invalid credentials or you are not a registered officer.'
    return render(request, 'officer/login.html', {'error': error})


def officer_logout_view(request):
    logout(request)
    return redirect('officer_login')


@officer_required
def officer_dashboard_view(request):
    officer = request.user.officer_profile
    qs = Complaint.objects.filter(municipality=officer.municipality).select_related('user')

    # Stats
    total     = qs.count()
    pending   = qs.filter(status='Pending').count()
    in_prog   = qs.filter(status='In Progress').count()
    resolved  = qs.filter(status='Resolved').count()
    rejected  = qs.filter(status='Rejected').count()

    # Filters from GET
    status_filter = request.GET.get('status', '')
    search        = request.GET.get('q', '').strip()
    category      = request.GET.get('category', '')

    complaints = qs.order_by('-created_at')
    if status_filter:
        complaints = complaints.filter(status=status_filter)
    if category:
        complaints = complaints.filter(category=category)
    if search:
        complaints = complaints.filter(
            Q(title__icontains=search) |
            Q(ward__icontains=search) |
            Q(address__icontains=search) |
            Q(user__username__icontains=search)
        )

    return render(request, 'officer/dashboard.html', {
        'officer':        officer,
        'complaints':     complaints,
        'total':          total,
        'pending':        pending,
        'in_progress':    in_prog,
        'resolved':       resolved,
        'rejected':       rejected,
        'status_filter':  status_filter,
        'search':         search,
        'category_filter': category,
        'categories':     Complaint.CATEGORY_CHOICES,
    })


@officer_required
def officer_complaint_detail_view(request, pk):
    officer   = request.user.officer_profile
    complaint = get_object_or_404(Complaint, pk=pk, municipality=officer.municipality)
    updates   = complaint.updates.select_related('officer').all()
    form      = StatusUpdateForm()

    if request.method == 'POST':
        form = StatusUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            update = form.save(commit=False)
            update.complaint  = complaint
            update.officer    = request.user
            update.old_status = complaint.status
            update.save()
            # Apply new status to the complaint
            complaint.status = update.new_status
            complaint.save()
            messages.success(request, f'Status updated to "{update.new_status}".')
            return redirect('officer_complaint_detail', pk=pk)

    return render(request, 'officer/complaint_detail.html', {
        'officer':   officer,
        'complaint': complaint,
        'updates':   updates,
        'form':      form,
    })
