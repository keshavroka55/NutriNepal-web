from django.contrib import admin
from .models import Profile,Food,MealEntry
from .models import WeightEntry

# Register your models here.
admin.site.register(Profile)
admin.site.register(Food)
admin.site.register(MealEntry)

@admin.register(WeightEntry)
class WeightEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight_kg', 'recorded_at')
    list_filter = ('user',)
    ordering = ('-recorded_at',)