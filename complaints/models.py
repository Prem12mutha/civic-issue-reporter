from django.db import models
from django.contrib.auth.models import User


MUNICIPALITY_CHOICES = [
    ('AMC', 'Ahmedabad Municipal Corporation'),
    ('GMC', 'Gandhinagar Municipal Corporation'),
]

STATUS_CHOICES = [
    ('Pending',     'Pending'),
    ('In Progress', 'In Progress'),
    ('Resolved',    'Resolved'),
    ('Rejected',    'Rejected'),
]

CATEGORY_CHOICES = [
    ('road',        'Road & Potholes'),
    ('water',       'Water Supply'),
    ('garbage',     'Garbage & Waste'),
    ('drainage',    'Drainage & Sewage'),
    ('streetlight', 'Street Lighting'),
    ('park',        'Parks & Public Spaces'),
    ('encroach',    'Encroachment'),
    ('noise',       'Noise Pollution'),
    ('other',       'Other'),
]


class Complaint(models.Model):
    MUNICIPALITY_CHOICES = MUNICIPALITY_CHOICES
    STATUS_CHOICES       = STATUS_CHOICES
    CATEGORY_CHOICES     = CATEGORY_CHOICES

    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    title        = models.CharField(max_length=200)
    description  = models.TextField()
    category     = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    image        = models.ImageField(upload_to='complaints/', blank=True, null=True)
    municipality = models.CharField(max_length=3, choices=MUNICIPALITY_CHOICES, default='AMC')
    ward         = models.CharField(max_length=100)
    address      = models.CharField(max_length=500, blank=True, null=True)
    phone        = models.CharField(max_length=15, blank=True, null=True)
    email        = models.EmailField(blank=True, null=True)
    latitude     = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude    = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"


class OfficerProfile(models.Model):
    """Extends a Django User with municipality officer privileges."""
    user         = models.OneToOneField(User, on_delete=models.CASCADE, related_name='officer_profile')
    municipality = models.CharField(max_length=3, choices=MUNICIPALITY_CHOICES)
    designation  = models.CharField(max_length=100, default='Field Officer')
    employee_id  = models.CharField(max_length=20, unique=True)
    phone        = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.municipality})"


class ComplaintUpdate(models.Model):
    """Audit log: every status change an officer makes on a complaint."""
    complaint       = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='updates')
    officer         = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='officer_updates')
    old_status      = models.CharField(max_length=20)
    new_status      = models.CharField(max_length=20)
    note            = models.TextField(blank=True)
    resolution_image = models.ImageField(upload_to='resolutions/', blank=True, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.complaint.title}: {self.old_status} → {self.new_status}"
