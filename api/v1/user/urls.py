from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^signup/$',views.UserSignupView.as_view()),
    re_path(r'^add_product/$',views.AddProductView.as_view()),
    
    ]