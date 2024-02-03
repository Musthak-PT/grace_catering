from django.urls import include, path, re_path
from . import views


urlpatterns = [
    re_path(r'^review/', include([
        path('create-customer-review', views.CreateCustomerReviewWebApiView.as_view()),
        path('get-customer-review', views.GetCustomerReviewWebApiView.as_view()),
    ])),
    
    
]
