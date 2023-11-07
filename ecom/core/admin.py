from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdminUser
from django.contrib.contenttypes.admin import GenericTabularInline
from tag.models import TaggedItem
from store.admin import ProductAdmin
from store.models import Product
from .models import User




@admin.register(User)
class UserAdmin(BaseAdminUser):
   #  autocomplete_fields = ['']
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2","email", "first_name", "last_name"),
            },
        ),
    )


class TagInline(GenericTabularInline):
   autocomplete_fields = ['tag']
   model = TaggedItem


class CustomProductAdmin(ProductAdmin):
   inlines = [TagInline]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)


