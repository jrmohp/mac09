from django.urls.conf import path

from . import views

urlpatterns =[
    path("checkin/",views.onsite_checkin_view,name='checkin_process'),
    path('submit_checkin/', views.submit_checkin, name='submit_checkin'),






]