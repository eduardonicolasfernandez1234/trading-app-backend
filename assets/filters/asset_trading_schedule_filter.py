import django_filters
from django.db.models import Q

from assets.models import AssetTradingSchedule


class AssetTradingScheduleFilter(django_filters.FilterSet):
    """
    Filters for AssetTradingSchedule list endpoint
    """

    search = django_filters.CharFilter(method='filter_search')

    ordering = django_filters.OrderingFilter(
        fields=(
            ('day_of_week', 'day_of_week'),
            ('start_time', 'start_time'),
            ('end_time', 'end_time'),
            ('asset__symbol', 'asset'),
            ('created_at', 'created_at'),
        )
    )

    class Meta:
        model = AssetTradingSchedule
        fields = [
            'asset',
            'day_of_week',
        ]

    def filter_search(self, queryset, name, value):
        """
        Global search across AssetTradingSchedule fields
        """
        return queryset.filter(
            Q(asset__symbol__icontains=value) |
            Q(asset__name__icontains=value)
        )
