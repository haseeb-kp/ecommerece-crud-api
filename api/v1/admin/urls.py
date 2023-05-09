from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^customers/$',views.CustomerListView.as_view()),
    re_path(r'^products/$',views.ProductListView.as_view()),
    re_path(r'^customer/(?P<id>\d+)/$', views.CustomerDetailView.as_view()),
    re_path(r'^customers/(?P<id>\d+)/products/$', views.ProductListAPIView.as_view(), name='product_list'),
    re_path(r'^customers/(?P<id>\d+)/products/(?P<pk>\d+)/$', views.ProductDetailAPIView.as_view(), name='product_detail'),
    
    ]