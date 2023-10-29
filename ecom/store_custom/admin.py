from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from tag.models import TaggedItem
from store.admin import ProductAdmin
from store.models import Product


class TagInline(GenericTabularInline):
   autocomplete_fields = ['tag']
   model = TaggedItem


class CustomProductAdmin(ProductAdmin):
   inlines = [TagInline]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)


