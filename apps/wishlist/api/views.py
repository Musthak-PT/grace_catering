from rest_framework import  generics,status
from solo_core.helpers.response import ResponseInfo
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from apps.wishlist.api.serializers import WishListSerializer
from solo_core.helpers.custom_messages import _success
from rest_framework.permissions import IsAuthenticated
from apps.wishlist.models import WishList
# from apps.wishlist.api.schemas import GetWishListResponseSchemas
from solo_core.helpers.pagination import RestPagination
from drf_yasg import openapi

# Create your views here.
class WishlistCreateApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(WishlistCreateApiView, self).__init__(**kwargs)

    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Wishlist(Web)"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data,context = {'request':request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#------End-----
#-----Listing all wishlists------------
# class GetAllWishlistAPIView(generics.ListAPIView): 
#     def __init__(self, **kwargs):
#         self.response_format= ResponseInfo().response
#         super(GetAllWishlistAPIView, self).__init__(**kwargs)
    
#     queryset            = WishList.objects.filter().order_by('-id')
#     serializer_class    = loyalitySchema
#     pagination_class    = RestPagination
#     search_fields       = ['name']
#     queryset            = WishList.objects.all()
    
#     @swagger_auto_schema( pagination_class    = RestPagination,
#      tags = ["Wishlist(Web)"],manual_parameters=[
#             openapi.Parameter(
#                 name          = "loyaltyid",
#                 in_           = openapi.IN_QUERY,
#                 type          = openapi.TYPE_INTEGER,
#                 description   = "User ID for Retreive Wishlisted Properties",
#                 required      = False,
#             ),
#         ],
#     )
    
#     def get(self, request, *args, **kwargs):
#         loyalty_instance_id = request.GET.get('loyaltyid',None)

#         if loyalty_instance_id : 
#             try: 
#                 loyalty = Loyalty.objects.get(id=loyalty_instance_id)
#                 serializer  = self.serializer_class(loyalty)
#                 self.response_format['status_code'] = status.HTTP_200_OK
#                 self.response_format["message"] = _success
#                 self.response_format["status"] = True
#                 self.response_format["data"] = serializer.data
#                 return Response(self.response_format, status = status.HTTP_200_OK)

#             except Loyalty.DoesNotExist: 
#                 self.response_format['status_code']             = status.HTTP_404_NOT_FOUND
#                 self.response_format["message"]                 = "Loyalty not found."
#                 self.response_format["status"]                  = False
#                 return Response(self.response_format, status    = status.HTTP_404_NOT_FOUND)

#         else: 
#             queryset                                        = self.get_queryset()
#             serializer                                      = self.serializer_class(queryset, many=True)
#             self.response_format['status_code']             = status.HTTP_200_OK
#             self.response_format["message"]                 = _success
#             self.response_format["status"]                  = True
#             self.response_format["data"]                    = serializer.data
#             return Response(self.response_format, status    = status.HTTP_200_OK) 