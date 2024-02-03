from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from apps.subscription.api.serializers import SubscribersSerializer
from apps.subscription.api.subscription_mail import notify_me_subscription_mail_send
from apps.subscription.models import Subscribers
from solo_core.helpers.custom_messages import _success
from solo_core.response import ResponseInfo

# Create your views here.
#subscription
class SubscriptionApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(SubscriptionApiView, self).__init__(**kwargs)
        
    serializer_class= SubscribersSerializer
    
    @swagger_auto_schema(tags=["Subscribers"])
    def post(self, request):
        try:
            serializer =self.serializer_class(data=request.data,context={'request':request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            
            self.response_format['status_code']= status.HTTP_201_CREATED
            self.response_format['message']=_success
            self.response_format['status']=True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#End
