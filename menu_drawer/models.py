from django.db import models
from django.utils.text import slugify


class Menu(models.Model):
    menu_title = models.CharField(
        max_length=100,
    )

    def __str__(self):
        return self.menu_title


class MenuItem(models.Model):
    def get_slug(self):
        return slugify(self.item_title)

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

    def __str__(self):
        return f"{self.menu_item} - наследник {self.parent}"
