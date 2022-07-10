from django.urls import path
from . import views
from django.urls import reverse_lazy

urlpatterns = [
    path('sign-up/', views.SignUpView.as_view(success_url=reverse_lazy('login')), name="sign-up"),
    path('dashboard/', views.DashboardView.as_view(), name="dashboard"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.Logout, name="logout"),
]