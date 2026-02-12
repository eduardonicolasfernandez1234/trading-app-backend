import django_filters
from django.db.models import Q

from assets.models import AssetSwap


class AssetSwapFilter(django_filters.FilterSet):
    """
    Filters for AssetSwap list endpoint
    """

    search = django_filters.CharFilter(method='filter_search')

    ordering = django_filters.OrderingFilter(
        fields=(
            ('swap_long', 'swap_long'),
            ('swap_short', 'swap_short'),
            ('triple_swap_day', 'triple_swap_day'),
            ('asset__symbol', 'asset'),
            ('created_at', 'created_at'),
        )
    )

    class Meta:
        model = AssetSwap
        fields = [
            'asset',
            'triple_swap_day',
        ]

    def filter_search(self, queryset, name, value):
        """
        Global search across AssetSwap fields
        """
        return queryset.filter(
            Q(asset__symbol__icontains=value) |
            Q(asset__name__icontains=value)
        )
