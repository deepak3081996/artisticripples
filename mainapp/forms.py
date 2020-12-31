from django.forms import (
    ModelForm, Textarea, Form, IntegerField, EmailField
)
from django.core.exceptions import ValidationError
from .models import Quotation

import re

EXPRESSION_TO_MATCH_ALPHABET_WITH_SPACE = re.compile('^[a-z][a-z, ]*$', re.IGNORECASE)

class QuotationForm(ModelForm):
    class Meta:
        model = Quotation
        fields = ['first_name',
                  'last_name',
                  'email',
                  'phone_number',
                  'quotation',
                  'customization',
                  'product']
        widgets = {
            'quotation': Textarea(attrs={'cols': 80, 'rows': 10}),
            'customization': Textarea(attrs={'cols': 80, 'rows': 10}),
        }
        exclude = ('user','author_comment')
        help_texts = {
                      'first_name': 'Required. 50 characters or fewer. Letters only.',
                      'last_name': 'Required. 50 characters or fewer. Letters only.',
                      'email':'Required.',
                      'quotation':'Required.',
                      'customization':'Required.',
                      }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.fields[ 'email' ].widget.attrs[ 'placeholder' ]="example@domain.com"
        self.fields[ 'first_name' ].widget.attrs[ 'placeholder' ]="Enter First Name"
        self.fields[ 'last_name' ].widget.attrs[ 'placeholder' ]="Enter Last Name"        
        self.fields[ 'phone_number' ].widget.attrs[ 'placeholder' ]="Enter Your Phone Number"
        self.fields[ 'quotation' ].widget.attrs[ 'placeholder' ]="We will automatically fill this."
        self.fields[ 'customization' ].widget.attrs[ 'placeholder' ]="If you want to add or get something remove or if you have any other query related to this product. Please write to us."
        self.fields[ 'quotation' ].widget.attrs[ 'disabled' ]= "true"
        self.fields[ 'product' ].widget.attrs[ 'disabled' ]= "true"

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if EXPRESSION_TO_MATCH_ALPHABET_WITH_SPACE.match(first_name):
            return first_name
        else:
            raise ValidationError("no special character allowed in First Name except space.")

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if EXPRESSION_TO_MATCH_ALPHABET_WITH_SPACE.match(last_name):
            return last_name
        else:
            raise ValidationError("no special character allowed in Last Name except space.")


class QuotationTrackingForm(Form):
    tracking_id = IntegerField(label='Tracking Id', required=False)
    email = EmailField(label='Email', required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.fields[ 'tracking_id' ].widget.attrs[ 'placeholder' ]="Please enter the tracking id which you recieved during Quote submission."
        self.fields[ 'email' ].widget.attrs[ 'placeholder' ]="Please enter the email id which you used during Quote submission."
     
