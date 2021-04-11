"""django1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin_page'),
    path('polls/', include('polls.urls'), name='polls'),
    path('', include('home_page.urls'), name='home'),
    path('simplesite1/', include('simplesite1_bstrap.urls')),
    path('blog/', include('blog.urls')),
    path('people/', include('people.urls')),
    path('orders/', include('myshop_orders.urls', namespace='orders')),
    path('cart/', include('myshop_cart.urls', namespace='cart')),   # порядок важен
    path('shop/', include('myshop.urls', namespace='shop')),
    # path('accounts/login/', views.LoginView.as_view(), name='login'),
]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/login/', views.LoginView.as_view(), name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL)   #media root
