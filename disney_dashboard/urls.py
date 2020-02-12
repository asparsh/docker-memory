"""disney_dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from disney_imputed_component.views import getDashBoardData, getTimeSeriesGraph
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', getDashBoardData, name='home'),
    path('admin/', admin.site.urls),
    path('ajax/getdevice_node/', getTimeSeriesGraph, name='get_graph'),
    path('ajax/get_device/', getTimeSeriesGraph, name='get_graph'),
    # path(r'^mytimeseries/$', new_image, name='new_image'),
]+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
