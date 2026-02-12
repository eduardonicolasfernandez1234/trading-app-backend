from django.db import models
from django.utils import timezone

from core.querysets import SoftDeleteQuerySet
from core.utils.current_user import get_current_user


class BaseModel(models.Model):
    """
        BaseModel abstract with:
          - timestamps created_at / updated_at
          - auditory created_by / updated_by
          - soft delete
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        'accounts.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created",
        editable=False
    )
    updated_by = models.ForeignKey(
        'accounts.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated",
        editable=False
    )

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()
    all_objects = SoftDeleteQuerySet.as_manager()

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def delete(self, using=None, keep_parents=False, hard=False):
        if hard:
            return super().delete(using=using, keep_parents=keep_parents)
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
        return None

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])

    def save(self, *args, **kwargs):
        current_user = get_current_user()

        if not self.pk and current_user and current_user.is_authenticated:
            self.created_by = current_user
        if current_user and current_user.is_authenticated:
            self.updated_by = current_user

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"
