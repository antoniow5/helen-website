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
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import logout


urlpatterns = [
    path('admin/', admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),

    path('', views.index, name='index'),
    # path('index2', views.index2, name='index2'),

    # path('login-page', views.login_page, name='login_page'),
    # path('login-page/', views.login_page, name='login_page'),

    path('login-user', views.login_user, name="login_user"),
    path('login-user', views.login_user, name="login_user"),

    path('item/<int:item_id>', views.item, name='item'),
    path('item/<int:item_id>/', views.item),

    path('item/<int:item_id>/favorite', views.item_favorite, name='item_favorite'),
    path('item/<int:item_id>/favorite/', views.item_favorite),

    path('catalog', views.catalog, name='catalog'),
    path('catalog/', views.catalog),
    
    path('cart', views.cart, name='cart'),
    path('cart/', views.cart, name='cart'),

    path('user', views.user_container),
    path('user/', views.user_container),

    
    path('cart/add/<int:variant_id>', views.add_to_cart),
    path('cart/add/<int:variant_id>/', views.add_to_cart),

    path('logout', logout),

    # path('register-page', views.register_page, name="register_page"),
    # path('register-page/', views.register_page, name="register_page"),

    path('register-user', views.register_user, name="register_user"),
    path('register-user/', views.register_user, name="register_user"),


    path('user-data', views.user_data, name="user_data"),
    path('user-data/', views.user_data, name="user_data"),


    path('user-favorite', views.user_favorite, name="user_favorite"),
    path('user-favorite/', views.user_favorite, name="user_favorite"),


    path('user-orders', views.user_orders, name="user_orders"),
    path('user-orders/', views.user_orders, name="user_orders"),

    path('create-order', views.create_order, name="create_order"),
    path('create-order/', views.create_order, name="create_order"),




]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



# urlpatterns += i18n_patterns(
#     path("", index),
# )