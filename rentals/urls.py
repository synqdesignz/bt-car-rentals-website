from django.urls import path
from . import views  # Import views from the same app
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('homepage/', views.homepage_cars, name='homepage_cars'),
    path('fleet/', views.fleet, name='fleet'),
    path('fleet-api/', views.fleet_list, name='fleet-list'),
    path('menubookings/', views.menubookings, name='menubookings'),
    path('terms/', views.terms, name='terms'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('booking/<int:car_id>/', views.booking, name='booking'),
    path('get_booked_dates/<int:car_id>/', views.get_booked_dates, name="get_booked_dates"),
    path('confirm/', views.confirm, name='confirm'),
    path('search/', views.search_available_cars, name='search_available_cars'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
