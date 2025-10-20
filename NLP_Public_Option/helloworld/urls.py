from django.urls import path

import helloworld.views

urlpatterns = [
    path('index/',helloworld.views.index)

]