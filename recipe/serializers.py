from rest_framework import serializers
from .models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    recipe_image = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = Recipe
        fields = [
            'id',
            'user',
            'recipe_name',
            'recipe_description',
            'recipe_image',
            'recipe_view_count',
        ]
        read_only_fields = ['user', 'recipe_view_count']