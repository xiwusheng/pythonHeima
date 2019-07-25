from django.contrib import admin
from .models import TypeInfo, GoodsInfo

# Register your models here.


class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttitle']
    # list_per_page = 10
    # search_fields = ['title']
    # list_display_links = ['ttitle']


class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['id', 'gtitle', 'gunit', 'gclick', 'gprice', 'gpic', 'gkucun', 'gjianjie']
    # list_editable = ['gkucun']
    # readonly_fields = ['gclick']
    # search_fields = ['gtitle', 'gcontent', 'gjianjie']
    # list_display_links = ['gtitle']


admin.site.register(TypeInfo, TypeInfoAdmin)
admin.site.register(GoodsInfo, GoodsInfoAdmin)

