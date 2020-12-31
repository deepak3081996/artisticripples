from django.forms import (
    ModelForm, Textarea, Form, IntegerField
)
from django.core.exceptions import ValidationError
from .models import (
    Query, Feedback
)

import re

EXPRESSION_TO_MATCH_ALPHABET_WITH_SPACE = re.compile('^[a-z][a-z, ]*$', re.IGNORECASE)

class TrackingForm(Form):
    tracking_id = IntegerField(label='Tracking Id',
                                      required=True,
                                      error_messages={'required': 'Please enter your Tracking Id'}
                                     )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.fields[ 'tracking_id' ].widget.attrs[ 'placeholder' ]="Please enter the tracking id which you recieved during query submission."
                                  
class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['first_name',
                  'last_name',
                  'email',
                  'phone_number', 'feedback']
        widgets = {
            'feedback': Textarea(attrs={'cols': 80, 'rows': 10}),
        }
        exclude = ('user',)
        help_texts = {
                      'first_name': '50 characters or fewer. Letters only.',
                      'last_name': '50 characters or fewer. Letters only.',
                      'email':'',
                      'feedback':'Required.',
                      }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.fields[ 'email' ].widget.attrs[ 'placeholder' ]="example@domain.com"
        self.fields[ 'first_name' ].widget.attrs[ 'placeholder' ]="Enter First Name"
        self.fields[ 'last_name' ].widget.attrs[ 'placeholder' ]="Enter Last Name"
        self.fields[ 'phone_number' ].widget.attrs[ 'placeholder' ]="Enter Your Phone Number"
        self.fields[ 'feedback' ].widget.attrs[ 'placeholder' ]="Please Enter Your feedback we will sincerly appreciate your concern."

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if  not first_name or EXPRESSION_TO_MATCH_ALPHABET_WITH_SPACE.match(first_name):
            return first_name
        else:
            raise ValidationError("no special character allowed in First Name except space.")

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not last_name or EXPRESSION_TO_MATCH_ALPHABET_WITH_SPACE.match(last_name):
            return last_name
        else:
            raise ValidationError("no special character allowed in Last Name except space.")

class QueryForm(ModelForm):
    class Meta:
        model = Query
        fields = ['first_name',
                  'last_name',
                  'email',
                  'phone_number', 'subject', 'query']
        widgets = {
            'query': Textarea(attrs={'cols': 80, 'rows': 10}),
        }
        exclude = ('user',)
        help_texts = {'subject': 'Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only.',
                      'first_name': 'Required. 50 characters or fewer. Letters only.',
                      'last_name': 'Required. 50 characters or fewer. Letters only.',
                      'email':'Required.',
                      'query':'Required.',
                      }

    def __init__(self, *args, **kwargs):
        super( QueryForm, self ).__init__(*args, **kwargs)        
        self.fields[ 'email' ].widget.attrs[ 'placeholder' ]="example@domain.com"
        self.fields[ 'first_name' ].widget.attrs[ 'placeholder' ]="Enter First Name"
        self.fields[ 'last_name' ].widget.attrs[ 'placeholder' ]="Enter Last Name"
        self.fields[ 'subject' ].widget.attrs[ 'placeholder' ]="Enter Your Subject"
        self.fields[ 'phone_number' ].widget.attrs[ 'placeholder' ]="Enter Your Phone Number"
        self.fields[ 'query' ].widget.attrs[ 'placeholder' ]="Please Enter Your Query or Queries we will try our best to help you."

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


