import django_filters
from django.db.models import Q

from signals.models import TradingSignal


class TradingSignalFilter(django_filters.FilterSet):
    """
    Filters for TradingSignal list endpoint.

    Supports:
    - Text search across asset symbol, source name, provider name
    - Exact filtering by enums and FKs
    - Date range filtering for signal_time
    """

    search = django_filters.CharFilter(method='filter_search')

    # Date range
    signal_time_from = django_filters.DateTimeFilter(
        field_name='signal_time',
        lookup_expr='gte'
    )
    signal_time_to = django_filters.DateTimeFilter(
        field_name='signal_time',
        lookup_expr='lte'
    )

    class Meta:
        model = TradingSignal
        fields = {
            'direction': ['exact'],
            'status': ['exact'],
            'execution_type': ['exact'],
            'confidence_level': ['exact'],
            'session': ['exact'],

            'signal_source': ['exact'],
            'signal_provider': ['exact'],
            'asset': ['exact'],
        }

    def filter_search(self, queryset, name, value):
        """
        Free text search:
        - Asset symbol
        - Signal source name
        - Signal provider name
        """
        return queryset.filter(
            Q(asset__symbol__icontains=value) |
            Q(signal_source__name__icontains=value) |
            Q(signal_provider__name__icontains=value)
        )
