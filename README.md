# django_menu_drawer

## Описание:
- Приложение реализует древовидное меню через template tag. 
- Вся информация о меню хранится в базе данных.
- Редактируется в стандартной админке Django.
- Выбранный на данный момент пункт определяется в url страницы.
- На отрисовку одного меню требуется один запрос к базе данных.
- На одной странице может быть несколько меню.


## Инструменты:
- Python 3.10
- Django

## Дополнительные инструменты:
- django-debug-toolbar - для проверки количества запросов к базе данных.
- slugify - используется в дополнительной коменде, написанной для быстрого заполнения базы данных

## Подготовка к запуску:
- Склонируйте репозиторий
- Установите все зависимости:
```bash
pip install -r requirements.txt
```
- Выполните миграции:
```bash
python manage.py makemigrations
python manage.py migrate
```
- Перейдите в menu_drawer/management/commands/load_menu.py и создайте свое меню в методе get_menu_dict. После чего запустите команду:
```bash
py manage.py load_menu --menu-title "Название_вашего_меню"
```
- Запустите проект:
```bash
py manage.py runserver
```
