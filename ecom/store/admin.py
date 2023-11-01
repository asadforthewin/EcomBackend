from typing import Any
from django.contrib import admin,messages
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Count
from django.db.models import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse

from tag.models import TaggedItem
from . import models


# INVENTORY FILTER USED IN PRODUCT CLASS
class InventoryFilter(admin.SimpleListFilter):
   title = 'price'
   parameter_name = 'unit_price'

   def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
      return  [
         ('a', 'Less than 40$'),
         ('b', 'greater than 40$')
      ]
   
   def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
       if self.value == 'a':
        return queryset.filter(price__lt=40)
       elif self.value == 'b':
          return queryset.filter(price__gt=40)
   

   
 
# PRODUCT CLASS
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
   autocomplete_fields = ['collection']
   actions = ['clear_inventory'] #action in the product model list page
   list_display= ['title' , 'unit_price', 'inventory_status','collection_title'] #lists to be displayed
#    on product list page
   list_editable = ['unit_price'] #unit price is editable on list page 
   list_per_page = 10 #pagination
   list_filter = ['collection', 'last_update', InventoryFilter] #Filters on the right side 

   prepopulated_fields = {
      'slug':['title'] #only populated if we dont touch the slug field, Js used here
   }
   search_fields = ['title__istartswith'] #search bar field that is case insensitive 
#    and only search the initials

   def collection_title(self, product):
      return product.collection.title
 

   @admin.display(ordering='inventory')
   def inventory_status(self, product):
      if (product.inventory)<20:
         return "Low"
      else:
         return "ok"
      
   @admin.action(description="clear Inventory")
   def clear_inventory(self,request, queryset):
      updated_count = queryset.update(inventory=0)
      self.message_user(
         request,
         f"{updated_count} products were successfully updated",
         messages.ERROR
      )
    



      
# COllECTION CLASS
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
   list_display= ['title', 'product_count']
   list_per_page = 10
   search_fields = ['title']
  
   @admin.display(ordering = 'product_count') 
   def product_count(self,collection):
    url = (reverse('admin:store_product_changelist') + '?' + urlencode({
       "collection__id" : str(collection.id)  
    }))
    return format_html('<a href="{}">{}</a>', url, collection.product_count)
     
   
   def get_queryset(self, request):
    return super().get_queryset(request). annotate(product_count = Count('product'))
      




@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
   list_display= ['first_name' , 'last_name', 'membership','orders']
   list_editable = ['membership']
   list_per_page = 10
   search_fields = ['customer']

   @admin.display(ordering= 'orders')
   def orders(self,customer):
        url = reverse('admin:store_order_changelist') + '?' + urlencode({"customer__id":customer.id})
         
        return format_html('<a href="{}">{}</a>', url, customer.orders)
   
   def get_queryset(self, request):
      return super().get_queryset(request) . annotate(orders=Count('order') )   

   

class OrderItemInline(admin.TabularInline):
   model = models.OrderItem
   autocomplete_fields= ['product']
   extra=0
   min_num = 1

   
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
   autocomplete_fields=['customer']
   inlines = [OrderItemInline]
   list_display=['id','placed_at','customer']
   

   
