from rest_framework import serializers
from apps.property_management.models import *

class GetAccommodationTypeUsWebResponseSchemas(serializers.ModelSerializer):
    
    class Meta:
        model  = AccommodationType
        fields = ['id', 'slug', 'name', 'description']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas

class GetPropertyCollectionWebResponseSchemas(serializers.ModelSerializer):
    
    class Meta:
        model  = PropertyCollection
        fields = ['id', 'slug', 'name', 'description']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas

class GetPropertyFacilityWebResponseSchemas(serializers.ModelSerializer):
    
    class Meta:
        model  = PropertyFacility
        fields = ['id', 'slug', 'name', 'description','image']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas
    
#get all filtered properties
class FilterPropertyImageListSchema(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id','property_image']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data:
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data

class FilterPropertyAddressListSchema(serializers.ModelSerializer):
    class Meta:
        model = PropertyAddress
        fields = ['id','street','city']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data:
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data

class FilterPropertyFacilityListSchema(serializers.ModelSerializer):
    class Meta:
        model = PropertyFacility
        fields = ['name']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data:
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data

class FilterPropertyManagementSchema(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image')
    address = serializers.SerializerMethodField('get_address')
    facility = serializers.SerializerMethodField('get_facility')

    class Meta:
        model = PropertyManagement
        fields = ['id', 'image', 'name', 'address', 'total_price', 'facility']

    def get_image(self, instance):
        image_obj = PropertyImage.objects.filter(property_management_id=instance.id)
        image_schema = FilterPropertyImageListSchema(image_obj, many=True)
        return image_schema.data

    def get_address(self, instance):
        address_obj = instance.address
        if address_obj:
            address_schema = FilterPropertyAddressListSchema(address_obj)
            return address_schema.data
        else:
            return None

    def get_facility(self, instance):
        # Step 1: Collect hotel_room IDs
        hotel_room_ids = PropertyManagementHotelRoom.objects.filter(
            property_management=instance
        ).values_list('hotel_room', flat=True)

        # Step 2: Get related PropertyFacility instances
        property_facility_instances = HotelRoomPropertyFacility.objects.filter(
            hotel_room__in=hotel_room_ids
        ).values_list('property_facility', flat=True)

        # Step 3: Get unique 'name' field values
        facility_names = PropertyFacility.objects.filter(
            id__in=property_facility_instances
        ).values_list('name', flat=True).distinct()

        return facility_names
#End

