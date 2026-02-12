from analytics.models import AnalyticsRun


class AnalyticsRunService:
    """
    Servicio para registrar ejecuciones de analytics.
    """

    @staticmethod
    def create_run(*, user, run_type, input_payload, output_payload):
        return AnalyticsRun.objects.create(
            user=user,
            analysis_type=run_type,
            input_data=input_payload,
            output_data=output_payload,
            status='completed'
        )
