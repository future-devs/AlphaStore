from django.urls import path
from . import views

urlpatterns = [
    path('test', views.websiteTest, name='websiteTest'),
    path('', views.index, name='index'),
    path("get-product/<int:pid>/",
         views.getProductData, name="getProductData"),
    path("get-random-products/", views.getRandomProducts, name="getRandomProducts"),
    path("get-random-category-products/<int:count>/<str:category>/",
         views.getRandomCategoryProducts, name="getRandomCategoryProducts"),
    path("products/<str:pid>",
         views.getProductPage, name="getProductPage"),



]
