from django.urls import path

from menu_drawer.views import HomeView

urlpatterns = [
    path('<str:template>/', HomeView.as_view(), name='home'),
]

