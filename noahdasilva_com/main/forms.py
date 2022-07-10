from django import forms


SUBJECT = [ # (value, display_text),
    ('', 'Select one...'),
    ('General Inquiry', 'General Inquiry'), 
    ('Service Inquiry', 'Service Inquiry'), 
    ('Feedback', 'Feedback'), 
    ('Other', 'Other'),
]

class ContactForm(forms.Form):
    name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'maxlength': '128'}))
    email = forms.EmailField(max_length=256, widget=forms.EmailInput(attrs={'maxlength': '256'}))
    company = forms.CharField(max_length=128, required=False, widget=forms.TextInput(attrs={'maxlength': '128'}))
    phone = forms.CharField(max_length=32, required=False, widget=forms.NumberInput(attrs={'maxlength': '32'}))
    subject = forms.CharField(widget=forms.Select(choices=SUBJECT))
    message = forms.CharField(max_length=2048, required=False, widget=forms.Textarea(attrs={'maxlength': '2048'}))