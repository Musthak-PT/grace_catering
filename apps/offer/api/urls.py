from django.urls import path, re_path, include
from . import views

urlpatterns = [       
   re_path(r'^web/', include([
      path('get-all-property-offers', views.GetAllPropertyOffersWebAPIView.as_view()),
   ])),
]