
from django import forms
from django.contrib.auth.models import User
from .models import Profile, Food, MealEntry

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('age', 'sex', 'height_cm', 'weight_kg', 'activity_factor', 'goal')

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ('name', 'serving_size_g', 'kcal', 'protein_g', 'fat_g', 'carbs_g')

class MealForm(forms.ModelForm):
    class Meta:
        model = MealEntry
        fields = ('date', 'food', 'servings')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

# for meal edit
class MealEntryForm(forms.ModelForm):
    class Meta:
        model = MealEntry
        fields = ['date', 'food', 'servings']


class WeightUpdateForm(forms.Form):
    weight_kg = forms.FloatField(label="Weight (kg)", min_value=0, max_value=500,
                                 widget=forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'}))
    

# foods_list control over only the superuser. 
class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'serving_size_g', 'kcal', 'protein_g', 'fat_g', 'carbs_g']
        # or use exclude = ['creator', 'created_at']

    