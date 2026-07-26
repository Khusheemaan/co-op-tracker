"""
URL configuration for coop_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tracker import views #pulls in the file we just edited, which was tracker -> views.py

urlpatterns = [
    path('admin/', admin.site.urls),
    path('applications/', views.application_list), #when someone visits /applications/, run the application_list view.
    path('applications/add/', views.add_application),
    path('applications/<int:pk>/', views.application_detail),
    #<int:pk> is a URL parameter. The URL parameter captures a number from the address and hands it to the view. (pk : primary key).
]

