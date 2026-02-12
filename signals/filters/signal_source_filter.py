import django_filters

from signals.models import SignalSource


class SignalSourceFilter(django_filters.FilterSet):
    """
    Filters for SignalSource list endpoint
    """
    search = django_filters.CharFilter(method='filter_search')

    ordering = django_filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('platform', 'platform'),
            ('signal_style', 'signal_style'),
            ('risk_profile', 'risk_profile'),
            ('is_private', 'is_private'),
            ('created_at', 'created_at'),
        )
    )

    class Meta:
        model = SignalSource
        fields = [
            'platform',
            'signal_style',
            'risk_profile',
            'is_private',
        ]

    def filter_search(self, queryset, name, value):
        """
        Global search across multiple fields
        """
        return queryset.filter(name__icontains=value) | queryset.filter(platform__icontains=value)
