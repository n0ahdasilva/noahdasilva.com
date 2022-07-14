from django.urls import path
from . import views
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('sign-up/', views.SignUpView.as_view(success_url=reverse_lazy('login')), name="sign-up"),
    path('dashboard/', views.DashboardView.as_view(), name="dashboard"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.Logout, name="logout"),
    path('forgot/password-reset/', auth_views.PasswordResetView.as_view(
        template_name="password_reset.html"), name="password_reset"),
    path('forgot/password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name="password_reset_done.html"), name="password_reset_done"),
    path('forgot/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="password_reset_confirm.html"), name="password_reset_confirm"),
    path('forgot/reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name="password_reset_complete.html"), name="password_reset_complete"),
    path('forgot/password-change/', auth_views.PasswordChangeView.as_view(
        template_name="password_change.html"), name="password_change"),
    path('forgot/password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name="password_change_done.html"), name="password_change_done"),
]