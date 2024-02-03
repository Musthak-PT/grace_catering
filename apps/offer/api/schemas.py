from rest_framework import serializers
from apps.offer.models import PropertyOffer

class GetAllPropertyOfferSchemas(serializers.ModelSerializer):
    
    class Meta:
        model  = PropertyOffer
        fields = '__all__'
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas