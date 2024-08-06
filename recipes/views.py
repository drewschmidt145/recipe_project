from django.shortcuts import render, redirect  # imported by default
from django.views.generic import ListView, DetailView  # to display lists
from .models import Recipe  # to access recipe model
from django.contrib.auth.mixins import LoginRequiredMixin  # to protect class-based view
from django.contrib.auth.decorators import (
    login_required,
)  # to protect function-based view
from .forms import RecipesSearchForm, CreateRecipeForm
import pandas as pd
from .utils import get_recipename_from_id, get_chart
from django.contrib import messages

from django.db.models import Q  # Import Q object for comples queries


# Create your views here.
def recipes_home(request):
    return render(request, "recipes/recipes_home.html")


def about(request):
    return render(request, "recipes/about.html")


class RecipeListView(LoginRequiredMixin, ListView):  # class-based view
    model = Recipe  # specify model
    template_name = "recipes/main.html"  # specity template


class RecipeDetailView(LoginRequiredMixin, DetailView):  # class-based view
    model = Recipe  # specify model
    template_name = "recipes/detail.html"  # specify template


# #define function-based view - search(request)
# #keep protected
@login_required
def search(request):
    # Initialize the search form
    form = RecipesSearchForm(request.POST or None)
    recipes_df = None
    chart = None
    qs = Recipe.objects.none()  # Initialize with an empty queryset

    if request.method == "POST":
        # Check if the form is valid
        if form.is_valid():
            # Retrieve input values from the form
            recipe_name = form.cleaned_data.get("recipe_name")
            ingredients = form.cleaned_data.get("ingredients")
            recipe_diff = form.cleaned_data.get("recipe_diff")
            chart_type = form.cleaned_data.get("chart_type")

            try:
                # Use Q objects for complex queries
                q_objects = Q()

                # If recipe_name is provided, add a filter for name containing the input
                if recipe_name:
                    q_objects &= Q(name__icontains=recipe_name)
                # If ingredients is provided, add a filter for ingredients containing the input
                if ingredients:
                    q_objects &= Q(ingredients__icontains=ingredients)
                # If recipe_diff is provided, add a filter for difficulty matching the input
                if recipe_diff:
                    q_objects &= Q(difficulty=recipe_diff)

                # Filter recipes based on the constructed query
                qs = Recipe.objects.filter(q_objects)

                if qs.exists():
                    # Convert the queryset to a DataFrame for further processing
                    recipes_df = pd.DataFrame(qs.values())

                    # Generate a chart based on the selected chart type
                    chart = get_chart(
                        chart_type, recipes_df, labels=recipes_df["name"].values
                    )

                    # Convert DataFrame to HTML for rendering in the template
                    recipes_df = recipes_df.to_html()

            except Exception as e:
                # Print an error message if an exception occurs during processing
                print(f"Error: {str(e)}")

    # Render the template with the form, search results, and chart
    return render(
        request,
        "recipes/search.html",
        {"form": form, "recipes_df": recipes_df, "chart": chart},
    )


@login_required
def create_view(request):
    if request.method == "POST":
        create_form = CreateRecipeForm(request.POST, request.FILES)
        if create_form.is_valid():
            create_form.save()
            messages.success(request, "Recipe created successfully.")
            return redirect("create")
    else:
        create_form = CreateRecipeForm()

    context = {"create_form": create_form}
    return render(request, "recipes/create.html", context)
