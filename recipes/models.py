from django.db import models

# Id,Title,Ingredients,Instructions,Image_Name,Cleaned_Ingredients

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()
    image_name = models.CharField(max_length=100)
    cleaned_ingredients = models.TextField()

    def __str__(self):
        return self.title