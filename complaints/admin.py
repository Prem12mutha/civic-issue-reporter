from django.contrib import admin
from .models import Complaint, OfficerProfile, ComplaintUpdate


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display  = ['title', 'municipality', 'category', 'ward', 'status', 'user', 'created_at']
    list_filter   = ['status', 'municipality', 'category']
    search_fields = ['title', 'ward', 'user__username']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(OfficerProfile)
class OfficerProfileAdmin(admin.ModelAdmin):
    list_display  = ['user', 'municipality', 'designation', 'employee_id', 'phone']
    list_filter   = ['municipality']
    search_fields = ['user__username', 'user__first_name', 'employee_id']


@admin.register(ComplaintUpdate)
class ComplaintUpdateAdmin(admin.ModelAdmin):
    list_display  = ['complaint', 'officer', 'old_status', 'new_status', 'created_at']
    list_filter   = ['new_status']
    readonly_fields = ['created_at']
