from django.urls import path
from .views import SignUpView, DashboardView

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name="sign-up"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
]