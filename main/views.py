from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.http import BadHeaderError, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.core.mail import send_mail
import urllib.request
import urllib.parse
import json
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
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''

            if result['success']:
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
            else:
                return HttpResponse('Invalid reCAPTCHA.')
                
            return render(request, 'contact.html', {'form': form, 'from_email': from_email})
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


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