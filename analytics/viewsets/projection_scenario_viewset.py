from decimal import Decimal

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from analytics.models import ProjectionScenario
from analytics.serializers import ProjectionScenarioSerializer
from analytics.services import AnalyticsRunService
from analytics.services.projection_simulation_service import ProjectionSimulationService
from trades.models import Trade


class ProjectionScenarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar escenarios de proyección y simulación.

    Permite a los usuarios crear escenarios hipotéticos para
    simular resultados futuros basados en datos históricos.
    """
    queryset = ProjectionScenario.objects.all()
    serializer_class = ProjectionScenarioSerializer

    @action(detail=True, methods=['post'], url_path='run-simulation')
    def run_simulation(self, request, pk=None):
        scenario = self.get_object()
        user = request.user

        initial_balance = Decimal(
            request.data.get('initial_balance', scenario.initial_balance)
        )
        risk_percent = Decimal(
            request.data.get('risk_per_trade_percent', scenario.risk_per_trade_percent)
        )
        mode = request.data.get('mode', 'historical')
        save_result = request.data.get('save_result', False)

        trades = Trade.objects.filter(
            trade_account__user=user,
            status='closed'
        ).order_by('closed_at')

        result = ProjectionSimulationService.simulate(
            historical_trades=list(trades),
            initial_balance=initial_balance
        )

        # Ajuste de riesgo
        if mode == 'adjusted':
            factor = risk_percent / Decimal('1.0')
            equity = initial_balance
            for point in result['equity_curve']:
                point['pnl'] *= factor
                equity += point['pnl']
                point['equity'] = equity

            result['final_balance'] = equity

        response_payload = {
            'scenario_id': scenario.id,
            'mode': mode,
            'initial_balance': initial_balance,
            'risk_per_trade_percent': risk_percent,
            'final_balance': result['final_balance'],
            'max_drawdown_percent': result['max_drawdown_percent'],
            'equity_curve': result['equity_curve'],
        }

        # 💾 Persistir si el usuario quiere
        if save_result:
            AnalyticsRunService.create_run(
                user=user,
                run_type='projection_simulation',
                input_payload=request.data,
                output_payload=response_payload
            )

        return Response(response_payload)

    @action(detail=False, methods=['post'], url_path='compare')
    def compare_scenarios(self, request):
        """
        Compara múltiples escenarios de proyección.
        Cada escenario debe pertenecer a una sola fuente de señales.
        """
        scenario_ids = request.data.get('scenario_ids', [])
        scenarios = ProjectionScenario.objects.filter(
            id__in=scenario_ids,
            user=request.user
        )

        results = []

        for scenario in scenarios:
            trades = Trade.objects.filter(
                trade_account__user=request.user,
                trading_signal__signal_source=scenario.signal_source,
                status='closed'
            ).order_by('closed_at')

            simulation = ProjectionSimulationService.simulate(
                historical_trades=list(trades),
                initial_balance=scenario.initial_balance
            )

            results.append({
                'scenario_id': scenario.id,
                'signal_source': scenario.signal_source.name if scenario.signal_source else None,
                'final_balance': simulation['final_balance'],
                'max_drawdown_percent': simulation['max_drawdown_percent'],
            })

        return Response(results)

    @action(detail=True, methods=['get'], url_path='equity-curve')
    def equity_curve(self, request, pk=None):
        """
        Devuelve la curva de equity del escenario.
        """
        scenario = self.get_object()

        trades = Trade.objects.filter(
            trade_account__user=request.user,
            trading_signal__signal_source=scenario.signal_source,
            status='closed'
        ).order_by('closed_at')

        result = ProjectionSimulationService.simulate(
            historical_trades=list(trades),
            initial_balance=scenario.initial_balance
        )

        return Response(result['equity_curve'])
