from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^signup/$',views.UserSignupView.as_view()),
    re_path(r'^product/$',views.ProductListView.as_view()),
    re_path(r'^edit_profile/$',views.UserEditProfileView.as_view()),
    re_path(r'^product/(?P<pk>\d+)/$', views.ProductDetailAPIView.as_view()),
    re_path(r'^product/status/(?P<pk>\d+)/$', views.ActivateDeactivateProductView.as_view()),
    ]