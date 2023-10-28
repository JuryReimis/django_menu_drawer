from django.contrib import admin

from menu_drawer.forms import ParentalRelationForm
from menu_drawer.models import ParentalRelation, Menu, MenuItem


class MenuItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'item_slug': ('item_title', )
    }


class ParentalRelationAdmin(admin.ModelAdmin):
    form = ParentalRelationForm


admin.site.register(ParentalRelation, ParentalRelationAdmin)
admin.site.register(Menu)
admin.site.register(MenuItem, MenuItemAdmin)
