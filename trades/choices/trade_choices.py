from django.db import models


class TradeStatusChoices(models.TextChoices):
    """
    Estados posibles de un trade a nivel lógico.
    """
    OPEN = 'open', 'Open'
    PARTIALLY_CLOSED = 'partially_closed', 'Partially Closed'
    CLOSED = 'closed', 'Closed'


class TradeEntrySourceChoices(models.TextChoices):
    """
    Origen de la apertura de una posición.
    """
    MANUAL = 'manual', 'Manual'
    BOT = 'bot', 'Bot'
    API = 'api', 'API'


class TradeCloseReasonChoices(models.TextChoices):
    """
    Motivo por el cual se cierra total o parcialmente una posición.
    """
    TAKE_PROFIT = 'tp', 'Take Profit'
    STOP_LOSS = 'sl', 'Stop Loss'
    MANUAL = 'manual', 'Manual'
    BOT = 'bot', 'Bot'


class TradeCostTypeChoices(models.TextChoices):
    """
    Tipos de costos asociados a un trade o a un cierre.
    """
    SWAP = 'swap', 'Swap'
    COMMISSION = 'commission', 'Commission'
    FEE = 'fee', 'Fee'
    OTHER = 'other', 'Other'
