"""
URL configuration for helen project.

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
from django.urls import path, include
from app.views import index, item, cart, catalog, login, index2, authentication
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),

    path('', index),
    path('index2', index2, name='index2'),

    path('login', login, name='login'),
    path('login/', login, name='login'),

    path('auth', authentication, name="authentication"),
    path('auth', authentication, name="authentication"),


    path('item', item),
    path('item/', item),

    path('catalog', catalog),
    path('catalog/', catalog),
    
    path('cart', catalog),
    path('cart/', catalog),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



urlpatterns += i18n_patterns(
    path("", index),
)