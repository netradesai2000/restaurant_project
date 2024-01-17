from django.contrib import admin
from restoapp.models import dish

# Register your models here.
class DishAdmin(admin.ModelAdmin):
        list_display=['id','name','price','dishdetails','cat','is_active']
        list_filter=['cat','price','is_active']
admin.site.register(dish,DishAdmin)