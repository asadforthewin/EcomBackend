from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey



class TaggedItemManager(models.Manager):
    def get_tags_for(self,obj_type,obj_id ):

        contenttype = ContentType.objects.get_for_model(obj_type)
        return TaggedItem.objects.select_related('tag').    filter(content_type = contenttype, 
                                            object_id= obj_id)


class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.label

class TaggedItem(models.Model):
    objects= TaggedItemManager() #custom manager 
    # What tag is applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # 1-type(product, video or article)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # 2-Object ID
    object_id = models.IntegerField()
    # The actual object(product) to which the tag is applied to
    content_object = GenericForeignKey()
    