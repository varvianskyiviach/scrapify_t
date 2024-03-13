from django.urls import path

from products.api import ProductAPIView

urlpatterns = [
    path("all_products/", ProductAPIView.as_view()),
    path("products/<str:product_name>/", ProductAPIView.as_view()),
    path("products/<str:product_name>/<str:product_field>", ProductAPIView.as_view()),
]
