import django_filters
from django.db.models import Q

from assets.models import AssetType


class AssetTypeFilter(django_filters.FilterSet):
    """
    Filters for AssetType list endpoint
    """

    search = django_filters.CharFilter(method='filter_search')

    ordering = django_filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('created_at', 'created_at'),
        )
    )

    class Meta:
        model = AssetType
        fields = []

    def filter_search(self, queryset, name, value):
        """
        Global search across AssetType fields
        """
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value)
        )
