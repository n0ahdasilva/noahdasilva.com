from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.http import BadHeaderError, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
import requests
from blog.models import Post
from .forms import ContactForm


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-created_on']


def about_view(request):
    return render(request, 'about.html', {})


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = ''
    extra_context = {
        'recaptcha_key': settings.RECAPTCHA_SITE_KEY
    }

    def form_valid(self, form):
        # Retrieve token
        token = self.request.POST('g-recaptcha-response')
        if token:
            data = {
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': token
            }
            # Verify response with Google
            response = requests.post(
                'https://www.google.com/recaptcha/api/siteverify',
                data = data
            )
            result = response.json()
            # check results
            if result['success'] == True and result['score'] >= 0.5:
                form.save()
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
                return render(self.request, 'contact.html', 
                    {'form': self.get_form(), 'from_email': from_email})
            else:
                return render(self.request, 'contact.html', 
                    {'form': self.get_form()})


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