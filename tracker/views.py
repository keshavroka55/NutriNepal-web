from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, F, FloatField
from datetime import date

from .models import Profile, Food, MealEntry
from .forms import  FoodForm, MealForm,MealEntryForm
# for the weights
from django.urls import reverse
from .forms import WeightUpdateForm
from .models import WeightEntry
from .models import Profile
import json

from django.http import HttpResponseForbidden
from django.db.models import Q



def home(request):
    return render(request,'homepage.html')

@login_required
def dashboard(request):
    print("Current user:", request.user)
    today = request.GET.get('date') or timezone.localdate()
    entries = MealEntry.objects.filter(user=request.user, date=today)

    totals = entries.aggregate(
        kcal=Sum('food__kcal', distinct=False),  # not correct with servings directly
        protein_g=Sum('food__protein_g'),
        fat_g=Sum('food__fat_g'),
        carbs_g=Sum('food__carbs_g'),
    )
    # Compute with servings manually
    total_kcal = sum(e.kcal for e in entries)
    total_protein = sum(e.protein_g for e in entries)
    total_fat = sum(e.fat_g for e in entries)
    total_carbs = sum(e.carbs_g for e in entries)

    profile = get_object_or_404(Profile, user=request.user)
    target = profile.daily_target_kcal()
    remaining = max(0, target - total_kcal)
    # total_kcal = profile.total_kcal()


    context = {
        'date': today,
        'entries': entries.order_by('-id'),
        'total_kcal': round(total_kcal, 1),
        'total_protein': round(total_protein, 1),
        'total_fat': round(total_fat, 1),
        'total_carbs': round(total_carbs, 1),
        'target_kcal': round(target, 0),
        'remaining_kcal': round(remaining, 0),
    }
    return render(request, 'dashboard.html', context)

@login_required
def foods_list(request):
    """
    - Foods created by superusers: visible to everyone.
    - Foods created by normal users: visible only to the creator.
    """
    if request.user.is_superuser:
        foods = Food.objects.filter(Q(creator__is_superuser=True)).order_by('-created_at')
    else:
        foods = Food.objects.filter(Q(creator__is_superuser=True) | Q(creator=request.user)).order_by('-created_at')
    return render(request, 'FoodCURD/foods_list.html', {'foods': foods})

@login_required
def food_create(request):
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            food = form.save(commit=False)
            food.creator = request.user
            food.save()
            messages.success(request, 'Food added!')
            return redirect('foods_list')
    else:
        form = FoodForm()
    return render(request, 'add_food.html', {'form': form, 'title': 'Add Food'})

@login_required
def food_update(request, pk):
    food = get_object_or_404(Food, pk=pk)
    # authorization: only superuser or owner can edit
    if not (request.user.is_superuser or food.creator == request.user):
        messages.error(request, "You don't have permission to edit this food.")
        return HttpResponseForbidden("Forbidden")

    if request.method == 'POST':
        form = FoodForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            messages.success(request, 'Food updated!')
            return redirect('foods_list')
    else:
        form = FoodForm(instance=food)
    return render(request, 'food_form.html', {'form': form, 'title': 'Edit Food'})

@login_required
def food_delete(request, pk):
    food = get_object_or_404(Food, pk=pk)
    # authorization: only superuser or owner can delete
    if not (request.user.is_superuser or food.creator == request.user):
        messages.error(request, "You don't have permission to delete this food.")
        return HttpResponseForbidden("Forbidden")

    if request.method == 'POST':
        food.delete()
        messages.success(request, 'Food deleted!')
        return redirect('foods_list')

    # GET -> show confirmation
    return render(request, 'FoodCURD/food_confirm_delete.html', {'food': food})


@login_required
def meal_create(request):
    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            messages.success(request, 'Meal added!')
            return redirect('dashboard')
    else:
        form = MealForm()
    return render(request, 'meal_form.html', {'form': form, 'title': 'Add Meal'})

# for daily Kcal intake

