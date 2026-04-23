from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from .models import Job, Application, Profile
from .forms import JobForm, ApplicationForm


# =========================
# HELPERS
# =========================
def is_employer(user):
    return hasattr(user, 'profile') and user.profile.role == 'employer'


# =========================
# REGISTER
# =========================
def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Account created!")
        return redirect('job_list')

    return render(request, 'registration/register.html', {'form': form})


# =========================
# JOB LIST
# =========================
def job_list(request):
    query = request.GET.get('q')
    job_type = request.GET.get('type')

    jobs = Job.objects.filter(
        status='open',
        deadline__gt=timezone.now()
    ).order_by('-created_at')

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company__icontains=query) |
            Q(category__icontains=query) |
            Q(position__icontains=query)
        )

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    return render(request, 'job/job_list.html', {'jobs': jobs})


# =========================
# JOB DETAIL
# =========================
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if not request.session.get(f'viewed_{pk}'):
        job.views += 1
        job.save()
        request.session[f'viewed_{pk}'] = True

    return render(request, 'job/job_detail.html', {'job': job})


# =========================
# CREATE JOB
# =========================
@login_required
def job_create(request):

    if not is_employer(request.user):
        messages.error(request, "Only employers can post jobs")
        return redirect('job_list')

    form = JobForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        job = form.save(commit=False)
        job.owner = request.user
        job.save()
        return redirect('job_detail', pk=job.pk)

    return render(request, 'job/job_form.html', {'form': form})


# =========================
# EDIT JOB ✅ FIXED
# =========================
@login_required
def job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if request.user != job.owner:
        return redirect('job_list')

    form = JobForm(request.POST or None, request.FILES or None, instance=job)

    if form.is_valid():
        form.save()
        messages.success(request, "Job updated")
        return redirect('job_detail', pk=job.pk)

    return render(request, 'job/job_form.html', {'form': form})


# =========================
# DELETE JOB ✅ FIXED
# =========================
@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if request.user != job.owner:
        return redirect('job_list')

    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted")
        return redirect('job_list')

    return render(request, 'job/job_confirm_delete.html', {'job': job})


# =========================
# APPLY JOB
# =========================


@login_required
def job_apply(request, pk):

    job = get_object_or_404(Job, pk=pk)

    # Deadline check
    if job.deadline and job.deadline < timezone.now():
        messages.error(request, "This job has expired")
        return redirect('job_detail', pk=pk)

    # Check if already applied
    already_applied = Application.objects.filter(
        job=job,
        user=request.user
    ).exists()

    form = ApplicationForm(request.POST or None, request.FILES or None)

    if request.method == "POST":

        if already_applied:
            messages.warning(request, "You have already applied for this job")
            return redirect('job_detail', pk=pk)

        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.user = request.user
            app.save()

            messages.success(request, "Application submitted successfully")
            return redirect('job_list')

    return render(request, 'job/job_apply.html', {
        'form': form,
        'job': job,
        'already_applied': already_applied
    })
# =========================
# VIEW APPLICATIONS (EMPLOYER)
# =========================
@login_required
def job_applications(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if request.user != job.owner:
        return redirect('job_list')

    applications = job.applications.all().order_by('-applied_at')

    return render(request, 'job/job_applications.html', {
        'job': job,
        'applications': applications
    })


# =========================
# PROFILE
# =========================
@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})


# =========================
# EDIT PROFILE
# =========================
@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.skills = request.POST.get('skills')
        profile.education = request.POST.get('education')
        profile.experience = request.POST.get('experience')

        if request.FILES.get('image'):
            profile.image = request.FILES['image']

        profile.save()
        messages.success(request, "Profile updated")
        return redirect('profile')

    return render(request, 'edit_profile.html', {'profile': profile})


# =========================
# MY APPLICATIONS ✅ FIXED
# =========================
@login_required
def my_applications(request):
    apps = Application.objects.filter(user=request.user).order_by('-applied_at')
    return render(request, 'applications.html', {'apps': apps})


# =========================
# APPLICATION STATUS ✅ FIXED
# =========================
@login_required
def application_status(request):
    apps = Application.objects.filter(user=request.user).order_by('-applied_at')
    return render(request, 'status.html', {'apps': apps})