from django.db import models
from django.shortcuts import reverse

# Create your models here.
difficulty_choices = (
    ("Easy", "Easy"),
    ("Medium", "Medium"),
    ("Intermediate", "Intermediate"),
    ("Hard", "Hard"),
)


# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=120)
    cooking_time = models.PositiveIntegerField(help_text="in minutes")
    ingredients = models.CharField(max_length=300)
    difficulty = models.CharField(max_length=12, choices=difficulty_choices)
    pic = models.ImageField(upload_to="recipes", default="no_picture.jpg")

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("recipes:detail", kwargs={"pk": self.pk})
