from rest_framework import serializers
from .models import Key, DogPhoto

class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = ("id", "key", "int_value", "slug", "created_at", "updated_at")

class DogPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogPhoto
        fields = ("id", "breed", "sub_breed", "original_url", "transformed_url", "unique_photo_id", "metadata", "created_at", "updated_at")
