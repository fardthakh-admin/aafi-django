from import_export import resources
from .models import *


class NutritionDataResource(resources.ModelResource):
    class Meta:
        model = nutrition
        fields = ('name', 'carbContent', 'name_ar', 'name_en', 'portion',
                  'proteinContent', 'totalCalories', 'weight')  # Adjust fields as necessary
