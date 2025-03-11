from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from recipes.models import Recipe


# Create your views here.

def home(request):
    recipe_list = Recipe.objects.all()[:10]
    return render(request, 'index.html', {'recipes': recipe_list})
