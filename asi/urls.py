from django.urls.conf import path

from . import views

urlpatterns =[
    path("",views.index),
    path("payments/",views.paymentp),
    path("update/",views.updatep),
    path("login/",views.login),
    path("logout/",views.logout),
    path("viewinv/",views.viewenv),






]
