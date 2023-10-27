from django.urls import path

from menu_drawer.views import HomeView

urlpatterns = [
    path('<str:template>/<slug:slug>/', HomeView.as_view(), name='home'),
    # path('1-menu/<slug:slug>/', )
]

