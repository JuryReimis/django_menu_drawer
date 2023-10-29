from django.core.management import BaseCommand, CommandError
from slugify import slugify

from menu_drawer.models import Menu, MenuItem, ParentalRelation


class Command(BaseCommand):
    r"""Для корректного внесения данных структура словаря должна быть следующей:
    {
            'menu_title': 'Your menu name',
            'menu_items': [                         # Здесь самые верхние пункты меню - root_nodes
                {
                    'item_title': 'YourMenuItemName',
                    'item_slug': 'your_slug',        # Может отсутствовать. Тогда сгенерируется автоматически.
                    'children': [                   # Их дети. В Меню будут являться вложенными в верхние пункты.
                        {
                            'item_title': 'YourMenuItemName',
                            'item_slug': 'your_slug',
                            'children': []
                        },
                        {
                            'item_title': 'YourMenuItemName',
                            'children': []
                        },
                        {
                            'item_title': 'YourMenuItemName',
                            'children': []
                        },
                        # Далее по аналогии
                    ]
                },
                {
                    'item_title': 'YourMenuItemName',
                    'children': []
                },
            ]
        }"""
    help = r'Команда написана для быстрого добавления новых меню в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('--menu-title', type=str, help='Введите название всех меню, которые хотите загрузить в бд, через запятую')

    def handle(self, *args, **options):
        menu_names = options.get('menu_title')
        if not menu_names:
            raise CommandError('missing --menu-title')
        for name in menu_names.split(','):
            data = self.get_menu_dict(name)
            menu_title = data.get('menu_title')
            menu_items = data.get('menu_items')
            if menu_title:
                menu = Menu.objects.create(menu_title=menu_title)
            else:
                raise Exception('Не удалось обнаружить menu_name')

            self.iterate_children(children=menu_items, menu=menu, parent=None)

    def iterate_children(self, children: list, menu: str, parent: MenuItem = None):
        if children:
            for child in children:
                item_title = child.get('item_title')
                item_slug = child.get('item_slug')
                if not item_slug:
                    item_slug = slugify(item_title)
                menu_item = MenuItem.objects.get_or_create(item_title=item_title, item_slug=item_slug)[0]
                try:
                    ParentalRelation.objects.create(menu=menu, menu_item=menu_item, parent=parent)
                except Exception as error:
                    print(error)
                else:
                    self.iterate_children(child.get('children'), menu=menu, parent=menu_item)

    @staticmethod
    def get_menu_dict(menu_name: str):
        menu = {
            'Products': {
                'menu_title': 'Products',
                'menu_items': [  # Здесь самые верхние пункты меню - root_nodes
                    {
                        'item_title': 'Продукты нефтепереработки',
                        'children': [  # Их дети. В Меню будут являться вложенными в верхние пункты.
                            {
                                'item_title': 'Заводской газ',
                                'children': [
                                    {
                                        'item_title': 'Легкие дистилляты',
                                        'children': [
                                            {
                                                'item_title': 'Бензин',
                                                'children': [
                                                    {
                                                        'item_title': 'Средний бензин',
                                                        'children': [
                                                            {
                                                                'item_title': 'Автомобильный бензин',
                                                                'children': []
                                                            },
                                                            {
                                                                'item_title': 'Авиационный бензин',
                                                                'children': []
                                                            },
                                                            {
                                                                'item_title': 'Взрывчатые вещества',
                                                                'children': []
                                                            },
                                                            {
                                                                'item_title': 'Смешанные лигроины',
                                                                'children': []
                                                            },
                                                            {
                                                                'item_title': 'Сырье для производства синтетических химических продуктов',
                                                                'children': []
                                                            },
                                                            {
                                                                'item_title': 'Растворители',
                                                                'children': []
                                                            },
                                                        ]
                                                    },
                                                    {
                                                        'item_title': 'Тяжелый бензин',
                                                        'children': [
                                                            {
                                                                'item_title': 'Ряд основных продуктов переработки сырой нефти',
                                                                'children': []
                                                            },
                                                            {
                                                                'item_title': 'Находит свое применение',
                                                                'children': []
                                                            },
                                                        ]
                                                    },
                                                ]
                                            },
                                            {
                                                'item_title': 'Керосин',
                                                'children': [
                                                    {
                                                        'item_title': 'Находит свое применение',
                                                        'item_slug': 'primenenie-kerosina',
                                                        'children': []
                                                    },
                                                ]
                                            },
                                        ]
                                    },
                                    {
                                        'item_title': 'Средние дистилляты',
                                        'children': [
                                            {
                                                'item_title': 'Газойль',
                                                'children': [
                                                    {
                                                        'item_title': 'Применение',
                                                        'item_slug': 'primenenie-gasoily',
                                                        'children': []
                                                    },
                                                ]
                                            },
                                            {
                                                'item_title': 'Поглотительные масла',
                                                'children': [
                                                    {
                                                        'item_title': 'Применение',
                                                        'item_slug': 'primenenie-poglotitelnih-masel',
                                                        'children': []
                                                    },
                                                ]
                                            },
                                            {
                                                'item_title': 'Светлые масла',
                                                'children': [
                                                    {
                                                        'item_title': 'Технические масла',
                                                        'children': []
                                                    },
                                                    {
                                                        'item_title': 'Медицинские масла',
                                                        'children': []
                                                    },
                                                ]
                                            },
                                            {
                                                'item_title': 'Насыщенные масла',
                                                'children': [
                                                    {
                                                        'item_title': 'Применение',
                                                        'item_slug': 'primenenie-nasishennih-masel',
                                                        'children': []
                                                    },
                                                ]
                                            },
                                        ]
                                    },
                                    {
                                        'item_title': 'Тяжелые дистилляты',
                                        'children': [
                                            {
                                                'item_title': 'Жирные кислоты',
                                                'children': []
                                            },
                                            {
                                                'item_title': 'Жирные спирты и сульфаты',
                                                'children': []
                                            },
                                            {
                                                'item_title': 'Смазочные масла',
                                                'children': []
                                            },
                                            {
                                                'item_title': 'Вазелин',
                                                'children': []
                                            },
                                        ]
                                    },
                                ]
                            },
                        ]
                    },
                    {
                        'item_title': 'Пищевые продукты',
                        'children': [
                            {
                                'item_title': 'Растительного происхождения',
                                'children': [
                                    {
                                        'item_title': 'Животные корма',
                                        'children': [
                                            {
                                                'item_title': 'Сено',
                                                'children': []
                                            },
                                            {
                                                'item_title': 'Силос',
                                                'children': []
                                            },
                                        ]
                                    },
                                    {
                                        'item_title': 'Продукты',
                                        'item_slug': 'rastitelnoe-dlya-cheloveka',
                                        'children': [
                                            {
                                                'item_title': 'Бобы',
                                                'children': [
                                                    {
                                                        'item_title': 'Горох',
                                                        'children': []
                                                    },
                                                    {
                                                        'item_title': 'Фасоль',
                                                        'children': []
                                                    },
                                                    {
                                                        'item_title': 'Нут',
                                                        'children': []
                                                    },
                                                ]
                                            },
                                            {
                                                'item_title': 'Фрукты',
                                                'children': [
                                                    {
                                                        'item_title': 'Яблоки',
                                                        'children': []
                                                    },
                                                    {
                                                        'item_title': 'Бананы',
                                                        'children': []
                                                    },
                                                    {
                                                        'item_title': 'Апельсины',
                                                        'children': []
                                                    },
                                                    {
                                                        'item_title': 'Фиги',
                                                        'children': []
                                                    },
                                                ]
                                            },
                                            {
                                                'item_title': 'Овощи',
                                                'children': [
                                                    {
                                                        'item_title': 'Картофель',
                                                        'children': []
                                                    },
                                                    {
                                                        'item_title': 'Томаты',
                                                        'children': []
                                                    },
                                                    {
                                                        'item_title': 'Лук',
                                                        'children': []
                                                    },
                                                    {
                                                        'item_title': 'Морковь',
                                                        'children': []
                                                    },
                                                ]
                                            },
                                        ]
                                    },
                                ]
                            },
                            {
                                'item_title': 'Животного происхождения',
                                'children': [
                                    {
                                        'item_title': 'Мясо',
                                        'children': [
                                            {
                                                'item_title': 'Говядина',
                                                'children': []
                                            },
                                            {
                                                'item_title': 'Свинина',
                                                'children': []
                                            },
                                            {
                                                'item_title': 'Баранина',
                                                'children': []
                                            },
                                            {
                                                'item_title': 'Конина',
                                                'children': []
                                            },
                                        ]
                                    },
                                    {
                                        'item_title': 'Птица',
                                        'children': [
                                            {
                                                'item_title': 'Курица',
                                                'children': []
                                            },
                                            {
                                                'item_title': 'Утка',
                                                'children': []
                                            },
                                            {
                                                'item_title': 'Перепел',
                                                'children': []
                                            },
                                            {
                                                'item_title': 'Индейка',
                                                'children': []
                                            },
                                        ]
                                    },
                                    {
                                        'item_title': 'Рыба',
                                        'children': [
                                            {
                                                'item_title': 'Красная рыба',
                                                'children': [
                                                    {
                                                        'item_title': 'Севрюга',
                                                        'children': []
                                                    },
                                                    {
                                                        'item_title': 'Белуга',
                                                        'children': []
                                                    },
                                                    {
                                                        'item_title': 'Осетр',
                                                        'children': []
                                                    },
                                                ]
                                            },
                                            {
                                                'item_title': 'Белая',
                                                'children': [
                                                    {
                                                        'item_title': 'Треска',
                                                        'children': []
                                                    },
                                                    {
                                                        'item_title': 'Минтай',
                                                        'children': []
                                                    },
                                                    {
                                                        'item_title': 'Сельдь',
                                                        'children': []
                                                    },
                                                ]
                                            },
                                        ]
                                    },
                                    {
                                        'item_title': 'Молочное',
                                        'children': [
                                            {
                                                'item_title': 'Молоко',
                                                'children': []
                                            },
                                            {
                                                'item_title': 'Сыр',
                                                'children': []
                                            },
                                            {
                                                'item_title': 'Творог',
                                                'children': []
                                            },
                                            {
                                                'item_title': 'Сметана',
                                                'children': []
                                            },
                                        ]
                                    },
                                ]
                            },
                            {
                                'item_title': 'Синтетические',
                                'children': [
                                    {
                                        'item_title': 'Химия',
                                        'children': []
                                    },
                                ]
                            },
                        ]
                    },
                    {
                        'item_title': 'Электроника',
                        'children': [
                            {
                                'item_title': 'Микропроцессоры',
                                'children': [
                                    {
                                        'item_title': 'АМД',
                                        'children': [
                                            {
                                                'item_title': 'Ryzen',
                                                'children': [
                                                    {
                                                        'item_title': '2700',
                                                        'children': []
                                                    },
                                                    {
                                                        'item_title': '1700',
                                                        'children': []
                                                    },
                                                ]
                                            },
                                            {
                                                'item_title': 'Athlon',
                                                'children': []
                                            },
                                        ]
                                    },
                                    {
                                        'item_title': 'Интел',
                                        'children': [
                                            {
                                                'item_title': 'i3',
                                                'children': [
                                                    {
                                                        'item_title': 'i3-7700',
                                                        'children': []
                                                    },
                                                    {
                                                        'item_title': 'i3-12321465',
                                                        'children': []
                                                    },
                                                ]
                                            },
                                            {
                                                'item_title': 'i5',
                                                'children': [
                                                    {
                                                        'item_title': 'i5-8800',
                                                        'children': []
                                                    },
                                                    {
                                                        'item_title': 'i5-5461',
                                                        'children': []
                                                    },
                                                ]
                                            },
                                            {
                                                'item_title': 'i7',
                                                'children': [
                                                    {
                                                        'item_title': 'i7-3770',
                                                        'children': []
                                                    },
                                                    {
                                                        'item_title': 'i7-89752',
                                                        'children': []
                                                    },
                                                ]
                                            },
                                        ]
                                    },
                                ]
                            },
                            {
                                'item_title': 'Компьютерная периферия',
                                'children': [
                                    {
                                        'item_title': 'Звук',
                                        'children': [
                                            {
                                                'item_title': 'Наушники',
                                                'children': []
                                            },
                                            {
                                                'item_title': 'Колонки',
                                                'children': []
                                            },
                                        ]
                                    },
                                    {
                                        'item_title': 'Управление',
                                        'children': [
                                            {
                                                'item_title': 'Мышь',
                                                'children': []
                                            },
                                            {
                                                'item_title': 'Клавиатура',
                                                'children': []
                                            },
                                            {
                                                'item_title': 'Контроллеры',
                                                'children': []
                                            },
                                        ]
                                    },
                                    {
                                        'item_title': 'Аксессуары',
                                        'children': []
                                    },
                                ]
                            },
                        ]
                    },
                ]
            },
            'Institutes': {
                'menu_title': 'Institutes',
                'menu_items': [
                    {
                        'item_title': 'Россия',
                        'children': [  # Их дети. В Меню будут являться вложенными в верхние пункты.
                            {
                                'item_title': 'МГУ',
                                'item_slug': 'your_slug',
                                'children': []
                            },
                            {
                                'item_title': 'МГТУ',
                                'children': []
                            },
                            {
                                'item_title': 'РГСУ',
                                'children': []
                            },
                            # Далее по аналогии
                        ]
                    },
                    {
                        'item_title': 'Англия',
                        'children': [
                            {
                                'item_title': 'Кембридж',
                                'children': []
                            },
                            {
                                'item_title': 'Оксфорд',
                                'children': []
                            },
                            {
                                'item_title': 'Имперский колледж',
                                'children': []
                            },
                            {
                                'item_title': 'Манчестер',
                                'children': []
                            },
                        ]
                    },
                    {
                        'item_title': 'США',
                        'children': [
                            {
                                'item_title': 'Гарвард',
                                'children': []
                            },
                            {
                                'item_title': 'Стенфорд',
                                'children': []
                            },
                            {
                                'item_title': 'Колумбийский',
                                'children': [
                                    {
                                        'item_title': 'Колонки',
                                        'children': []
                                    },
                                ]
                            },
                        ]
                    },
                ]
            }
        }
        return menu.get(menu_name)
