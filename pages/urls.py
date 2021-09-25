from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'),name='home'),
    path('about-us', TemplateView.as_view(template_name='about-us.html'),name='about-us'),
    path('contact-us', TemplateView.as_view(template_name='contact-us.html'),name='contact-us'),
    # path('',TemplateView.as_view(template_name='home.html')),
]
