from django.db import models

# id,Title,Ingredients,Instructions,Image_Name,Cleaned_Ingredients

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()
    image_name = models.CharField(max_length=100)
    cleaned_ingredients = models.TextField()

    def __str__(self):
        return self.title

    def get(self, n):
        if n=='title':
            return self.title
        if n=='ingredients':
            return self.ingredients
        if n=='instructions':
            return self.instructions
        if n=='image_name':
            return self.image_name
        if n=='cleaned_ingredients':
            return self.cleaned_ingredients