from drf_yasg import openapi
import logging
from apps.users.models import Users
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from solo_core.helpers.custom_messages import _account_tem_suspended,_invalid_credentials
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
import json
from solo_core.response import ResponseInfo
from apps.authentication.api.serializers import RefreshTokenSerializer, UpdateCustomerProfilePictureSerializer, UserRegisterSerializer, LoginSerializer, LogoutSerializer, OTPSerializer, UserRegisterUpdateSerializer, CustomerRegistrationSerializer, UpdateCustomerProfileSerializer, CustomerLoginSerializer
from apps.authentication.api.schemas import FinalRegistrationPostSchema, FinalRegistrationSchema, LoginPostSchema, LoginSchema, RegisterPostSchema, RegisterSchema, UsersSchema, VerifyOTPPostSchema,GetAllCustomerApiViewSchema, AdminLoginSchema
from solo_core import settings
from solo_core.helpers.helper import DataEncryption
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import generics
from solo_core.helpers.custom_messages import _success
from rest_framework import filters



logger = logging.getLogger(__name__)


class RegisterAPIView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(RegisterAPIView, self).__init__(**kwargs)

    serializer_class = RegisterPostSchema

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            user_data = request.data
            user_data.update({'is_active' : False})
            serializer = UserRegisterSerializer(data=user_data)
            if serializer.is_valid():
                if serializer.save():
                    data = {'user': serializer.data, 'errors': {}}
                    self.response_format['status_code'] = status.HTTP_201_CREATED
                    self.response_format["data"] = data
                    self.response_format["status"] = True
                    return Response(self.response_format, status=status.HTTP_201_CREATED)
                else:
                    self.response_format['status_code'] = status.HTTP_200_OK
                    data = {'user': serializer.data, 'errors': {}}
                    self.response_format["data"] = data
                    self.response_format["status"] = True
                    return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                data = {'user': {}, 'errors': serializer.errors}
                self.response_format["data"] = data
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FinalRegistrationAPIView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(FinalRegistrationAPIView, self).__init__(**kwargs)

    serializer_class = FinalRegistrationPostSchema

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            user_data = request.data
            serializer = UserRegisterUpdateSerializer(data=user_data)
            if serializer.is_valid():
                if serializer.update():
                    data = request.data
                    password = data.get('password', '')
                    user_obj = Users.objects.get(pk=data.get('pk', ''))
                    user = auth.authenticate(username=user_obj.email, password=password)
                    if user:
                        refresh = RefreshToken.for_user(user)
                        serializer = FinalRegistrationSchema(user)
                        data = {'user': serializer.data, 'errors': {}, 'token': str(
                            refresh.access_token), 'refresh': str(refresh)}
                        self.response_format['status_code'] = 200
                        self.response_format["data"] = data
                        self.response_format["status"] = True
                        return Response(self.response_format, status=status.HTTP_201_CREATED)
                    else:
                        self.response_format['status_code'] = 106
                        data = {'user': serializer.data, 'errors': {}, 'token': '', 'refresh': ''}
                        self.response_format["data"] = data
                        self.response_format["status"] = True
                        return Response(self.response_format, status=status.HTTP_201_CREATED)
                else:
                    self.response_format['status_code'] = 102
                    data = {'user': {}, 'errors': {},
                            'token': '', 'refresh': ''}
                    self.response_format["data"] = data
                    self.response_format["status"] = False
                    return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            else:
                self.response_format['status_code'] = 102
                data = {'user': {}, 'errors': serializer.errors,
                        'token': '', 'refresh': ''}
                self.response_format["data"] = data
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            self.response_format['status_code'] = 101
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_200_OK)

        

# class LoginAPIView(GenericAPIView):
#     def __init__(self, **kwargs):
#         self.response_format = ResponseInfo().response
#         super(LoginAPIView, self).__init__(**kwargs)

    # serializer_class = LoginPostSchema

