from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('feedback/', views.feedback_form, name='feedback_form'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
