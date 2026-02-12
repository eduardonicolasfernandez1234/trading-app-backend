from django.db import models


class PlatformChoices(models.TextChoices):
    TELEGRAM = 'telegram', 'Telegram'
    WHATSAPP = 'whatsapp', 'WhatsApp'
    DISCORD = 'discord', 'Discord'
    OTHER = 'other', 'Other'


class SignalStyleChoices(models.TextChoices):
    SCALPING = 'scalping', 'Scalping'
    DAY_TRADING = 'day', 'Day Trading'
    SWING = 'swing', 'Swing Trading'


class RiskProfileChoices(models.TextChoices):
    CONSERVATIVE = 'conservative', 'Conservative'
    MODERATE = 'moderate', 'Moderate'
    AGGRESSIVE = 'aggressive', 'Aggressive'


class DirectionChoices(models.TextChoices):
    BUY = 'buy', 'Buy'
    SELL = 'sell', 'Sell'


class SignalStatusChoices(models.TextChoices):
    ACTIVE = 'active', 'Active'
    CANCELLED = 'cancelled', 'Cancelled'
    HIT_TP = 'hit_tp', 'Hit Take Profit'
    HIT_SL = 'hit_sl', 'Hit Stop Loss'


class ExecutionTypeChoices(models.TextChoices):
    MARKET = 'market', 'Market'
    LIMIT = 'limit', 'Limit'
    STOP = 'stop', 'Stop'


class MarketSessionChoices(models.TextChoices):
    ASIA = 'asia', 'Asia'
    LONDON = 'london', 'London'
    NEW_YORK = 'new_york', 'New York'


class ConfidenceLevelChoices(models.TextChoices):
    LOW = 'low', 'Low'
    MEDIUM = 'medium', 'Medium'
    HIGH = 'high', 'High'


class MarketConditionChoices(models.TextChoices):
    TRENDING = 'trending', 'Trending'
    RANGING = 'ranging', 'Ranging'


class VolatilityLevelChoices(models.TextChoices):
    LOW = 'low', 'Low'
    MEDIUM = 'medium', 'Medium'
    HIGH = 'high', 'High'
