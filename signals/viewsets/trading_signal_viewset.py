from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from analytics.services import SignalPerformanceService, SignalAccuracyService
from signals.filters import TradingSignalFilter
from signals.models import TradingSignal, SignalSource, SignalProvider
from signals.serializers import TradingSignalSerializer


class TradingSignalViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar señales de trading.
    """
    queryset = TradingSignal.objects.select_related(
        'asset',
        'signal_source',
        'signal_provider'
    )
    serializer_class = TradingSignalSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = TradingSignalFilter

    ordering_fields = [
        'signal_time',
        'entry_price',
        'status',
        'direction',
        'asset__symbol',
    ]
    ordering = ['-signal_time']

    @action(detail=False, methods=['get'], url_path='quick-search')
    def quick_search(self, request):
        """
        Endpoint optimizado para inputs de búsqueda rápida.
        - Sin paginación
        - Máx 30 registros
        - Con filtros + search
        """
        queryset = self.filter_queryset(self.get_queryset())[:30]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='follow')
    def follow(self, request, pk=None):
        """
        Marca una señal como seguida por el usuario.
        """
        signal = self.get_object()
        user = request.user

        # Pseudocódigo: persistir decisión
        decision = {
            'user_id': user.id,
            'signal_id': signal.id,
            'decision': 'followed',
            'source': request.data.get('source', 'manual'),
            'timestamp': timezone.now()
        }

        return Response({
            'message': 'Signal followed',
            'decision': decision
        })

    @action(detail=True, methods=['post'], url_path='ignore')
    def ignore(self, request, pk=None):
        """
        Marca una señal como ignorada por el usuario.
        Solo afecta a esta señal.
        """
        signal = self.get_object()
        user = request.user

        decision = {
            'user_id': user.id,
            'signal_id': signal.id,
            'decision': 'ignored',
            'source': request.data.get('source', 'manual'),
            'reason': request.data.get('reason'),
            'timestamp': timezone.now()
        }

        return Response({
            'message': 'Signal ignored',
            'decision': decision
        })

    @action(detail=True, methods=['get'], url_path='evaluate')
    def evaluate(self, request, pk=None):
        """
        Evalúa el resultado teórico de una señal
        independientemente del usuario.
        """
        signal = self.get_object()

        performance = SignalPerformanceService.calculate_signal_performance(signal)

        return Response({
            'signal_id': signal.id,
            'performance_id': performance.id,
            'status': 'evaluated'
        })

    @action(detail=False, methods=['get'], url_path='accuracy-by-source')
    def accuracy_by_source(self, request):
        """
        Devuelve la precisión histórica por grupo de señales.
        """
        sources = SignalSource.objects.all()
        results = []

        for source in sources:
            results.append(
                SignalAccuracyService.accuracy_by_signal_source(source)
            )

        return Response(results)

    @action(detail=False, methods=['get'], url_path='accuracy-by-provider')
    def accuracy_by_provider(self, request):
        """
        Devuelve la precisión histórica por proveedor/instructor.
        """
        providers = SignalProvider.objects.all()
        results = []

        for provider in providers:
            results.append(
                SignalAccuracyService.accuracy_by_provider(provider)
            )

        return Response(results)

    @action(detail=True, methods=['get'], url_path='suggestion')
    def suggestion(self, request, pk=None):
        """
        Devuelve una sugerencia para la señal (seguir / ignorar).
        """
        signal = self.get_object()
        source = signal.signal_source

        accuracy_data = SignalAccuracyService.accuracy_by_signal_source(source)

        ignore = accuracy_data['accuracy_percent'] < 40

        return Response({
            'signal_id': signal.id,
            'signal_source': source.name,
            'historical_accuracy': accuracy_data['accuracy_percent'],
            'suggestion': 'ignore' if ignore else 'follow',
            'reason': (
                'Low historical accuracy'
                if ignore else 'Good historical performance'
            )
        })