#     @swagger_auto_schema(tags=["Authorization"])
#     def post(self, request):
#         try:
#             data = request.data
#             email = data.get('email', '')
#             password = data.get('password', '')
#             user = auth.authenticate(username=email, password=password)            
#             if user:
#                 serializer = LoginSchema(user)

#                 if not user.is_active:
#                     data = {'user': {}, 'token': '', 'refresh': ''}
#                     self.response_format['status_code'] = status.HTTP_202_ACCEPTED
#                     self.response_format["data"] = data
#                     self.response_format["status"] = True
#                     self.response_format["message"] = 'Account Temparary suspended, contact admin'
#                     return Response(self.response_format, status=status.HTTP_200_OK)
#                 else:
#                     refresh = RefreshToken.for_user(user)
#                     data = {'user': serializer.data, 'token': str(
#                         refresh.access_token), 'refresh': str(refresh)}
#                     self.response_format['status_code'] = status.HTTP_200_OK
#                     self.response_format["data"] = data
#                     self.response_format["status"] = True
#                     return Response(self.response_format, status=status.HTTP_200_OK)

#             else:
#                 self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
#                 self.response_format["message"] = 'Invalid credentials'
#                 self.response_format["status"] = False
#                 return Response(self.response_format, status=status.HTTP_401_UNAUTHORIZED)

#         except Exception as e:
#             pass
#             self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
#             self.response_format['status'] = False
#             self.response_format['message'] = str(e)
#             return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Start Login 
class LoginAPIView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(LoginAPIView, self).__init__(**kwargs)
        
    serializer_class = LoginSerializer
    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            email    = serializer.validated_data.get('email', '')
            password = serializer.validated_data.get('password', '')
            try:
                user_instance = Users.objects.get(email=email)
            except:
                user_instance = None
            if user_instance:
                user = auth.authenticate(request=request, username=user_instance.email, password=password)
                
                if user:
                    serializer = LoginSchema(user, context={"request": request})
                    if not user.is_active:
                        data = {'user': {}, 'token': '', 'refresh': ''}
                        self.response_format['status_code'] = status.HTTP_202_ACCEPTED
                        self.response_format["data"] = data
                        self.response_format["status"] = False
                        self.response_format["message"] = _account_tem_suspended
                        return Response(self.response_format, status=status.HTTP_200_OK)
                    else:
                        final_out         = json.dumps(serializer.data)
                        key               = settings.E_COMMERCE_SECRET        
                        encrypted_data    = DataEncryption.encrypt(key, final_out)
                        access_tokens     = AccessToken.for_user(user)
                        refresh_token     = RefreshToken.for_user(user)             
                  
                        
                        data = {'user': encrypted_data, 'token': str(access_tokens), 'refresh': str(refresh_token)}
                        self.response_format['status_code'] = status.HTTP_200_OK
                        self.response_format["data"] = data
                        self.response_format["status"] = True

                        return Response(self.response_format, status=status.HTTP_200_OK)

                else:
                    self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                    self.response_format["message"] = _invalid_credentials
                    self.response_format["status"] = False
                    return Response(self.response_format, status=status.HTTP_401_UNAUTHORIZED)

            else:
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["message"] = _invalid_credentials
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# End Login

class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(LogoutAPIView, self).__init__(**kwargs)

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.response_format['status'] = True
            self.response_format['status_code'] = status.HTTP_200_OK
            return Response(self.response_format, status=status.HTTP_200_OK)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
        
        
        
        
class RefreshTokenView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RefreshTokenSerializer

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(RefreshTokenView, self).__init__(**kwargs)

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            user = Users.objects.get(id=request.user.id)
            refresh = RefreshToken.for_user(user)
            data = {'token': str(
                refresh.access_token), 'refresh': str(refresh)}
            self.response_format['status_code'] = 200
            self.response_format["data"] = data
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)

        except Exception as e:
            self.response_format['status_code'] = 101
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_200_OK)
        
