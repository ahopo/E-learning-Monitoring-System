from django.contrib import admin
from django.urls import path,include 
from main import views
from django.conf.urls import url

admin.site.site_header = 'E-Learning Monitoring System'
admin.site.site_title = 'EMLS Portal'
admin.site.index_title = 'Welcome to E-Learning Monitoring System'
urlpatterns = [   
    path('admin/', admin.site.urls), 
    path('main/',include('main.urls')),
    path('',views.index, name='index')   
]
