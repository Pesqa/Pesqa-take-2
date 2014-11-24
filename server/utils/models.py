from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.fields import AutoCreatedField, AutoLastModifiedField

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``creatd`` and ``modified`` fields.
    """
    created = AutoCreatedField(_('created'))
    modified = AutoLastModifiedField(_('modified'))
    
    class Meta:
        abstract = True