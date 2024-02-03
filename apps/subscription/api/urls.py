from django.urls import re_path,path, include
from . import views

urlpatterns = [
    re_path(r'^enquiry/', include([
        path('subscribe', views.SubscriptionApiView.as_view()),
    ]))
]