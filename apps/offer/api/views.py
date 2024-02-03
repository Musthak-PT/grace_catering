from django.shortcuts import render
from rest_framework import status, generics
from apps.offer.api.schemas import GetAllPropertyOfferSchemas
from apps.offer.models import PropertyOffer
from drf_yasg import openapi
from rest_framework import filters
from solo_core.helpers.response import ResponseInfo
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
# Property Offer section is started
class GetAllPropertyOffersWebAPIView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAllPropertyOffersWebAPIView, self).__init__(**kwargs)

    queryset         = PropertyOffer.objects.filter().order_by('-id')
    serializer_class = GetAllPropertyOfferSchemas
    filter_backends  = [filters.SearchFilter]
    # permission_classes = [IsAuthenticated]
    search_fields    = ['slug']

    id = openapi.Parameter('id', openapi.IN_QUERY,
                                type=openapi.TYPE_INTEGER, required=False, description="Enter Property Offer id:")

    @swagger_auto_schema(tags=["Property Offer"], manual_parameters=[id])
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
# End