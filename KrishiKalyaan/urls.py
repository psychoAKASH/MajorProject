from django.urls import path
from . import views


urlpatterns = [
    path('', views.index,name='home'),
    path('about/', views.about,name='about'),
    path('schemes/', views.schemes,name='schemes'),
    path('latestnews/', views.latestnews,name='latestnews'),
    path('organic_farming/', views.organic,name='organic'),
    path('contact/', views.contact,name='contact'),
    path('calculate/', views.index1, name="calculate"),
    path('predict/', views.predict, name="predict"),
    path('home/', views.feedback, name='feedback'),



]