"""memoprojcet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from memoapp.views import index, post, modify, delete, signup, signin, signout, like

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', index, name='index'),
    path('write/', post, name='write'),
    path('modify/<int:memokey>', modify, name='modify'),
    path('delete/<int:memokey>', delete, name='delete'),
    path('join/', signup, name='join'),
    path('Login/', signin, name='signin'),
    path('Logout/', signout, name='signout'),
    path('like/', like, name='like'),
]