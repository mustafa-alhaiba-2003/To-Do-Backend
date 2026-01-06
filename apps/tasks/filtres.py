import django_filters
from django.utils import timezone
from django.db.models import Q

from .models import Task


class TaskFilter(django_filters.FilterSet):
    # --- IDs ---
    id = django_filters.NumberFilter(field_name="id")
    id__in = django_filters.BaseInFilter(field_name="id", lookup_expr="in")

    # --- Choice fields ---
    status = django_filters.CharFilter(field_name="status")
    status__in = django_filters.BaseInFilter(field_name="status", lookup_expr="in")

    priority = django_filters.CharFilter(field_name="priority")
    priority__in = django_filters.BaseInFilter(field_name="priority", lookup_expr="in")

    # --- Text filters ---
    title = django_filters.CharFilter(field_name="title", lookup_expr="exact")
    title__icontains = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    title__istartswith = django_filters.CharFilter(field_name="title", lookup_expr="istartswith")

    description__icontains = django_filters.CharFilter(field_name="description", lookup_expr="icontains")

    # "q" param to search title OR description (in addition to DRF SearchFilter)
    q = django_filters.CharFilter(method="filter_q")

    def filter_q(self, queryset, name, value):
        value = (value or "").strip()
        if not value:
            return queryset
        return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value))

    # --- Date/time filters (ranges) ---
    # start_date: auto_now_add, but still filterable
    start_date = django_filters.IsoDateTimeFilter(field_name="start_date")
    start_date__gte = django_filters.IsoDateTimeFilter(field_name="start_date", lookup_expr="gte")
    start_date__lte = django_filters.IsoDateTimeFilter(field_name="start_date", lookup_expr="lte")
    start_date__range = django_filters.IsoDateTimeFromToRangeFilter(field_name="start_date")

    due_date = django_filters.IsoDateTimeFilter(field_name="due_date")
    due_date__gte = django_filters.IsoDateTimeFilter(field_name="due_date", lookup_expr="gte")
    due_date__lte = django_filters.IsoDateTimeFilter(field_name="due_date", lookup_expr="lte")
    due_date__range = django_filters.IsoDateTimeFromToRangeFilter(field_name="due_date")

    # --- Helpful booleans ---
    overdue = django_filters.BooleanFilter(method="filter_overdue")
    due_today = django_filters.BooleanFilter(method="filter_due_today")

    # due_in_days=7  -> due date within next N days
    due_in_days = django_filters.NumberFilter(method="filter_due_in_days")

    def filter_overdue(self, queryset, name, value):
        if value is None:
            return queryset
        now = timezone.now()
        if value is True:
            return queryset.filter(due_date__lt=now, status="in-progress")
        return queryset.exclude(due_date__lt=now, status="in-progress")

    def filter_due_today(self, queryset, name, value):
        if value is None:
            return queryset
        today = timezone.localdate()
        if value is True:
            return queryset.filter(due_date__date=today)
        return queryset.exclude(due_date__date=today)

    def filter_due_in_days(self, queryset, name, value):
        if value in (None, ""):
            return queryset
        try:
            days = int(value)
        except (TypeError, ValueError):
            return queryset
        now = timezone.now()
        end = now + timezone.timedelta(days=days)
        return queryset.filter(due_date__gte=now, due_date__lte=end)
