from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# =========================
# PROFILE
# =========================
class Profile(models.Model):
    ROLE_CHOICES = (
        ('candidate', 'Candidate'),
        ('employer', 'Employer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate')

    image = models.ImageField(upload_to='profile/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    skills = models.TextField(blank=True)
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


# AUTO CREATE PROFILE
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# =========================
# JOB
# =========================
class Job(models.Model):

    CATEGORY_CHOICES = (
        ('IT', 'IT'),
        ('Business', 'Business'),
        ('Marketing', 'Marketing'),
        ('Design', 'Design'),
        ('Other', 'Other'),
    )

    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('remote', 'Remote'),
        ('internship', 'Internship'),
    )

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
    )

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200, default="Not Specified")

    responsibility = models.TextField()
    requirements = models.TextField()
    hr_email = models.EmailField(blank=True, null=True)
    hr_phone = models.CharField(max_length=20, blank=True, null=True)

    post_img = models.ImageField(upload_to='job_images/', blank=True, null=True)

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')

    deadline = models.DateTimeField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    views = models.PositiveIntegerField(default=0)

    def is_expired(self):
        return self.deadline < timezone.now()

    def __str__(self):
        return self.title


# =========================
# APPLICATION
# =========================
class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    email = models.EmailField()

    resume = models.FileField(upload_to='resumes/')

    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"
    
STATUS_CHOICES = (
    ('applied', 'Applied'),
    ('reviewing', 'Reviewing'),
    ('shortlisted', 'Shortlisted'),
    ('rejected', 'Rejected'),
)

status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')