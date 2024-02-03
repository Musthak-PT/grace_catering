from pprint import pprint
from django.shortcuts import render
from rest_framework import status, generics
from apps.property_management.api.schemas import *
from apps.property_management.api.serializers import *
from apps.property_management.models import *
from drf_yasg import openapi
from rest_framework import filters
from solo_core.helpers.response import ResponseInfo
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from solo_core.helpers.pagination import RestPagination

# Create your views here.
# AccommodationType is started
class GetAllAccommodationTypeWebAPIView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAllAccommodationTypeWebAPIView, self).__init__(**kwargs)

    queryset         = AccommodationType.objects.filter().order_by('-id')
    serializer_class = GetAccommodationTypeUsWebResponseSchemas
    filter_backends  = [filters.SearchFilter]
    fields = ['id', 'slug', 'name', 'description']

    id = openapi.Parameter('id', openapi.IN_QUERY,
                                type=openapi.TYPE_INTEGER, required=False, description="Enter id")

    @swagger_auto_schema(tags=["Property management(Web)"], manual_parameters=[id])
    def get(self, request, *args, **kwargs):
        queryset    = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('id', None)
        if instance_id:
            queryset = queryset.filter(pk=instance_id)
        serializer = self.serializer_class(queryset, many=True)
        
        self.response_format['status'] = True
        self.response_format['data']   = serializer.data
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)    
# End AccommodationType

# PropertyCollection is started
class GetAllPropertyCollectionWebAPIView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAllPropertyCollectionWebAPIView, self).__init__(**kwargs)

    queryset         = PropertyCollection.objects.filter().order_by('-id')
    serializer_class = GetPropertyCollectionWebResponseSchemas
    filter_backends  = [filters.SearchFilter]
    fields = ['id', 'slug', 'name', 'description']

    id = openapi.Parameter('id', openapi.IN_QUERY,
                                type=openapi.TYPE_INTEGER, required=False, description="Enter id")

    @swagger_auto_schema(tags=["Property management(Web)"], manual_parameters=[id])
    def get(self, request, *args, **kwargs):
        queryset    = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('id', None)
        if instance_id:
            queryset = queryset.filter(pk=instance_id)
        serializer = self.serializer_class(queryset, many=True)
        
        self.response_format['status'] = True
        self.response_format['data']   = serializer.data
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)    
# End PropertyCollection

# PropertyFacility is started
class GetAllPropertyFacilityWebAPIView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAllPropertyFacilityWebAPIView, self).__init__(**kwargs)

    queryset         = PropertyFacility.objects.filter().order_by('-id')
    serializer_class = GetPropertyFacilityWebResponseSchemas
    filter_backends  = [filters.SearchFilter]
    fields = ['id', 'slug', 'name', 'description','image']

    id = openapi.Parameter('id', openapi.IN_QUERY,
                                type=openapi.TYPE_INTEGER, required=False, description="Enter id")

    @swagger_auto_schema(tags=["Property management(Web)"], manual_parameters=[id])
    def get(self, request, *args, **kwargs):
        queryset    = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('id', None)
        if instance_id:
            queryset = queryset.filter(pk=instance_id)
        serializer = self.serializer_class(queryset, many=True)
        
        self.response_format['status'] = True
        self.response_format['data']   = serializer.data
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)    
# End PropertyFacility
#Start
class GetPropertyFilteringWebAPIView(generics.GenericAPIView):
    
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetPropertyFilteringWebAPIView, self).__init__(**kwargs)
    
    queryset            = PropertyManagement.objects.filter().order_by('-id')
    serializer_class    = PropertyFilteringSerializer
    serializer          = FilterPropertyManagementSchema
    pagination_class    = RestPagination
    filter_backends     = [filters.SearchFilter]
    @swagger_auto_schema(tags=["Property management(Web)"])
    def post(self, request):
        room_type_name = request.data.get('room_type', None)
        queryset = self.get_queryset()
        if room_type_name:
            room_list = list(HotelRoom.objects.filter(room_type_id__in=room_type_name).values_list('id', flat=True))
            property_room_type_obj = list(PropertyManagementHotelRoom.objects.filter(hotel_room_id__in=room_list).values_list('property_management', flat=True).distinct())
            queryset = queryset.filter(id__in=property_room_type_obj)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer(page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)
#End