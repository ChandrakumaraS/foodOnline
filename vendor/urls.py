from django.urls import path, include
from . import views
from accounts import views as AccountViews



urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendor'),
    path('profile/', views.vprofile, name='vprofile'),
    path('menu_builder/', views.menu_builder, name='menu_builder'),
    path('menu_builder/category/<int:pk>/', views.fooditem_by_category, name='fooditem_by_category'),
    
    # category CRUD
    path('menu_builder/category/add/', views.add_category, name='add_category'),
    path('menu_builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('menu_builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),

    # fooditem CRUD
    path('menu_builder/food/add/', views.add_food, name='add_food'),
    path('menu_builder/food/edit/<int:pk>/', views.edit_food, name='edit_food'),
    path('menu_builder/foody/delete/<int:pk>/', views.delete_food, name='delete_food'),

    # Opening Hours
    path('opening_hour/', views.opening_hour, name='opening_hour'),
    path('opening_hour/add/', views.add_opening_hour, name='add_opening_hour'),
    path('opening_hour/remove/<int:pk>/', views.remove_opening_hour, name='remove_opening_hour'),

    path('order_detail/<int:order_number>/', views.order_detail, name='vendor_order_detail'),
    path('my_orders/', views.my_orders, name='vendor_my_orders'),
]