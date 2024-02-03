from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from django.utils.html import escape
from apps.bannerimage.models import BannerImages
from solo_core.helpers.signer import URLEncryptionDecryption
from django.contrib import messages
from django.http import JsonResponse
import uuid
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
# Create your views here.

# start About us
# class BannerImageView(View):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.context = {"breadcrumbs" : []}
#         self.template = 'admin/home-page/banner-image/banner-image-list.html'
#         self.context['title'] = 'Banner Image'
#         self.generateBreadcrumbs()
        
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template, context=self.context)

#     def generateBreadcrumbs(self):
#         self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
#         self.context['breadcrumbs'].append({"name" : "Banner Image", "route" : '','active' : True})
        

# class LoadBannerImageDatatable(BaseDatatableView):
#     model = BannerImages
#     order_columns = ['id']
    
#     def get_initial_queryset(self):
#         filter_value = self.request.POST.get('columns[3][search][value]', None)
#         if filter_value == '1':
#             return self.model.objects.filter(is_active=True).order_by('-id')
#         elif filter_value == '2':
#             return self.model.objects.filter(is_active=False).order_by('-id')
#         else:
#             return BannerImages.objects.all().order_by('-id')
    
#     def filter_queryset(self, qs):
#         search = self.request.POST.get('search[value]', None)
#         if search:
#             qs = qs.filter(Q(title__istartswith=search)|Q(description__istartswith=search))
#         return qs

    
#     def prepare_results(self, qs):
#         json_data = []
#         for item in qs:
#             json_data.append({
#                 'id'              : escape(item.id),
#                 'image'           : escape(item.image.url),
#                 'is_active'       : escape(item.is_active),
#                 'encrypt_id'      : escape(URLEncryptionDecryption.enc(item.id)),
#             })
#         return json_data
    

# class BannerImageCreateOrUpdateView(View):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)

#         self.context = {"breadcrumbs": []}
#         self.context['title'] = 'Banner Image'
#         self.action = "Create"
#         self.template = 'admin/home-page/banner-image/create-or-update-banner-image.html'

#     def get(self, request, *args, **kwargs):
#         id = URLEncryptionDecryption.dec(kwargs.pop('id', None))

#         if id:
#             self.action = "Update "
#             self.context['banner_image_obj'] = get_object_or_404(BannerImages, id=id)
#             self.context['uuid'] = uuid.uuid4()
#         self.generateBreadcrumbs()
#         return render(request, self.template, context=self.context)

#     def generateBreadcrumbs(self):
#         self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
#         self.context['breadcrumbs'].append(
#             {"name": "Banner Image", "route": reverse('about_us:about_us.index'), 'active': False})
#         self.context['breadcrumbs'].append({"name": "{} Banner Image".format(self.action), "route": '', 'active': True})

#     def post(self, request, *args, **kwargs):
#         banner_image_id = request.POST.get('banner_image_id', None)
#         try:
#             if banner_image_id:
#                 self.action = 'Updated'
#                 banner_image_obj         = get_object_or_404(BannerImages, id=banner_image_id)
#             else:
#                 banner_image_obj         = BannerImages()

#             banner_image_obj.image       = request.POST.get('title')
#             banner_image_obj.description = request.POST.get('description')
#             banner_image_obj.save()
            
#             messages.success(request, f"Data Successfully "+ self.action)
            
#         except Exception as e:
#             messages.error(request, f"Something went wrong."+str(e))
#             if banner_image_id is not None:
#                 return redirect('banner_image:banner_image.update', id=URLEncryptionDecryption.dec(int(banner_image_id)))
#             return redirect('banner_image:banner_image.create')
#         return redirect('banner_image:banner_image.index')


# class DestroyAboutUsRecordsView(View):
#     def __init__(self, **kwargs):
#         self.response_format = {"status_code": 101, "message": "", "error": ""}

#     def post(self, request, *args, **kwargs):
#         try:
#             about_us_id = request.POST.getlist('ids[]')
#             if about_us_id:
#                 BannerImages.objects.filter(id__in=about_us_id).delete()
#                 self.response_format['status_code'] = 200
#                 self.response_format['message'] = 'Success'
#         except Exception as e:
#             self.response_format['message'] = 'error'
#             self.response_format['error'] = str(e)
            
#         return JsonResponse(self.response_format, status=200)
    
    
# class AboutUsStatusChange(View):
#     def __init__(self, **kwargs):
#         self.response_format = {"status_code":101, "message":"", "error":""}
        
#     def post(self, request, **kwargs):
#         try:
#             instance_id = request.POST.get('id', None)
#             instance    = BannerImages.objects.get(id = instance_id)
#             if instance_id:
#                 if instance.is_active:
#                     instance.is_active = False
#                 else:
#                     instance.is_active =True
#                 instance.save()
#                 self.response_format['status_code']=200
#                 self.response_format['message']= 'Success'
                
#         except Exception as es:
#             self.response_format['message']='error'
#             self.response_format['error'] = str(es)
#         return JsonResponse(self.response_format, status=200)
    
    
# class BannerImageUploadView(View):
#     def __init__(self, **kwargs):
#         self.response_format = {"status_code": 101, "message": "", "error": ""}
        
#     def post(self, request, *args, **kwargs):
#         try:
#             instance_id = 0
#             if request.FILES.__len__() != 0:
#                 image = request.FILES.get('file')
#                 uuid  = request.POST.get('uuid', None)
#                 banner_image = BannerImages()
#                 banner_image.uuid = uuid
#                 path = default_storage.save(banner_temporary_image_upload_image_dir(request), ContentFile(image.read()))
#                 banner_image.image = path
#                 banner_image.save()
#                 instance_id = banner_image.id
                
#             self.response_format['status_code'] = 200
#             self.response_format['message'] = 'Success'
#             self.response_format['data'] = instance_id
#         except Exception as e:
#             self.response_format['message'] = 'error'
#             self.response_format['error'] = str(e)
#         return JsonResponse(self.response_format, status=200)
# End About us