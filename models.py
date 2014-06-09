from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Object(models.Model):
    """
    Object Documentation
    """
    name = models.CharField(max_length=128, blank=False, help_text="Terms Name")
    slug = models.SlugField(blank=True, null=True)
    account = models.ForeignKey(User)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Object, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0.name}".format(self)

    class Meta:
        verbose_name = 'object'
        verbose_name_plural = 'objects'
        unique_together = ('account', 'slug')

