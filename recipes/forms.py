from django import forms
from .models import Recipe

CHART_CHOICES = (("#1", "Bar chart"), ("#2", "Pie chart"), ("#3", "Line chart"))

DIFFICULTY_CHOICES = (
    ("", " "),
    ("Easy", "Easy"),
    ("Medium", "Medium"),
    ("Intermediate", "Intermediate"),
    ("Hard", "Hard"),
)


class RecipesSearchForm(forms.Form):
    recipe_name = forms.CharField(max_length=120, required=False, label="Recipe Name")
    ingredients = forms.CharField(max_length=300, required=False, label="Ingredients")
    recipe_diff = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES, required=False, label="Recipe Difficulty Level"
    )
    chart_type = forms.ChoiceField(
        choices=CHART_CHOICES, required=False, label="Chart Type"
    )


class CreateRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["name", "cooking_time", "difficulty", "ingredients", "pic"]
