from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from tracker.models import Food

@login_required
def foods_list(request):
    """
    Searchable foods list:
    - non-superusers see: foods created by any superuser OR foods they created (default behavior)
    - superusers see all foods
    Filters are applied on top of that base visibility.
    """

    # Base queryset depending on user's role
    if request.user.is_superuser:
        qs = Food.objects.all().order_by('-created_at')
    else:
        qs = Food.objects.filter(Q(creator__is_superuser=True) | Q(creator=request.user)).order_by('-created_at')

    # --- Read GET params ---
    q = request.GET.get('q', '').strip()                  # text search
    creator_filter = request.GET.get('creator', 'all')    # 'all' | 'my' | 'global'
    min_kcal = request.GET.get('min_kcal', '')
    max_kcal = request.GET.get('max_kcal', '')
    min_protein = request.GET.get('min_protein', '')
    max_protein = request.GET.get('max_protein', '')

    # --- Build filters using Q objects ---
    filters = Q()

    if q:
        # search in name (case-insensitive, partial)
        filters &= Q(name__icontains=q)

    # numeric filters: convert safely, ignore invalid input
    def to_float(val):
        try:
            return float(val)
        except (TypeError, ValueError):
            return None

    min_k = to_float(min_kcal)
    max_k = to_float(max_kcal)
    if min_k is not None:
        filters &= Q(kcal__gte=min_k)
    if max_k is not None:
        filters &= Q(kcal__lte=max_k)

    min_p = to_float(min_protein)
    max_p = to_float(max_protein)
    if min_p is not None:
        filters &= Q(protein_g__gte=min_p)
    if max_p is not None:
        filters &= Q(protein_g__lte=max_p)

    # creator filter (applies AFTER base visibility)
    if creator_filter == 'my':
        # show only foods user created
        filters &= Q(creator=request.user)
    elif creator_filter == 'global':
        # show only foods created by superusers
        filters &= Q(creator__is_superuser=True)
    # else 'all' => no extra creator filter (respect base visibility)

    # Apply filters
    qs = qs.filter(filters)

    # --- Pagination ---
    page = request.GET.get('page', 1)
    paginator = Paginator(qs, 15)  # 15 items per page (adjust as needed)
    try:
        foods_page = paginator.page(page)
    except PageNotAnInteger:
        foods_page = paginator.page(1)
    except EmptyPage:
        foods_page = paginator.page(paginator.num_pages)

    # Keep query params (except page) for pagination links
    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')

    context = {
        'foods': foods_page,
        'query_params': query_params,
        # also pass the current filter values so template can keep them populated
        'q': q,
        'creator_filter': creator_filter,
        'min_kcal': min_kcal,
        'max_kcal': max_kcal,
        'min_protein': min_protein,
        'max_protein': max_protein,
    }
    return render(request, 'search.html', context)
