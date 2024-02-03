from django.urls import path, re_path, include
from . import views

urlpatterns = [       
   re_path(r'^web/', include([
      path('get-all-AccommodationType', views.GetAllAccommodationTypeWebAPIView.as_view()),
      path('get-all-PropertyCollection', views.GetAllPropertyCollectionWebAPIView.as_view()),
      path('get-all-PropertyFacility', views.GetAllPropertyFacilityWebAPIView.as_view()),
      path('get-all-PropertyFacility', views.GetAllPropertyFacilityWebAPIView.as_view()),
      path('property-filtering-and-sorting', views.GetPropertyFilteringWebAPIView.as_view()),
   ])),
]