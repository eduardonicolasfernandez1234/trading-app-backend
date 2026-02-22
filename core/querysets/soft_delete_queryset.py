from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    """QuerySet with soft delete support."""

    def delete(self, hard=False):
        if hard:
            return super().delete()
        return super().update(is_deleted=True, deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(is_deleted=False)

    def deleted(self):
        return self.filter(is_deleted=True)

    def restore(self):
        return self.filter(is_deleted=True).update(is_deleted=False, deleted_at=None)
