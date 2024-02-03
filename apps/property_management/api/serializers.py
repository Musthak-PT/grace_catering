from rest_framework import serializers
from apps.property_management.models import *

class PropertyFilteringSerializer(serializers.Serializer):
    room_type =  serializers.ListField(child=serializers.IntegerField(),required = False)

    class Meta:
        model  = RoomType
        fields = ['room_type']
