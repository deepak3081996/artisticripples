from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate

from account.models import Account
import re
EXPRESSION_TO_MATCH_ALPHABET_WITH_SPACE = re.compile('^[a-z][a-z, ]*$', re.IGNORECASE)

class PasswordChangeForm(forms.Form):
    password = forms.CharField(label="Old Pasword", 
                               widget=forms.PasswordInput,
                               help_text="Enter the current Password.")
    password1 = forms.CharField(label='New Password',
                                widget=forms.PasswordInput,
                                help_text=mark_safe('''<div class="container-fluid bg-light ">
                                    <div class="row bg-light ">Your password can’t be too similar to your other personal information.</div>
                                    <div class="row bg-light ">Your password must contain at least 8 characters.</div>
                                    <div class="row bg-light ">Your password can’t be a commonly used password.</div>
                                    <div class="row bg-light ">Your password can’t be entirely numeric.</div>
                                    </div>''')
                                )
    password2 = forms.CharField(label='New Password confirmation',
                                widget=forms.PasswordInput,
                                help_text='Enter the same password as before, for verification.'
                                )
    def __init__(self, *args, **kwargs):
        self.Request = kwargs.pop('Request',None)
        super( PasswordChangeForm, self ).__init__(*args, **kwargs)        
        self.fields['password1'].widget.attrs['placeholder']="Enter New Password"
        self.fields['password2'].widget.attrs['placeholder']="Re-Enter New Password"
        self.fields['password'].widget.attrs['placeholder']="Enter Old Password"
        

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords didn't match")
        return password2

    def clean_password(self):
        useremail = self.Request.user.email
        password = self.cleaned_data.get("password")
        user = authenticate(self.Request, email=useremail, password=password)
        if user is None:
            raise ValidationError("Old Password didn't match")
        return password

    def is_valid(self):
        result = super().is_valid()
##        self.clean_password2()
##        self.clean_password()
        return result 
 

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput,
                                help_text=mark_safe('''<div class="container-fluid bg-light ">
                                    <div class="row bg-light ">Your password can’t be too similar to your other personal information.</div>
                                    <div class="row bg-light ">Your password must contain at least 8 characters.</div>
                                    <div class="row bg-light ">Your password can’t be a commonly used password.</div>
                                    <div class="row bg-light ">Your password can’t be entirely numeric.</div>
                                    </div>''')
                                )
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput,
                                help_text='Enter the same password as before, for verification.'
                                )
    def __init__(self, *args, **kwargs):
        super( UserCreationForm, self ).__init__(*args, **kwargs)        
        self.fields['email'].widget.attrs['placeholder']="example@domain.com"
        self.fields['username'].widget.attrs['placeholder']="user.name"
        self.fields['password1'].widget.attrs['placeholder']="Enter Password"
        self.fields['password2'].widget.attrs['placeholder']="Re-Enter Password"
        self.fields['first_name'].widget.attrs['placeholder']="Enter First Name"
        self.fields['last_name'].widget.attrs['placeholder']="Enter Last Name"
        
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'username')
        help_texts = {'username': 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                      'first_name': 'Required. 150 characters or fewer. Letters only.',
                      'last_name': 'Required. 150 characters or fewer. Letters only.',
                      }

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

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords didn't match")
        return password2

    def is_valid(self):
        result = super().is_valid()
        return result

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ('email', 'password', 'is_active')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
