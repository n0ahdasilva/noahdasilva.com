from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.http import BadHeaderError, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.core.mail import send_mail
import requests
from django.conf import settings
from blog.models import Post
from .forms import ContactForm


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-created_on']


def about_view(request):
    return render(request, 'about.html', {})


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # reCAPTCHA validation
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post(settings.RECAPTCHA_URL, data=data)
            result = r.json()

            # If reCAPTCHA validation is successful
            if result['success'] and result['score'] > 0.5:
                # client is human
                name = form.cleaned_data['name']
                from_email = form.cleaned_data['email']
                company = form.cleaned_data['company']
                phone = form.cleaned_data['phone']
                subject = form.cleaned_data['subject']
                raw_message = form.cleaned_data['message']

                formatted_message = 'NAME: ' + name + '\nEMAIL: ' + from_email + '\nCOMPANY: ' + company + '\nPHONE: ' + phone + '\nSUBJECT: ' + subject + '\n\nMESSAGE:\n' + raw_message
                
                try:
                    send_mail(
                        'noahdasilva.com Contact Form',
                        formatted_message,
                        from_email,
                        ['noah@noahdasilva.com',],
                    )
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return render(request, 'contact.html', {'form': form, 'from_email': from_email})

            # If reCAPTCHA validation is unsuccessful
            else:
                return HttpResponse('Invalid reCAPTCHA. Please try again.')
    
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form, 'recaptcha_site_key':settings.RECAPTCHA_SITE_KEY})


def terms_and_conditions_view(request):
    return render(request, 'terms_and_conditions.html', {})


def privacy_policy_view(request):
    return render(request, 'privacy_policy.html', {})


def error_404(request, exception):
        data = {}
        return render(request,'404.html', data, status=404)


def error_500(request):
        data = {}
        return render(request,'500.html', data, status=500)