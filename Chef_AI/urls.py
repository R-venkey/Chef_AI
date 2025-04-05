"""
URL configuration for Chef_AI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path , include
from recipes.views import home, find_recipe, view_recipe, prepare_shopping_list, alternate_recipe, \
    stream_alternate_recipe

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home),
    path("find", find_recipe),
    path("recipe/<int:id>", view_recipe),
    path("shopping_list/<int:id>", prepare_shopping_list),
    path("recipes/alternate/<slug:alternate_type>/<int:id>", alternate_recipe),
    path("streaming/alternate/<slug:alternate_type>/<int:id>", stream_alternate_recipe),
]
