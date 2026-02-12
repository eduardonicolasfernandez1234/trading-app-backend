import django_filters
from django.db.models import Q

from assets.models import Asset


class AssetFilter(django_filters.FilterSet):
    """
    Filters for Asset list endpoint
    """

    search = django_filters.CharFilter(method='filter_search')

    ordering = django_filters.OrderingFilter(
        fields=(
            ('symbol', 'symbol'),
            ('name', 'name'),
            ('is_tradable', 'is_tradable'),
            ('asset_type__name', 'asset_type'),
            ('created_at', 'created_at'),
        )
    )

    class Meta:
        model = Asset
        fields = [
            'asset_type',
            'is_tradable',
        ]

    def filter_search(self, queryset, name, value):
        """
        Global search across Asset fields
        """
        return queryset.filter(
            Q(symbol__icontains=value) |
            Q(name__icontains=value) |
            Q(asset_type__name__icontains=value)
        )
