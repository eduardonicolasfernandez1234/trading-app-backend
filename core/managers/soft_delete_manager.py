from django.db import models
from core.querysets import SoftDeleteQuerySet


class SoftDeleteManager(models.Manager):
    """Default Manager: Only objects not deleted."""

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).alive()

    def with_deleted(self):
        return SoftDeleteQuerySet(self.model, using=self._db)

    def only_deleted(self):
        return SoftDeleteQuerySet(self.model, using=self._db).deleted()
