from django.urls import path
from . import views

urlpatterns = [
    # Citizen
    path('', views.home_view, name='home'),
    path('submit/', views.submit_complaint_view, name='submit_complaint'),
    path('complaint/<int:pk>/', views.complaint_detail_view, name='complaint_detail'),
    path('profile/', views.profile_view, name='profile'),

    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Officer Portal
    path('officer/login/', views.officer_login_view, name='officer_login'),
    path('officer/logout/', views.officer_logout_view, name='officer_logout'),
    path('officer/', views.officer_dashboard_view, name='officer_dashboard'),
    path('officer/complaint/<int:pk>/', views.officer_complaint_detail_view, name='officer_complaint_detail'),
]
