from django.urls import path
from . import views

urlpatterns = [
    path('warehouse/', views.warehouseHome, name='warehouseHome'),
    path('warehouse/test', views.warehouseTest, name='warehouseTest'),
    path("warehouse/get-all-products/",
         views.getAllProducts, name="getAllProducts"),
    path("warehouse/get-product/<int:pid>/",
         views.getProductData, name="getProductData"),
    path("warehouse/get-new-pid/", views.getNewPid, name="getNewPid"),
    path("warehouse/add-product/", views.addProduct, name="addProduct"),
    path("warehouse/delete-product/", views.deleteProduct, name="deleteProduct"),
    path("warehouse/save-details/", views.saveDetails, name="saveDetails"),
    path("warehouse/get-details/", views.getDetails, name="getDetails"),
]
