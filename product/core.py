from django.db import models
import uuid


def guid_factory() -> str:
    return uuid.uuid4().hex


class BlankModel(models.Model):
    class Meta:
        abstract = True


class AbstractBaseModel(BlankModel):
    guid = models.CharField(max_length=255, default=guid_factory, editable=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f'Row {self.guid}'
