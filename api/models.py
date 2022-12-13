from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

class Key(models.Model):
    key = models.CharField(max_length=25, default='', unique=True)
    int_value = models.IntegerField(default=1)
    slug = models.SlugField(max_length=25, default="", unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'key: { self.key }, int_value: { self.int_value }, slug: {self.slug}, created: { self.created_at } last_updated: {self.updated_at}'

def pre_save_key(sender, instance, *args, **kwargs):
    slugified = slugify(instance.key)
    instance.slug = slugified

pre_save.connect(pre_save_key, sender=Key)


class DogPhoto(models.Model):
    breed = models.CharField(max_length=50, default='')
    sub_breed = models.CharField(max_length=50, default='')
    original_url = models.CharField(max_length=250, default='')
    transformed_url = models.CharField(max_length=250, default='')
    unique_photo_id = models.CharField(max_length=250, default='', unique=True)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'breed: { self.breed }, sub_breed { self.sub_breed }, original_url: {self.original_url}, trans_url: { self.transformed_url } unique_id: {self.unique_photo_id}, metadata: {self.metadata}'
