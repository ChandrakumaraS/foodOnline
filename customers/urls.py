from django.urls import path, include
from accounts import views as AccountViews
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path('', AccountViews.custDashboard, name='customer'),
     path('profile/', views.cprofile, name='cprofile'),
     path('my_orders/', views.my_orders, name='customer_my_orders'),
     path('order_detail/<int:order_number>', views.order_detail, name='order_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)