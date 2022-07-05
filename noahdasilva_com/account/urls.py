from django.urls import path
from .views import SignUpView, DashboardView
from django.urls import reverse_lazy

urlpatterns = [
    path('sign-up/', SignUpView.as_view(success_url=reverse_lazy('login')), name="sign-up"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
]