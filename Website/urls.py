from django.urls import path
from . import views

urlpatterns = [
    path('test', views.websiteTest, name='websiteTest'),
    path('', views.index, name='index'),
    path('home', views.index, name='home'),
    path('product', views.getProductPage, name='getProductPage'),
    path('category', views.getCategoryPage, name='getCategoryPage'),
    path('tag', views.getTagPage, name='getTagPage'),
    path('signup-request', views.signupRequest, name='signupRequest'),
    path('login-request', views.loginRequest, name='loginRequest'),
    path('add-to-cart', views.addToCart, name='addToCart'),
    path('show-cart', views.showCart, name='showCart'),
    path('change-cart-value', views.changeCartValue, name='changeCartValue'),
    path('get-order-summary', views.getOrderSummary, name="getOrderSummary"),
    path('logout-request', views.logoutRequest, name="logoutRequest"),
    path('account', views.getAccountPage, name="getAccountPage"),
    path('save-account-changes', views.saveAccountChanges,
         name="saveAccountChanges"),
    path('change-password', views.changePassword, name='changePassword'),
    path('cancel-order', views.cancelOrder, name='cancelOrder'),

]
