from rest_framework import serializers
from apps.subscription.models import Subscribers
from apps.subscription.api.subscription_mail import notify_me_subscription_mail_send

#Subscription
class SubscribersSerializer(serializers.ModelSerializer): 
    subscriber_email = serializers.EmailField(required=True)

    class Meta:
        model = Subscribers
        fields=['subscriber_email']

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        request                     = self.context.get('request')
        instance                    = Subscribers()
        instance.subscriber_email   = validated_data.get('subscriber_email',None)
        instance.save()
        notify_me_subscription_mail_send(request, instance)
        return instance
#End
