from django.shortcuts import render
from django.views import generic


class HomeView(generic.View):
    template_name = 'menu_drawer/base.html'

    def get(self, request, *args, **kwargs):
        template = kwargs.get('template')
        if template == '1-menu':
            self.template_name = 'menu_drawer/1-menu.html'
        if template == '2-menu':
            self.template_name = 'menu_drawer/2-menu.html'
        if template == '3-menu':
            self.template_name = 'menu_drawer/3-menu.html'
        context = {

        }
        return render(request=request, template_name=self.template_name, context=context)

