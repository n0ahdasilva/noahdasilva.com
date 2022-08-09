from cgi import print_environ
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth.models import update_last_login
from django.utils import timezone
from django.dispatch import receiver
from .models import AuditEntry, User



@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):  
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(action='user_logged_in', ip=ip, username=user.username)
    user.previous_failed_login_attempts = user.failed_login_attempts
    user.failed_login_attempts = 0
    user.save(update_fields=['failed_login_attempts', 'previous_failed_login_attempts'])


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):  
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(action='user_logged_out', ip=ip, username=user.username)


@receiver(user_login_failed)
def user_login_failed_callback(sender, request, credentials, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
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