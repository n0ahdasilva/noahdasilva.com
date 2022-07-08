from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.core.mail import send_mail
from blog.models import Post
from .forms import ContactForm


#def home(request):
#    return render(request, 'home.html', {})

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
            name = form.cleaned_data['contact_name']
            email = form.cleaned_data['contact_email']
            company = form.cleaned_data['contact_company']
            phone = form.cleaned_data['contact_phone']
            subject = form.cleaned_data['contact_subject']
            message = form.cleaned_data['contact_message']
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def error_404(request, exception):
        data = {}
        return render(request,'404.html', data, status=404)


def error_500(request):
        data = {}
        return render(request,'500.html', data, status=500)