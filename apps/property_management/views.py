from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from django.utils.html import escape
from apps.property_management.models import AccommodationType, HotelRoom, PropertyAddress, PropertyCollection, PropertyFacility, PropertyImage, PropertyManagement, PropertyManagementHotelRoom, RoomImage, RoomType, property_management_image, property_temporary_image_upload_image_dir, room_temporary_image_upload_image_dir
from solo_core.helpers.signer import URLEncryptionDecryption
from solo_core.helpers.temporary_image_deletion import ImageDeletion
from django.contrib import messages
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import uuid
import os
from urllib.parse import urlparse
from apps.bannerimage.models import BannerImages
# Create your views here.

# Accommodation Type

class AccommodationTypeView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/property-management/accommodation-type/accommodation-type-list.html'
        self.context['title'] = 'Accommodation Type'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Accommodation Type", "route" : '','active' : True})
        

class LoadAccommodationTypeDatatable(BaseDatatableView):
    model = AccommodationType
    order_columns = ['id', 'name','description'] 
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return AccommodationType.objects.all().order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(name__istartswith=search)|Q(description__istartswith=search))
        return qs

    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'              : escape(item.id),
                'name'            : escape(item.name),
                'description'     : escape(item.description),
                # 'is_active'       : escape(item.is_contacted),
                'encrypt_id'      : escape(URLEncryptionDecryption.enc(item.id)),
            })
        return json_data
    

class AccommodationTypeCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.context = {"breadcrumbs": []}
        self.context['title'] = 'Accommodation Type'
        self.action = "Create"
        self.template = 'admin/home-page/property-management/accommodation-type/create-or-update-accommodation-list.html'

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))

        if id:
            self.action = "Update "
            self.context['accommodation_type_obj'] = get_object_or_404(AccommodationType, id=id)
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append(
            {"name": "Accommodation Type", "route": reverse('property_management:accommodation_type.index'), 'active': False})
        self.context['breadcrumbs'].append({"name": "{} Accommodation Type".format(self.action), "route": '', 'active': True})

    def post(self, request, *args, **kwargs):
        accommodation_type_id = request.POST.get('accommodation_type_id', None)
        try:
            if accommodation_type_id:
                self.action = 'Updated'
                accommodation_type_obj         = get_object_or_404(AccommodationType, id=accommodation_type_id)
            else:
                accommodation_type_obj         = AccommodationType()

            accommodation_type_obj.name        = request.POST.get('name')
            accommodation_type_obj.description = request.POST.get('description')
            accommodation_type_obj.save()

            messages.success(request, f"Data Successfully "+ self.action)

        except Exception as e:
            messages.error(request, f"Something went wrong."+str(e))
            if accommodation_type_id is not None:
                return redirect('property_management:accommodation_type.update', id=URLEncryptionDecryption.dec(int(accommodation_type_id)))
            return redirect('property_management:accommodation_type.create')
        return redirect('property_management:accommodation_type.index')


class DestroyAccommodationTypeRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            accommodation_type_id = request.POST.getlist('ids[]')
            if accommodation_type_id:
                AccommodationType.objects.filter(id__in=accommodation_type_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
            
        return JsonResponse(self.response_format, status=200)
    
# End Accommodation Type

# Property Collections

class PropertyCollectionView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/property-management/property-collection/property-collections-list.html'
        self.context['title'] = 'Property Collection'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Property Collection", "route" : '','active' : True})
        

class LoadPropertyCollectionDatatable(BaseDatatableView):
    model = PropertyCollection
    order_columns = ['id', 'name','description'] 
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return PropertyCollection.objects.all().order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(name__istartswith=search)|Q(description__istartswith=search))
        return qs

    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'              : escape(item.id),
                'name'            : escape(item.name),
                'description'     : escape(item.description),
                # 'is_active'       : escape(item.is_contacted),
                'encrypt_id'      : escape(URLEncryptionDecryption.enc(item.id)),
            })
        return json_data
    

class PropertyCollectionCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.context = {"breadcrumbs": []}
        self.context['title'] = 'Property Collection'
        self.action = "Create"
        self.template = 'admin/home-page/property-management/property-collection/create-or-update-property-collection.html'

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))

        if id:
            self.action = "Update "
            self.context['property_collection_obj'] = get_object_or_404(PropertyCollection, id=id)
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append(
            {"name": "Property Collection", "route": reverse('property_management:property_collection.index'), 'active': False})
        self.context['breadcrumbs'].append({"name": "{} Property Collection".format(self.action), "route": '', 'active': True})

    def post(self, request, *args, **kwargs):
        property_collection_id = request.POST.get('property_collection_id', None)
        try:
            if property_collection_id:
                self.action = 'Updated'
                property_collection_obj         = get_object_or_404(PropertyCollection, id=property_collection_id)
            else:
                property_collection_obj         = PropertyCollection()

            property_collection_obj.name        = request.POST.get('name')
            property_collection_obj.description = request.POST.get('description')
            property_collection_obj.save()

            messages.success(request, f"Data Successfully "+ self.action)

        except Exception as e:
            messages.error(request, f"Something went wrong."+str(e))
            if property_collection_id is not None:
                return redirect('property_management:property_collection.update', id=URLEncryptionDecryption.dec(int(property_collection_id)))
            return redirect('property_management:property_collection.create')
        return redirect('property_management:property_collection.index')
    

class DestroyPropertyCollectionRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            property_collection_id = request.POST.getlist('ids[]')
            if property_collection_id:
                PropertyCollection.objects.filter(id__in=property_collection_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
            
        return JsonResponse(self.response_format, status=200)
    
# End 

# Property Facility Start

class PropertyFacilityView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/property-management/property-facility/property-facility-list.html'
        self.context['title'] = 'Property Facility'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Property Facility", "route" : '','active' : True})
        
class LoadPropertyFacilityDatatable(BaseDatatableView):
    model = PropertyFacility
    order_columns = ['id', 'name', 'image', 'description'] 
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return PropertyFacility.objects.all().order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(name__istartswith=search)|Q(description__istartswith=search))
        return qs
    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'              : escape(item.id),
                'name'            : escape(item.name),
                'image'           : escape(item.image.url),
                'description'     : escape(item.description),
                'encrypt_id'      : escape(URLEncryptionDecryption.enc(item.id)),
            })
        return json_data

class PropertyFacilityCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.context = {"breadcrumbs": []}
        self.context['title'] = 'Property Facility'
        self.action = "Create"
        self.template = 'admin/home-page/property-management/property-facility/create-or-update-property-facility.html'

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))

        if id:
            self.action = "Update "
            self.context['property_facility_obj'] = get_object_or_404(PropertyFacility, id=id)
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append(
            {"name": "Property Facility", "route": reverse('property_management:property_facility.index'), 'active': False})
        self.context['breadcrumbs'].append({"name": "{} Property Facility".format(self.action), "route": '', 'active': True})

    def post(self, request, *args, **kwargs):
        property_facility_id = request.POST.get('property_facility_id', None)
        try:
            if property_facility_id:
                self.action = 'Updated'
                property_facility_obj         = get_object_or_404(PropertyFacility, id=property_facility_id)
            else:
                property_facility_obj         = PropertyFacility()

            property_facility_obj.name        = request.POST.get('name')
            property_facility_obj.description = request.POST.get('description')
            
            if request.FILES.__len__() != 0:
                if request.POST.get('property_image', None) is None:
                    property_facility_obj.image = request.FILES.get('property_image')
                    
            property_facility_obj.save()

            messages.success(request, f"Data Successfully "+ self.action)

        except Exception as e:
            messages.error(request, f"Something went wrong."+str(e))
            if property_facility_id is not None:
                return redirect('property_management:property_facility.update', id=URLEncryptionDecryption.dec(int(property_facility_id)))
            return redirect('property_management:property_facility.create')
        return redirect('property_management:property_facility.index')

class DestroyPropertyFacilityRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            property_facility_id = request.POST.getlist('ids[]')
            if property_facility_id:
                PropertyFacility.objects.filter(id__in=property_facility_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
            
        return JsonResponse(self.response_format, status=200)

# End


# Room Type

class RoomTypeView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/property-management/room-type/room-type-list.html'
        self.context['title'] = 'Room Type'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Room Type", "route" : '','active' : True})
        

class LoadRoomTypeDatatable(BaseDatatableView):
    model = RoomType
    order_columns = ['id', 'name', 'description'] 
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return RoomType.objects.all().order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(name__istartswith=search)|Q(description__istartswith=search))
        return qs

    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'              : escape(item.id),
                'name'            : escape(item.name),
                'description'     : escape(item.description),
                # 'is_active'       : escape(item.is_contacted),
                'encrypt_id'      : escape(URLEncryptionDecryption.enc(item.id)),
            })
        return json_data
    

class RoomTypeCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.context = {"breadcrumbs": []}
        self.context['title'] = 'Room Type'
        self.action = "Create"
        self.template = 'admin/home-page/property-management/room-type/create-or-update-room-type.html'

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))

        if id:
            self.action = "Update "
            self.context['room_type_obj'] = get_object_or_404(RoomType, id=id)
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append(
            {"name": "Room Type", "route": reverse('property_management:room_type.index'), 'active': False})
        self.context['breadcrumbs'].append({"name": "{} Room Type".format(self.action), "route": '', 'active': True})

    def post(self, request, *args, **kwargs):
        room_type_id = request.POST.get('room_type_id', None)
        try:
            if room_type_id:
                self.action = 'Updated'
                room_type_obj         = get_object_or_404(RoomType, id=room_type_id)
            else:
                room_type_obj         = RoomType()

            room_type_obj.name        = request.POST.get('name')
            room_type_obj.description = request.POST.get('description')
            room_type_obj.save()

            messages.success(request, f"Data Successfully "+ self.action)

        except Exception as e:
            messages.error(request, f"Something went wrong."+str(e))
            if room_type_id is not None:
                return redirect('property_management:room_type.update', id=URLEncryptionDecryption.dec(int(room_type_id)))
            return redirect('property_management:room_type.create')
        return redirect('property_management:room_type.index')


class DestroyRoomTypeRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            room_type_id = request.POST.getlist('ids[]')
            if room_type_id:
                RoomType.objects.filter(id__in=room_type_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
            
        return JsonResponse(self.response_format, status=200)
    
# End Accommodation Type

# Property Management start

class PropertyManagementView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/property-management/property_management/property-management-list.html'
        self.context['title'] = 'Property Management'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Property Management", "route" : '','active' : True})

class LoadPropertyManagementDatatable(BaseDatatableView):
    model = PropertyManagement
    order_columns = ['id', 'name', 'description', 'accomodation_type', 'total_price', 'no_of_rooms'] 
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return PropertyManagement.objects.all().order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(name__istartswith=search)|Q(description__istartswith=search))
        return qs

    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'                : escape(item.id),
                'name'              : escape(item.name),
                'description'       : escape(item.description),
                'accomodation_type' : escape(item.accomodation_type.name),
                'total_price'       : escape(item.total_price),
                'no_of_rooms'       : escape(item.no_of_rooms),
                # 'is_active'       : escape(item.is_contacted),
                'encrypt_id'        : escape(URLEncryptionDecryption.enc(item.id)),
            })
        return json_data
    
    
class PropertyManagementCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.context = {"breadcrumbs": []}
        self.context['title'] = 'Property Management'
        self.action = "Create"
        self.template = 'admin/home-page/property-management/property_management/create-or-update-property-management.html'

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        self.context['uuid'] = uuid.uuid4()
        self.context['accommodation_type_queryset']  = AccommodationType.objects.all()
        self.context['property_collection_queryset'] = PropertyCollection.objects.all()
        self.context['room_type_queryset']           = RoomType.objects.all()
        
        if id:
            self.action = "Update "
            self.context['property_management_obj'] = get_object_or_404(PropertyManagement, id=id)
            self.context['hotel_room_queryset']     = get_object_or_404(PropertyManagementHotelRoom, property_management_id=id)
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append(
            {"name": "Property Management", "route": reverse('property_management:property_management.index'), 'active': False})
        self.context['breadcrumbs'].append({"name": "{} Property Management".format(self.action), "route": '', 'active': True})

    def post(self, request, *args, **kwargs):
        property_management_id = request.POST.get('property_management_id', None)
        property_uuid = request.POST.get('property_uuid', None)
        
        try:
            if property_management_id:
                self.action = 'Updated'
                property_management_obj         = get_object_or_404(PropertyManagement, id=property_management_id)
                property_address_obj            = property_management_obj.address
            else:
                property_management_obj         = PropertyManagement()
                property_address_obj            = PropertyAddress()

            property_management_obj.name                   = request.POST.get('name', None)
            property_management_obj.description            = request.POST.get('description', None)
            property_management_obj.accomodation_type_id   = request.POST.get('accommodation_type', None)
            property_management_obj.total_price            = request.POST.get('total_price', None)
            property_management_obj.no_of_rooms            = request.POST.get('no_of_rooms', None)
            property_management_obj.alternative_phone      = request.POST.get('alternative_phone', None)
            property_management_obj.latitude               = request.POST.get('latitude', None)
            property_management_obj.longitude              = request.POST.get('longitude', None)
            property_management_obj.location               = request.POST.get('place', None)
            
            property_address_obj.street                 = request.POST.get('street', None)
            property_address_obj.city                   = request.POST.get('city', None)
            property_address_obj.city_area              = request.POST.get('city_area', None)
            property_address_obj.postal_code            = request.POST.get('postal_code', None)
            property_address_obj.phone                  = request.POST.get('phone', None)
            property_address_obj.alternative_phone      = request.POST.get('alternative_phone', None)
            property_address_obj.save()
            property_management_obj.address = property_address_obj
            
            property_collection_obj = request.POST.get('property_collection', None)
            # print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK", property_collection_obj)
            # for p_collection in property_collection_obj:
            #     p_collection_row = PropertyCollection.objects.filter(id=p_collection)
            #     if p_collection_row is not None:
            #         pass
            #     else:
            #         PropertyCollection.objects.filter(id=p_collection).delete()
            property_management_obj.save()
            
            PropertyImage.objects.filter(uuid=property_uuid).update(property_management=property_management_obj)
            messages.success(request, f"Data Successfully "+ self.action)

        except Exception as e:
            print("@22222222222???????????????????????>>>>>>>>>>>", e)
            messages.error(request, f"Something went wrong."+str(e))
            if property_management_id is not None:
                return redirect('property_management:property_management.update', id=URLEncryptionDecryption.dec(int(property_management_id)))
            return redirect('property_management:property_management.create')
        return redirect('property_management:property_management.index')
    
    
