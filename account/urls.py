from django.urls import path
from . import views
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from .forms import CustomSetPasswordForm, CustomPasswordChangeForm

urlpatterns = [
    path('sign-up/', views.SignUpView.as_view(success_url=reverse_lazy('login')), name="sign_up"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('account-activation-sent/', views.AccountActivationSentView.as_view(), name="account_activation_sent"),
    path('email_verification/<uidb64>/<token>/', views.email_verification_view, name="email_verification"),
    path('dashboard/', views.DashboardView.as_view(), name="dashboard"),
    path('delete-account/', views.DeleteAccountView.as_view(), name="delete_account"),
    path('delete-account/done/', views.delete_account_done_view, name="delete_account_done"),
    path('forgot/password-reset/', views.ResetPasswordView.as_view(), name="password_reset"),
    path('forgot/password-reset/sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="password_reset_done.html"), name="password_reset_done"),
    path('forgot/password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="password_reset_confirm.html", form_class=CustomSetPasswordForm), name="password_reset_confirm"),
    path('forgot/password-reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name="password_reset_complete.html"), name="password_reset_complete"),
    path('forgot/password-change/', auth_views.PasswordChangeView.as_view(
        template_name="password_change.html", form_class=CustomPasswordChangeForm), name="password_change"),
    path('forgot/password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name="password_change_done.html"), name="password_change_done"),
]