from django.http import (
    HttpResponse, HttpResponseRedirect
)
from django.shortcuts import (
    render, redirect
)
from .forms import (
    QueryForm, TrackingForm, FeedbackForm
)
from django.views import View
from django.contrib import messages
from django.db import models
from django.contrib.auth import get_user_model
from .models import QueryUpdate


def get_anonymous_user():
    return get_user_model().objects.get_or_create(username='anonymous.user')[0]

class Node:
    def __init__(self, key):
        self.val = key
        self.right = None

def createRightSkewedTree(hasUpdates,queryUpdateForQuery,queryUpdate):
    if hasUpdates:
        treeList = []
        for update in queryUpdateForQuery:
            tree = Node(update)
            childUpdates = queryUpdate.filter(updated_query_id = update.query_update_id)
            tree.right = createRightSkewedTree(len(childUpdates)!=0, childUpdates, queryUpdate)
            treeList.append(tree)
        return treeList
    return None
                    
class Feedback(View):
    def get(self, request, *args, **kwargs):
        default_data = {}
        
        if request.user.is_authenticated:
            default_data = {'email': request.user.email,
                            'first_name':request.user.first_name,
                            'last_name':request.user.last_name,
                            }
            form = FeedbackForm(default_data)
            return render(request, "contact/contactQuery.html", {'form': form})
            
        form=FeedbackForm()
        return render(request, "contact/feedbackForm.html", {'form': form})

    def post(self, request, *args, **kwargs):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            query = form.save(commit=False)
            query.user = get_anonymous_user()
            query.save()
            successMessage = "We have successfully received your feedback."
            messages.success(request,successMessage)
            return redirect('querysuccess')
        
        return render(request, "contact/feedbackForm.html", {'form': form})


    
class TrackingView(View):

    def get(self, request, *args, **kwargs):
        form=TrackingForm()
        return render(request, "contact/trackingform.html", {'form': form})

    def post(self, request, *args, **kwargs):
        form = TrackingForm(request.POST)
        result = {}
        result['hasUpdates'] = 0
        if form.is_valid():
            tracking_id = form.cleaned_data.get("tracking_id")
            queryUpdate = QueryUpdate.objects.all()
            queryUpdateForQuery = queryUpdate.filter(query_id=tracking_id).order_by('-update_date')
            hasUpdates = len(queryUpdateForQuery) != 0
            result['hasUpdates'] = int(hasUpdates)
            result['updates'] = queryUpdateForQuery
            rightSkewedTreeList = ''
            
            if hasUpdates:
##                for update in queryUpdateForQuery:
                treeList = createRightSkewedTree(hasUpdates,queryUpdateForQuery, queryUpdate)
                
                
                rightSkewedTreeList = treeList
            result['rightSkewedTreeList']=rightSkewedTreeList
##            for update in queryUpdateForQuery:
##                print(update.update_date)
        print(result)
        return render(request, "contact/trackingform.html", {'form': form, 'result':result})
        
    
class QueryView(View):

    def get(self, request, *args, **kwargs):
        default_data = {}
        
        if request.user.is_authenticated:
            default_data = {'email': request.user.email,
                            'first_name':request.user.first_name,
                            'last_name':request.user.last_name,
                            }
            form = QueryForm(default_data)
            return render(request, "contact/contactQuery.html", {'form': form})
            
        form = QueryForm()
        return render(request, "contact/contactQuery.html", {'form': form})

    def post(self, request, *args, **kwargs):
        form = QueryForm(request.POST)
        successMessage = "";
        
        if form.is_valid():
            query = form.save(commit=False)
            
            if request.user.is_authenticated:
                query.user = request.user
            else:
                print(get_anonymous_user())
                query.user = get_anonymous_user()
                
            query.save()
            successMessage = f"We have successfuly received your query, Use Ticket Id:{query.query_id} to track the status of your query."
            messages.success(request,successMessage)
            return redirect('querysuccess')
        
        return render(request, "contact/contactQuery.html", {'form': form})

class SuccessView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "contact/successPage.html")
