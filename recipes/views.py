import random

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.shortcuts import render
import re
from recipes.models import Recipe
from recipes.ai import get_shopping_list, alternative_recipe


# Create your views here.

def home(request):
    recipe_list = list(Recipe.objects.all())
    random.shuffle(recipe_list)
    return render(request, 'index.html', {'recipes': recipe_list[:10]})



def keyword_count(keyword, recipe):
    t=''
    t+=recipe.get('ingredients')
    t+=recipe.get('instructions')
    t+=recipe.get('image_name')
    t+=recipe.get('cleaned_ingredients')

    t=t.lower()
    l=re.findall(keyword, t)
    n=len(l)

    title=recipe.get('title').lower()
    l=re.findall(keyword, title)
    print(l, keyword)
    n+=len(l)*20

    return n


# Method to find recipes with keyword in title, ingredients, instructions, or cleaned_ingredients
def find_recipe(request):
    keyword = request.GET.get('keyword')
    recipe_list = []

    if keyword:
        recipe_list = Recipe.objects.filter(
            Q(title__icontains=keyword) |
            Q(ingredients__icontains=keyword) |
            Q(instructions__icontains=keyword) |
            Q(cleaned_ingredients__icontains=keyword)
        )

    recipes = [{
            'id': recipe.id,
            'title': recipe.title,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
            'image_name': recipe.image_name,
            'cleaned_ingredients': recipe.cleaned_ingredients,
            'count': keyword_count(keyword, recipe),
        } for recipe in recipe_list]

    recipes.sort(key=lambda x:keyword_count(keyword, x), reverse=True)

    context = {
        'recipes': recipes,
        'keyword': keyword
    }
    return JsonResponse(context)

def view_recipe(request, id):
    recipe = Recipe.objects.get(id=id)
    return render(request, 'recipe.html', {'recipe': recipe})


def prepare_shopping_list(request, id):
    recipe = Recipe.objects.get(id=id)
    x=get_shopping_list(recipe.ingredients,model='gemma2')
    print(x)
    return JsonResponse(x)



def alternate_recipe(request, alternate_type, id):
    alt = {
        'vegan': 'Vegan Alternative',
        'lowcal': 'Low Calorie Alternative',
        'healthy': 'Healthy Alternative',
    }

    return render(request, 'alternate_recipe.html', {'title': alt[alternate_type], 'recipe_id': id})


def stream_alternate_recipe(request, alternate_type, id):
    recipe = Recipe.objects.get(id=id)

    s = recipe.ingredients+"\n\n"
    s += recipe.instructions + "\n\n"

    alt = {
        'vegan': 'Vegan Alternative',
        'lowcal': 'Low Calorie Alternative',
        'healthy': 'Healthy Alternative',
    }

    generator = alternative_recipe(s, alternate_type, model="llama3")
    return StreamingHttpResponse(generator, content_type='text/plain')