from django import forms

from menu_drawer.models import ParentalRelation


class ParentalRelationForm(forms.ModelForm):
    class Meta:
        model = ParentalRelation
        fields = ['menu', 'menu_item', 'parent']

    def clean_menu_item(self):
        menu = self.cleaned_data.get('menu')
        menu_item = self.cleaned_data.get('menu_item')
        if ParentalRelation.objects.filter(menu=menu, menu_item=menu_item):
            raise forms.ValidationError(f'Item с slug\'ом {menu_item.item_slug} уже присутствует в меню {menu}')
        return menu_item

