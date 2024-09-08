from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Home page
    path('generate/', views.generate, name='generate'),  # Form submission
    path('generator/', views.generator_view, name='generator'),  # Generator page
    path('about/', views.about, name='about'),
    path('businesses/', views.business_list, name='business_list'),
    path('priv_terms', views.priv_terms, name='priv_terms')
]
