from django.urls import path
from .views import (
    About, Index, ProductDetailView, ProductView, QuotationView,
    QuotationTrackingView, GalleryView
)

urlpatterns = [
    path('about/', About.as_view(), name="about"),
    path('', Index.as_view(), name="index"),
    path('productDetail/<int:pk>', ProductDetailView.as_view(), name="productDetail"),
    path("productview/", ProductView.as_view(), name="ProductView"),
    path("registerQuotation/<int:product_id>", QuotationView.as_view(), name="registerQuotation"),
    path("quotationtracking/", QuotationTrackingView.as_view(), name="quotationtracking"),
    path("gallery/", GalleryView.as_view(), name="gallery"),
]
