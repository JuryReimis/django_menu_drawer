from django.contrib import admin

from menu_drawer.models import ParentalRelation, Menu, MenuItem


class MenuItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'item_slug': ('item_title', )
    }


admin.site.register(ParentalRelation)
admin.site.register(Menu)
admin.site.register(MenuItem, MenuItemAdmin)
