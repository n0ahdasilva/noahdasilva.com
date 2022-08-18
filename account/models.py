from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class CustomUserManager(BaseUserManager):
    use_in_migration = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, original_email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), unique=True, default='')
    original_email = models.EmailField(_('original email'), default='')
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    username = models.CharField(_('username'), max_length=24, unique=True)
    full_name = models.CharField(_('full name'), max_length=64, null=True, blank=True)
    is_superadmin = models.BooleanField(_('is_superadmin'), default=False)
    is_active = models.BooleanField(_('is_active'), default=True)
    is_staff = models.BooleanField(default=False)
    previous_login = models.DateTimeField(null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    previous_failed_login_attempts = models.IntegerField(default=0)
    otp_secret = models.CharField(_('OTP secret'), max_length=64, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('account')
    
    def get_total_posts_likes(self):
        likes = self.like_set.all()
        total_likes = 0
        for like in likes:
            if like.value == 'Like':
                total_likes += 1
        return total_likes
    
    def get_total_posts_comments(self):
        return self.comment_set.all().count()

    def get_total_posts_written(self):
        return self.post_author.all().count()
    
    def get_profile_score(self):
        score = self.get_total_posts_likes() * 10
        score += self.get_total_posts_comments() * 25
        score += self.get_total_posts_written() * 50
        return score


class AuditEntry(models.Model):
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    username = models.CharField(max_length=256, null=True)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Audit Entry')
        verbose_name_plural = _('Audit Entries')

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)
