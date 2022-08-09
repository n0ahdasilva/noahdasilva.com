from cgi import print_environ
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth.models import update_last_login
from django.utils import timezone
from django.dispatch import receiver
from .models import AuditEntry, User

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    AuditEntry.objects.create(action='user_logged_in', ip=ip, username=user.email)
    user.previous_failed_login_attempts = user.failed_login_attempts
    user.failed_login_attempts = 0
    user.save(update_fields=['failed_login_attempts', 'previous_failed_login_attempts'])


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    AuditEntry.objects.create(action='user_logged_out', ip=ip, username=user.email)


@receiver(user_login_failed)
def user_login_failed_callback(sender, request, credentials, **kwargs):
    ip = get_client_ip(request)
    login_email_used = credentials['username']
    AuditEntry.objects.create(action='user_login_failed', ip=ip, username=login_email_used)
    
    try:
        user = User.objects.get(email=login_email_used)
        user.failed_login_attempts += 1
        user.save(update_fields=['failed_login_attempts'])
    except User.DoesNotExist:
        pass


# Update last login, while also updating previous login form last session
# to inform the user of the last login from their account.
def update_last_and_previous_login(sender, user, **kwargs):
    user.previous_login = user.last_login
    user.last_login = timezone.now()
    user.save(update_fields=['previous_login', 'last_login'])

user_logged_in.disconnect(update_last_login, dispatch_uid='update_last_login')
user_logged_in.connect(update_last_and_previous_login, dispatch_uid='update_last_and_previous_login')