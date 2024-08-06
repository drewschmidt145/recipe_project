from django.test import TestCase
from .models import Recipe  # to access Recipe model
from django.urls import reverse
from .forms import RecipesSearchForm
from django.contrib.auth.models import User


class RecipeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Recipe.objects.create(
            name="Cheeseburger",
            cooking_time=10,
            ingredients="beef patty, bun, cheese",
            difficulty="hard",
        )

    def test_recipe_name(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Get the metadata for the 'name' field and use it to query its data
        field_label = recipe._meta.get_field("name").verbose_name

        # Compare the value to the expected result
        self.assertEqual(field_label, "name")

    def test_ingredients_max_length(self):
        ingredient = Recipe.objects.get(id=1)
        max_length = ingredient._meta.get_field("ingredients").max_length
        self.assertEqual(max_length, 300)

    def test_cookingtime_helptext(self):
        recipe = Recipe.objects.get(id=1)
        recipe_cookingtime = recipe._meta.get_field("cooking_time").help_text
        self.assertEqual(recipe_cookingtime, "in minutes")

    def test_difficulty_calculation(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.difficulty, "hard")

    # Get absolute URL
    def test_get_absolute_url(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.get_absolute_url(), "/list/1/")

    def test_list_view(self):
        # Log in a user before accessing the list view
        user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

        response = self.client.get(reverse("recipes:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/main.html")

    def test_detail_view(self):
        # Log in a user before accessing the detail view
        user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

        recipe = Recipe.objects.get(id=1)
        response = self.client.get(recipe.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/detail.html")


class RecipesSearchFormTest(TestCase):
    def test_form_renders_recipe_diff_input(self):
        # Test that the 'recipe_diff' field is rendered in the form
        form = RecipesSearchForm()
        self.assertIn("recipe_diff", form.as_p())

    def test_form_renders_chart_type_input(self):
        # Test that the 'chart_type' field is rendered in the form
        form = RecipesSearchForm()
        self.assertIn("chart_type", form.as_p())

    def test_form_valid_data(self):
        # Test that the form is considered valid when valid data is provided
        form = RecipesSearchForm(data={"recipe_diff": "Easy", "chart_type": "#2"})
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_invalid_data(self):
        # Test that the form is considered invalid when invalid data is provided
        form = RecipesSearchForm(data={"recipe_diff": "#1", "chart_type": ""})
        self.assertFalse(form.is_valid(), form.errors)
