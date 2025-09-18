from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    GOAL_CHOICES = (
        ('lose', 'Lose Weight'),
        ('maintain', 'Maintain'),
        ('gain', 'Gain Weight'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(default=20)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='M')
    height_cm = models.FloatField(default=170)
    weight_kg = models.FloatField(default=65)
    activity_factor = models.FloatField(default=1.4)  # 1.2 sedentary → 1.9 very active
    goal = models.CharField(max_length=10, choices=GOAL_CHOICES, default='maintain')

    def bmr(self):
        # Mifflin-St Jeor
        if self.sex == 'M':
            return 10 * self.weight_kg + 6.25 * self.height_cm - 5 * self.age + 5
        return 10 * self.weight_kg + 6.25 * self.height_cm - 5 * self.age - 161

    def tdee(self):
        return self.bmr() * self.activity_factor

    def daily_target_kcal(self):
        tdee = self.tdee()
        if self.goal == 'lose':
            return max(1200, tdee - 500)  # simple cut
        if self.goal == 'gain':
            return tdee + 300
        return tdee

    def __str__(self):
        return f"Profile({self.user.username})"


class Food(models.Model):
    name = models.CharField(max_length=120, unique=True)
    serving_size_g = models.FloatField(default=100)
    kcal = models.FloatField()
    protein_g = models.FloatField(default=0)
    fat_g = models.FloatField(default=0)
    carbs_g = models.FloatField(default=0)

    def __str__(self):
        return f"{self.name} ({self.serving_size_g}g)"


class MealEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.localdate)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    servings = models.FloatField(default=1.0)  # relative to food.serving_size_g

    @property
    def kcal(self):
        return self.food.kcal * self.servings

    @property
    def protein_g(self):
        return self.food.protein_g * self.servings

    @property
    def fat_g(self):
        return self.food.fat_g * self.servings

    @property
    def carbs_g(self):
        return self.food.carbs_g * self.servings

    def __str__(self):
        return f"{self.user.username} - {self.food.name} x {self.servings}"
    

# for weight histroy

class WeightEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight_entries')
    weight_kg = models.FloatField()
    recorded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-recorded_at']  # newest first

    def __str__(self):
        return f"{self.user.username} — {self.weight_kg} kg @ {self.recorded_at.date()}"