@login_required
def daily_kcal_summary(request):
    """
    Aggregate MealEntry per day for the logged-in user and return a list-of-dicts:
      [{'date': 'YYYY-MM-DD', 'total_kcal': 2200.0, 'total_protein': 120.0, ...}, ...]
    ORDER: oldest -> newest (ascending) so the template/chart code can treat the last item as the latest day.
    """
    qs = (
        MealEntry.objects.filter(user=request.user)
        .values('date')
        .annotate(
            total_kcal=Sum(F('food__kcal') * F('servings'), output_field=FloatField()),
            total_protein=Sum(F('food__protein_g') * F('servings'), output_field=FloatField()),
            total_fat=Sum(F('food__fat_g') * F('servings'), output_field=FloatField()),
            total_carbs=Sum(F('food__carbs_g') * F('servings'), output_field=FloatField()),
        )
        .order_by('date')  # <-- ascending: oldest first, newest last
    )

    # convert to list of simple dicts with ISO date strings and float values
    daily_kcal = []
    for r in qs:
        d = r.get('date')
        daily_kcal.append({
            'date': d,  # keep Python date object
            'date_str': d.isoformat() if hasattr(d, 'isoformat') else str(d),  # for Chart.js
            'total_kcal': float(r['total_kcal'] or 0),
            'total_protein': float(r['total_protein'] or 0),
            'total_fat': float(r['total_fat'] or 0),
            'total_carbs': float(r['total_carbs'] or 0),
        })

    return render(request, 'history/daily_kcal_summary.html', {'daily_kcal': daily_kcal})

@login_required
def daily_kcal_detail(request, year, month, day):
    """
    Shows the meal entries for a specific date and a per-day total.
    URL will pass year/month/day to identify the date.
    """
    the_date = date(year=int(year), month=int(month), day=int(day))
    entries = MealEntry.objects.filter(user=request.user, date=the_date).select_related('food').order_by('id')

    totals = entries.aggregate(
        total_kcal=Sum(F('food__kcal') * F('servings'), output_field=FloatField()),
        total_protein=Sum(F('food__protein_g') * F('servings'), output_field=FloatField()),
        total_fat=Sum(F('food__fat_g') * F('servings'), output_field=FloatField()),
        total_carbs=Sum(F('food__carbs_g') * F('servings'), output_field=FloatField()),
    )

    # ensure zeros instead of None
    for k in ['total_kcal', 'total_protein', 'total_fat', 'total_carbs']:
        totals[k] = totals.get(k) or 0.0

    return render(request, 'history/daily_kcal_detail.html', {
        'date': the_date,
        'entries': entries,
        'totals': totals,
    })



@login_required
def update_weight(request):
    # ensure profile exists
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = WeightUpdateForm(request.POST)
        if form.is_valid():
            w = form.cleaned_data['weight_kg']

            # Save a new history entry
            WeightEntry.objects.create(user=request.user, weight_kg=w, recorded_at=timezone.now())

            # Update user's profile current weight
            profile.weight_kg = w
            profile.save()

            return redirect('weight_history')
    else:
        # prefill with current profile weight
        initial = {'weight_kg': profile.weight_kg or 0.0}
        form = WeightUpdateForm(initial=initial)

    return render(request, 'history/update_weight.html', {'form': form, 'profile': profile})

@login_required
def weight_history(request):
    # fetch history entries for this user (limit to 100 for performance)
    entries = WeightEntry.objects.filter(user=request.user).order_by('-recorded_at')  # oldest -> newest for chart

    # Build lists for chart labels and data (dates and weights)
    labels = [e.recorded_at.date().isoformat() for e in entries]  # 'YYYY-MM-DD'
    data = [round(e.weight_kg, 2) for e in entries]

    # You can optionally limit to last N days:
    # entries = entries.reverse()[:30]  # last 30 entries then reverse again etc.

    return render(request, 'history/weight_history.html', {
        'entries': entries,
        'labels_json': json.dumps(labels),
        'data_json': json.dumps(data),
        'current_weight': getattr(request.user, 'profile', None).weight_kg if hasattr(request.user, 'profile') else None,
    })
