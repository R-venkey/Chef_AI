import csv
import ast
from django.core.management.base import BaseCommand
from recipes.models import Recipe  # Replace 'your_app' with your actual app name

class Command(BaseCommand):
    help = 'Load recipes from a CSV file into the Recipe model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            recipes = []

            for row in reader:
                # Convert ingredients and cleaned_ingredients from string to list
                ingredients = ast.literal_eval(row['Ingredients']) if row['Ingredients'] else []
                cleaned_ingredients = ast.literal_eval(row['Cleaned_Ingredients']) if row['Cleaned_Ingredients'] else []

                recipe = Recipe(
                    title=row['Title'],
                    ingredients="\n".join(ingredients),  # Store as a newline-separated string
                    instructions=row['Instructions'],
                    image_name=row['Image_Name'],
                    cleaned_ingredients="\n".join(cleaned_ingredients)  # Store as a newline-separated string
                )
                recipes.append(recipe)

            Recipe.objects.bulk_create(recipes)
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(recipes)} recipes'))
