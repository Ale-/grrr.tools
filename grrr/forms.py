from django import forms
from captcha.fields import CaptchaField
from contact_form.forms import ContactForm


class GrrrContactForm(ContactForm):

    captcha = CaptchaField()
        
    def init(self):
        print("mierda")
