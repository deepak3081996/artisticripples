from django import forms
from django.forms import (
    ModelForm, Textarea
)
from .models import Review


class CustomerLoginForm(forms.Form):
    email = forms.EmailField(label='Email', required=True, error_messages={'required': 'Please enter your Email'})
    password = forms.CharField(label='Password',
                                widget=forms.PasswordInput,
                                required=True
                                )

    def __init__(self, *args, **kwargs):
        super( CustomerLoginForm, self ).__init__(*args, **kwargs)        
        self.fields[ 'email' ].widget.attrs[ 'placeholder' ]="example@domain.com"
        self.fields[ 'password' ].widget.attrs['placeholder']="password"

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['review_content']
        widgets = {
            'review_content': Textarea(attrs={'cols': 80, 'rows': 5}),
        }
        exclude = ('user', 'previous_review', 'product', 'update_date')
        help_texts = {
                      'review_content':'Required.',
                      }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.fields[ 'review_content' ].widget.attrs[ 'placeholder' ]="Please enter your review here."
        
