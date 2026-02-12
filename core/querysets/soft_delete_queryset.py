from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    """QuerySet with soft delete support."""

    def delete(self, hard=False):
        if hard:
            return super().delete()
        return super().update(is_active=False, deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(is_active=True)

    def deleted(self):
        return self.filter(is_active=False)

    def restore(self):
        return self.filter(is_active=False).update(is_active=True, deleted_at=None)
