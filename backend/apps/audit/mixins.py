from .models import AuditLog


class AuditMixin:
    """Добавьте этот mixin к ViewSet — он автоматически логирует все изменения."""

    def perform_create(self, serializer):
        obj = serializer.save()
        AuditLog.objects.create(
            user=self.request.user,
            action=AuditLog.Action.CREATE,
            model_name=obj.__class__.__name__,
            object_id=obj.pk,
            object_repr=str(obj),
            changes={"created": True},
        )

    def perform_update(self, serializer):
        obj = serializer.save()
        AuditLog.objects.create(
            user=self.request.user,
            action=AuditLog.Action.UPDATE,
            model_name=obj.__class__.__name__,
            object_id=obj.pk,
            object_repr=str(obj),
            changes={"updated": True},
        )

    def perform_destroy(self, instance):
        AuditLog.objects.create(
            user=self.request.user,
            action=AuditLog.Action.DELETE,
            model_name=instance.__class__.__name__,
            object_id=instance.pk,
            object_repr=str(instance),
            changes={"deleted": True},
        )
        instance.delete()