class PropertyImageUploadView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}
        
    def post(self, request, *args, **kwargs):
        try:
            instance_id = 0
            if request.FILES.__len__() != 0:
                image = request.FILES.get('file')
                uuid  = request.POST.get('uuid', None)
                property_image = PropertyImage()
                property_image.uuid = uuid
                path = default_storage.save(property_temporary_image_upload_image_dir(request), ContentFile(image.read()))
                property_image.property_image = path
                property_image.save()
                instance_id = property_image.id
                
            self.response_format['status_code'] = 200
            self.response_format['message'] = 'Success'
            self.response_format['data'] = instance_id
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)


# @method_decorator(login_required, name='dispatch')
class TemporaryImageDestroyView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            image_id = request.POST.get('id')
            action_type = request.POST.get('action_type')
            
            if image_id:
                if action_type == '1': # PropertyImages
                    image_del_obj = PropertyImage.objects.get(pk=image_id)
                    ImageDeletion(request, image_del_obj, action_type)
                elif action_type == '2':
                    image_del_obj = BannerImages.objects.get(pk=image_id)
                    ImageDeletion(request, image_del_obj, action_type)
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)

# @method_decorator(login_required, name='dispatch')
class GetPropertyManagementImages(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": "", "data" : []}

    def post(self, request, *args, **kwargs):
        try:
            property_id = request.POST.get('property_management_id')
            if property_id:
                property_images = PropertyImage.objects.filter(property_management_id=property_id)
                json_data = []
                for item in property_images:
                    json_data.append({
                        'id'         : escape(item.id), 
                        'image'      : escape(request.build_absolute_uri(item.property_image.url)), 
                        'image_name' : escape(os.path.basename(urlparse(request.build_absolute_uri(item.property_image)).path)), 
                        'size'       : escape(item.property_image.size), 
                    })
                    
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
                self.response_format['data'] = json_data
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
# End


# Room image management

class RoomImageUploadView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}
        
    def post(self, request, *args, **kwargs):
        try:
            
            instance_id = 0
            if request.FILES.__len__() != 0:
                image = request.FILES.get('file')
                uuid  = request.POST.get('uuid', None)
                room_image = RoomImage()
                room_image.uuid = uuid
                path = default_storage.save(room_temporary_image_upload_image_dir(request), ContentFile(image.read()))
                room_image.room_image = path
                room_image.save()
                instance_id = room_image.id
                
            self.response_format['status_code'] = 200
            self.response_format['message'] = 'Success'
            self.response_format['data'] = instance_id
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    

class GetPropertyRoomImages(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": "", "data" : []}

    def post(self, request, *args, **kwargs):
        try:
            property_id = request.POST.get('property_management_id')
            if property_id:
                room_images = RoomImage.objects.filter(property_management_id=property_id)
                json_data = []
                for item in room_images:
                    json_data.append({
                        'id'         : escape(item.id), 
                        'image'      : escape(request.build_absolute_uri(item.property_image.url)), 
                        'image_name' : escape(os.path.basename(urlparse(request.build_absolute_uri(item.property_image)).path)), 
                        'size'       : escape(item.property_image.size), 
                    })
                    
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
                self.response_format['data'] = json_data
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
            
        return JsonResponse(self.response_format, status=200)
    

class TemporaryRoomImageDestroyView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            image_id = request.POST.get('id')
            action_type = request.POST.get('action_type')
            
            if image_id:
                if action_type == '3': # PropertyImages
                    image_del_obj = PropertyImage.objects.get(pk=image_id)
                    ImageDeletion(request, image_del_obj, action_type)
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)