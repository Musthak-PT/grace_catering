from django.db import models
from apps.authentication.models import AbstractDateFieldMix
from django.utils.text import slugify
from random import randint

# Create your models here.
class PropertyOffer(AbstractDateFieldMix):
    slug                = models.SlugField(max_length=256, unique=True, editable=False, blank = True, null = True)
    start_date          = models.DateField(null=True, blank=True)
    end_date            = models.DateField(null=True, blank=True)
    offer_percentage    = models.CharField(max_length=256, null=True, blank=True)
 
    class Meta:
        verbose_name = "PropertyOffer" 
        verbose_name_plural = "PropertyOffer"
        
    def save(self, *args, **kwargs):
        if not self.slug or self.offer_percentage:
            self.slug = slugify(str(self.offer_percentage))
            if PropertyOffer.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.offer_percentage)) + '-' + str(randint(1, 9999999))
        super(PropertyOffer, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.offer_percentage