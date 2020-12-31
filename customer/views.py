from django.shortcuts import (
    render, redirect
)
from django.http import HttpResponse
from django.views import View
from django.contrib import messages
from account.forms import (
    UserCreationForm, PasswordChangeForm
)
from django.contrib.auth import (
    authenticate, login, logout, update_session_auth_hash
)
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .forms import (
    CustomerLoginForm, ReviewForm
)
from .models import Review
from mainapp.models import Product
# Create your views here.

class ReviewView(View):

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id', 0)
        product = Product.objects.filter(product_id = product_id)[0]
        review = Review.objects.filter(product_id = product_id)
        
        if request.user.is_authenticated:
            form = ReviewForm({'product':product})
            return render(request, "customer/addreview.html", {'form':form, 'product':product})
        else:
            form = ReviewForm({'review_content':"Your are not authorised to access this form."})
            return render(request, "customer/addreview.html", {'form':form, 'product':product})

    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)

        if form.is_valid():
            product_id = kwargs.get('product_id', 0)
            product = Product.objects.filter(product_id = product_id)[0]
            review = form.save(commit=False)
            review.user  = request.user
            review.product = product
            review.save()
            return redirect(f'/productDetail/{product.product_id}')
        return render(request, "customer/addreview.html", {'form':form, 'product':product})

class ReplywView(View):
    
    def get(self, request, *args, **kwargs):
        previous_review_id = kwargs.get('review_id', 0)
        previous_review = Review.objects.filter(review_id = previous_review_id)[0]

        if request.user.is_authenticated:
            form = ReviewForm()
            return render(request, "customer/addreply.html", {'form':form, 'previous_review':previous_review})
        else:
            form = ReviewForm({'review_content':"Your are not authorised to access this form."})
            return render(request, "customer/addreply.html", {'form':form, 'previous_review':previous_review})

    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)

        if form.is_valid():
            previous_review_id = kwargs.get('review_id', 0)
            previous_review = Review.objects.filter(review_id = previous_review_id)[0]
            review = form.save(commit=False)
            review.user  = request.user
            review.previous_review = previous_review
            review.save()
            product = self._traverse_back_to_product(previous_review)
            return redirect(f'/productDetail/{product.product_id}')
        return render(request, "customer/addreply.html", {'form':form, 'previous_review':previous_review})

    def _traverse_back_to_product(self, previous_review):
        if previous_review.product:
            return previous_review.product
        return self._traverse_back_to_product(previous_review.previous_review)



class ChangePasswordView(View):

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm()
        return render(request, "customer/change_password.html", {'form':form})

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.POST, Request=request)

        if form.is_valid():
            useremail = request.user.email
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=useremail, password=password)
            if user is not  None:
                user.set_password(form.cleaned_data["password1"])
                user.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('/')
        return render(request, "customer/change_password.html", {'form':form})
    
class RegisterView(View):
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request,f"You have been already logged in using user {request.user.username}")
            return redirect('/')
        form = UserCreationForm()
        return render(request, "customer/register.html", {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user_name = user.username
            messages.success(request, f'{user_name} is registered successfully.')            
            user = authenticate(request, email=user.email, password=form.cleaned_data.get("password1"))
            if user is not None:
                login(request, user)
                messages.success(request, f'{user_name} is logedin successfully.')
    
            return redirect('/')
        return render(request, "customer/register.html", {'form': form})


class LoginView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request,f"You have been already logged in using user {request.user.username}")
            return redirect('/')
        form = CustomerLoginForm()
        return render(request, "customer/login.html", {"form":form})

    def post(self, request, *args, **kwargs):
        form = CustomerLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"user loged in successfuly {user.username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid User name or password.")
                return render(request, "customer/login.html", {"form":form})
    
@login_required(login_url='/customer/login/')
def logout_view(request):
    return logout_then_login(request, login_url='/customer/login/')
