"""
URL configuration for NLP_Public_Option project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.views.generic import RedirectView


urlpatterns = [
    path("admin/", admin.site.urls),

    # 测试模块
    path('hello/', include('helloworld.urls')),

    # 将根url重定向到/user/login
    path('', RedirectView.as_view(url='/user/login/', permanent=False)),

    # 用户模块
    path('user/',include('user.urls')),

    # 页面模块
    path('page/',include('page.urls'))

]


