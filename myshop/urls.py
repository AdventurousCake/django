from django.urls import path
from . import views
app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    # параметр ":category_slug" передается в функцию product_list
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

]