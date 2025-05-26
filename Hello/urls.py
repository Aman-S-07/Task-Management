
from django import views
from django.contrib import admin
from django.urls import path, include


admin.site.site_header = "Task"
admin.site.site_title = "Task Admin Portal" 
admin.site.index_title = "Management portal" 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('home.urls')),
    
   
  

]
