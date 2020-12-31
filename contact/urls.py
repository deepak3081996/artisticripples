from django.urls import path

from .views import (
    QueryView, SuccessView, TrackingView, Feedback
)

urlpatterns = [
    path('feedback/', Feedback.as_view(), name='feedback'),
    path('query/', QueryView.as_view(), name='query'),
    path('success/', SuccessView.as_view(), name='querysuccess'),
    path('tracker/', TrackingView.as_view(), name='tracking'),
]
