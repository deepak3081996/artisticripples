from django.urls import path

from .views import (
    RegisterView, LoginView, logout_view, ChangePasswordView, ReviewView, ReplywView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name="registerCustomer"),
    path('review/add/<int:product_id>', ReviewView.as_view(), name="review"),
    path('reply/add/<int:review_id>', ReplywView.as_view(), name="reply"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', logout_view, name="logout"),
    path('change_password/', ChangePasswordView.as_view(), name="changePassword"),
]
