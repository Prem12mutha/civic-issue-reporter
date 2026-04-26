from django import forms
from django.contrib.auth.models import User
from .models import Complaint, ComplaintUpdate


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            'title', 'category', 'description', 'image',
            'municipality', 'ward',
            'address', 'phone', 'email',
            'latitude', 'longitude',
        ]
        widgets = {
            'address':   forms.HiddenInput(),
            'latitude':  forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }


class StatusUpdateForm(forms.ModelForm):
    """Form officers use to update complaint status + add a note."""
    class Meta:
        model  = ComplaintUpdate
        fields = ['new_status', 'note', 'resolution_image']
        widgets = {
            'new_status': forms.Select(
                choices=Complaint.STATUS_CHOICES,
                attrs={'class': 'officer-select'}
            ),
            'note': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Add a note for the citizen (optional)…',
                'class': 'officer-textarea'
            }),
            'resolution_image': forms.ClearableFileInput(attrs={'class': 'officer-file'}),
        }
        labels = {
            'new_status':       'Change Status To',
            'note':             'Officer Note',
            'resolution_image': 'Attach Resolution Photo (optional)',
        }
