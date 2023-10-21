from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Tag(models.Model):
    label = models.CharField(max_length=255)

class TaggedItem(models.Model):
    # What tag is applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # 1-type(product, video or article)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # 2-Object ID
    object_id = models.IntegerField()
    # The actual object(product) to which the tag is applied to
    content_object = GenericForeignKey()
    