from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "message")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com", "autocomplete": "email"}),
            "message": forms.Textarea(attrs={"class": "form-control", "placeholder": "How can we help?", "rows": 5}),
        }

    def clean_name(self):
        return self.cleaned_data["name"].strip()

    def clean_message(self):
        return self.cleaned_data["message"].strip()