#----start create or update customer registration------------        
class CreateOrUpdateCustomerRegistrationApiView(generics.GenericAPIView):
    
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateCustomerRegistrationApiView, self).__init__(**kwargs)
    
    serializer_class = CustomerRegistrationSerializer
    
    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
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
            self.response_format['message'] = serializer.errors
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#End customer registeration
#Listing Customers
class GetAllCustomerApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAllCustomerApiView, self).__init__(**kwargs)

    queryset         = Users.objects.filter(user_type=2).order_by('-id')
    serializer_class = GetAllCustomerApiViewSchema
    filter_backends  = [filters.SearchFilter]
    # permission_classes = [IsAuthenticated]
    search_fields    = ['email', 'first_name', 'last_name', 'phone']

    id = openapi.Parameter('id', openapi.IN_QUERY,
                                type=openapi.TYPE_INTEGER, required=False, description="Enter Customer id")

    @swagger_auto_schema(tags=["Authorization"], manual_parameters=[id])
    def get(self, request, *args, **kwargs):
        queryset   = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('id', None)
        if instance_id:
            queryset = queryset.filter(pk=instance_id)
            
        serializer = self.serializer_class(queryset, many=True)
        self.response_format['status'] = True
        self.response_format['data']   = serializer.data
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)

#update customer profile
class UpdateProfileCustomerApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(UpdateProfileCustomerApiView, self).__init__(**kwargs)
    
    serializer_class = UpdateCustomerProfileSerializer
    
    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'request':request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            instance = Users.objects.get(id=request.user.id)
            serializer = self.serializer_class(instance, data=request.data, context={'request': request})
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
#End update of customer
#Update profile picture
class UpdateProfilePictureCustomerApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(UpdateProfilePictureCustomerApiView, self).__init__(**kwargs)
    
    serializer_class = UpdateCustomerProfilePictureSerializer
    
    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", request.user.id)
            instance = Users.objects.get(id=request.user.id)
            serializer = self.serializer_class(instance, data=request.data, context={'request': request})
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
#End Update profile picture
#Customer login
class CustomerLoginView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CustomerLoginView, self).__init__(**kwargs)
        
    serializer_class = CustomerLoginSerializer
    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            email    = serializer.validated_data.get('email', '')
            password = serializer.validated_data.get('password', '')
            try:
                user_instance = Users.objects.get(email=email)
            except:
                user_instance = None
            if user_instance:
                user = auth.authenticate(request=request, username=user_instance.email, password=password)
                
                if user:
                    serializer = AdminLoginSchema(user, context={"request": request})
                    if not user.is_active:
                        data = {'user': {}, 'token': '', 'refresh': ''}
                        self.response_format['status_code'] = status.HTTP_202_ACCEPTED
                        self.response_format["data"] = data
                        self.response_format["status"] = False
                        self.response_format["message"] = _account_tem_suspended
                        return Response(self.response_format, status=status.HTTP_200_OK)
                    else:
                        final_out         = json.dumps(serializer.data)
                        key               = settings.E_COMMERCE_SECRET
            
                        encrypted_data    = DataEncryption.encrypt(key, final_out)
                        access_tokens     = AccessToken.for_user(user)
                        refresh_token     = RefreshToken.for_user(user)             
                        
                        data = {'user': encrypted_data, 'token': str(access_tokens), 'refresh': str(refresh_token)}
                        self.response_format['status_code'] = status.HTTP_200_OK
                        self.response_format["data"] = data
                        self.response_format["status"] = True
                        return Response(self.response_format, status=status.HTTP_200_OK)

                else:
                    self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                    self.response_format["message"] = _invalid_credentials
                    self.response_format["status"] = False
                    return Response(self.response_format, status=status.HTTP_401_UNAUTHORIZED)

            else:
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["message"] = _invalid_credentials
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#End of customer login