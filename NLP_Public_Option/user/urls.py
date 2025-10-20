from django.urls import path


import user.views

urlpatterns = [
    path('index/',user.views.index),

    path('jinja3_test/',user.views.Jinja3test),

    path('login/',user.views.login),

    path('register/',user.views.register),

    path('logout/',user.views.logout),


]