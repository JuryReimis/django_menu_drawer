from django.core.exceptions import ValidationError
from django.db import models


class Menu(models.Model):
    menu_title = models.CharField(
        max_length=100,
    )

    def __str__(self):
        return self.menu_title


class MenuItem(models.Model):
    item_title = models.CharField(
        max_length=100,
    )

    item_slug = models.SlugField(
        db_index=True,
        unique=True,
        verbose_name="URL"
    )

    def __str__(self):
        return self.item_title


class ParentalRelation(models.Model):
    menu = models.ForeignKey(to='Menu', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(to='MenuItem', on_delete=models.CASCADE, related_name='parent_menu')
    parent = models.ForeignKey(to='MenuItem', null=True, blank=True, default=None, on_delete=models.CASCADE, related_name='child_relations')

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if ParentalRelation.objects.filter(menu=self.menu, menu_item=self.menu_item):
            raise ValidationError(f'Item со slug\'ом {self.menu_item.item_slug} уже присутствует в меню {self.menu}')
        super(ParentalRelation, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"{self.menu_item} - наследник {self.parent}"
