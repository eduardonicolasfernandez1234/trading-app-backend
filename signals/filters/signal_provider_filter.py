import django_filters
from django.db.models import Q

from signals.models import SignalProvider


class SignalProviderFilter(django_filters.FilterSet):
    """
    Filters for SignalProvider list endpoint
    """

    search = django_filters.CharFilter(method='filter_search')

    ordering = django_filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('alias', 'alias'),
            ('is_anonymous', 'is_anonymous'),
            ('experience_level', 'experience_level'),
            ('signal_source__name', 'signal_source'),
            ('created_at', 'created_at'),
        )
    )

    class Meta:
        model = SignalProvider
        fields = [
            'signal_source',
            'is_anonymous',
            'experience_level',
        ]

    def filter_search(self, queryset, name, value):
        """
        Global search across multiple fields
        """
        return queryset.filter(
            Q(name__icontains=value) |
            Q(alias__icontains=value) |
            Q(signal_source__name__icontains=value)
        )
