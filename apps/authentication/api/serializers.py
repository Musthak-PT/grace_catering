from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.hashers import make_password
from apps.users.models import Users
from solo_core.helpers.helper import ConvertBase64File
from uuid import uuid4


class UserRegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=255, min_length=4)
    email = serializers.EmailField(max_length=255)
    first_name = serializers.CharField(max_length=255, min_length=4)
    last_name = serializers.CharField(max_length=255, min_length=2)
    is_active = serializers.BooleanField(default = True)

    class Meta:
        model = Users
        fields = ['id','phone', 'email', 'first_name','last_name','is_active']

    def validate(self, attrs):
        phone = attrs.get('phone', '')
        email = attrs.get('email', '') 
        
        
        if Users.objects.filter(phone=phone).exists():
            raise serializers.ValidationError(
                {'phone': ('Phone number is already in use')})
            
        if Users.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': ('email address is already in use')})
            
        return super().validate(attrs)

    def create(self, validated_data):
        return Users.objects.create_user(**validated_data)




class UserRegisterUpdateSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    password = serializers.CharField(max_length=65, min_length=8)
    username = serializers.CharField(max_length=255, min_length=4)
    confirm_password = serializers.CharField(max_length=65, min_length=8)

    class Meta:
        model = Users
        fields = ['password', 'username','pk']

    def validate(self, attrs):
        password = attrs.get('password', '')
        confirm_password = attrs.get('confirm_password', None)
        pk = attrs.get('pk', None)

        if confirm_password != password:
            raise serializers.ValidationError(
                {'password_mismatch': ('password an confirm password are not match')})
        
        
        if not Users.objects.filter(pk=pk).exists():
            raise serializers.ValidationError(
                {'not_found': ('user not found in our system.')})
            
      
        return super().validate(attrs)
    
    

    def update(self):
        pk = self.data.get('pk')
        if pk:
            user = Users.objects.get(pk=pk)
            user.username = self.data.get('username')
            user.set_password(self.data.get('password'))
            user.is_active = True
            user.save()
            return True
        
        return False
        






class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = Users
        fields = ['username', 'password']


class OTPSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=255, min_length=4)

    class Meta:
        model = Users
        fields = ['otp']


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
# Start Login
class LoginSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    
    class Meta:
        model = Users
        fields = ['email','password']
    
    def validate(self, attrs):
        return super().validate(attrs)    
    
# End Login
#--------Start Customer registeration----------
class CustomerRegistrationSerializer(serializers.ModelSerializer):
    email               = serializers.EmailField(required=True)
    password            = serializers.CharField(required=True)
    confirm_password    = serializers.CharField(required=True)
    
    class Meta:
        model = Users
        fields = ['email', 'password', 'confirm_password', ]
        
    def validate(self, attrs):
     
        email               = attrs.get('email')
        password            = attrs.get('password')
        confirm_password    = attrs.get('confirm_password')
        instance_id         = attrs.get('instance_id')
        
        if not instance_id:
            if email and Users.objects.filter(email=email).exists():
                raise serializers.ValidationError({"error": ['Sorry, that email address is already in exists!']})
            if password != confirm_password:
                raise serializers.ValidationError({"error": ['Sorry, Password do not match!']})
            return super().validate(attrs)
    
    def create(self, validated_data):
        request               = self.context.get('request')
        instance              = Users()
        instance.email        = validated_data.get('email', None)
        password              = validated_data.get('password', None)
        confirm_password      = validated_data.get('confirm_password', None)
        if password == confirm_password:
            instance.password = make_password(password)
        instance.user_type    = 2
        instance.save()
        
        return instance
#End registeration
#update customer profile
class UpdateCustomerProfileSerializer(serializers.ModelSerializer):
    
    first_name               = serializers.CharField(max_length=255, required=False)
    last_name                = serializers.CharField(max_length=255, required=False)
    phone_number             = serializers.CharField(required=False)
    alternative_phone_number = serializers.CharField(required=False)
    
    class Meta:
        model  = Users
        fields = ['first_name', 'last_name', 'phone_number', 'alternative_phone_number']
        

    def validate(self, attrs):
        return super().validate(attrs)
    
    
    def update(self, instance, validated_data):
        
        request                           = self.context.get('request')
        # Update User objects
        instance.first_name               = validated_data.get('first_name', None)
        instance.last_name                = validated_data.get('last_name', None)
        instance.phone                    = validated_data.get('phone_number', None)
        instance.alternative_phone        = validated_data.get('alternative_phone_number', None)
        instance.save()
        return instance
#End
#Update profile picture
class UpdateCustomerProfilePictureSerializer(serializers.ModelSerializer):
    image               = serializers.CharField(required=False)
    
    class Meta:
        model  = Users
        fields = ['image']
        
    def validate(self, attrs):
        return super().validate(attrs)
    
    def update(self, instance, validated_data):
        # import pdb;pdb.set_trace()
        request       = self.context.get('request')
        profile_pic   = validated_data.get('image', None)
        if validated_data.get('image', None):
            extension           = ConvertBase64File.base64_file_extension(profile_pic)
            output_schema_xsd   = ConvertBase64File.base64_to_file(profile_pic)
            unique_filename     = f'{uuid4()}.{extension}'                    
            instance.image.save(unique_filename, output_schema_xsd, save = True)
        instance.save()
        return instance
#End Update profile picture
#Customer login serializer
class CustomerLoginSerializer(serializers.ModelSerializer):
    email       = serializers.EmailField(required=True)
    password    = serializers.CharField(required=True)
    
    class Meta:
        model  = Users
        fields = ['email', 'password']
        
    def validate(self, attrs):
        return super().validate(attrs) 
#End of Customer login