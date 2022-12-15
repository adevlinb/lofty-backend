from django.shortcuts import render
from rest_framework import generics
from .serializers import KeySerializer, DogPhotoSerializer
from .models import Key, DogPhoto
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from imagekitio import ImageKit
import requests
import os
import json

def home(request):
  return render(request, 'home.html')


@api_view(['GET', 'POST', 'DELETE'])
def keys_list(request):
    if request.method == 'GET':
        keys = Key.objects.all()
        keys_serializer = KeySerializer(keys, many=True)
        return JsonResponse(keys_serializer.data, safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        key_data = JSONParser().parse(request)
        key_serializer = KeySerializer(data=key_data)
        if key_serializer.is_valid():
            key_serializer.save()
            return JsonResponse(key_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(key_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Key.objects.all().delete()
        delete_message = json.dumps({'message': 'All keys were deleted successfully!'})
        return JsonResponse(delete_message, safe=False, status=status.HTTP_204_NO_CONTENT)




@api_view(['GET', 'PUT', 'DELETE'])
def key_detail(request, pk):
    try:
        key = Key.objects.get(pk=pk)
    except Key.DoesNotExist:
        message = json.dumps({'message': 'The key does not exist'})
        return JsonResponse(message, safe=False, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        key_serializer = KeySerializer(key)
        return JsonResponse(key_serializer.data)

    elif request.method == 'PUT':
        key_data = JSONParser().parse(request)
        key_serializer = KeySerializer(key, data=key_data)
        if key_serializer.is_valid():
            key_serializer.save()
            return JsonResponse(key_serializer.data)
        return JsonResponse(key_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        key.delete()
        delete_message = json.dumps({'message': 'The key was deleted successfully!'})
        return JsonResponse(delete_message, safe=False, status=status.HTTP_204_NO_CONTENT)




@api_view(['GET', 'PUT', 'DELETE'])
def key_slug_detail(request, slug):
    try:
        key = Key.objects.get(slug=slug)
    except Key.DoesNotExist:
        message = json.dumps({'message': 'The key does not exist'})
        return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        key_serializer = KeySerializer(key)
        return JsonResponse(key_serializer.data)

    elif request.method == 'PUT':
        data = {"int_value": key.int_value + 1}
        key_serializer = KeySerializer(key, data=data)
        if key_serializer.is_valid():
            key_serializer.save()
            return JsonResponse(key_serializer.data)
        return JsonResponse(key_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        key.delete()
        delete_message = json.dumps({'message': 'The key was deleted successfully!'})
        return JsonResponse(delete_message, safe=False, status=status.HTTP_204_NO_CONTENT)




@api_view(['GET', 'DELETE'])
def dogs_list(request):
    if request.method == 'GET':
        dogs = DogPhoto.objects.all()
        dog_photo_serializer = DogPhotoSerializer(dogs, many=True)
        return JsonResponse(dog_photo_serializer.data, safe=False, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        count = DogPhoto.objects.all().delete()
        delete_message = json.dumps({'message': 'All Dog Photos were deleted successfully!'})
        return JsonResponse(delete_message, safe=False, status=status.HTTP_204_NO_CONTENT)




def get_image_data(dog_photo_link):
    url = f'https://ik.imagekit.io/rfxlfa3n0/{dog_photo_link}'
    imagekit = ImageKit(
    private_key = os.environ["PRIVATE_KEY"],
    public_key = os.environ["PUBLIC_KEY"],
    url_endpoint = f'https://ik.imagekit.io/rfxlfa3n0/{dog_photo_link}'
    )
    get_metadata = imagekit.get_remote_file_url_metadata(url)
    return get_metadata.response_metadata.raw




@api_view(['GET'])
def populate_dog_photos(request):
    idx = 0
    while idx < 24:
        dog_photo = requests.get('https://dog.ceo/api/breeds/image/random').json()
        start = dog_photo["message"].index("breed") + 7
        end = dog_photo["message"].find("/", start)
        newStr = dog_photo["message"][start:end]
        data = newStr.split("-")
        jpeg = dog_photo["message"].index(".jpg")
        unique_id = dog_photo["message"][end+1:jpeg]
        sub_breed = ""
        metadata = get_image_data(dog_photo["message"])
        if len(data) > 1:
            sub_breed = data[1]
        else: sub_breed = data[0]
        new_dog = {
            "breed": data[0],
            "sub_breed": sub_breed,
            "original_url":  f'{dog_photo["message"]}',
            "transformed_url": f'https://ik.imagekit.io/rfxlfa3n0/tr:ot-Dog%20Breed%20{data[0]},ots-45,otbg-white/{dog_photo["message"]}',
            "unique_photo_id": unique_id,
            "metadata": metadata
        }
        if DogPhoto.objects.filter(unique_photo_id=unique_id).exists():
            idx -= 1
        else:
            idx += 1
            dog = DogPhoto(**new_dog)
            dog.save()
    dogs = DogPhoto.objects.all()
    dog_photo_serializer = DogPhotoSerializer(dogs, many=True)
    return JsonResponse(dog_photo_serializer.data, safe=False, status=status.HTTP_200_OK)




@api_view(['GET', 'DELETE'])
def dog_photo_detail_with_transformed_photo(request, pk):
    try:
        dog_photo = DogPhoto.objects.get(pk=pk)
    except DogPhoto.DoesNotExist:
        message = json.dumps({'message': 'The dog photo does not exist'})
        return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        dog_photo_serializer = DogPhotoSerializer(dog_photo)
        return JsonResponse(dog_photo_serializer.data)

    elif request.method == 'DELETE':
        dog_photo.delete()
        delete_message = json.dumps({'message': 'Doggie Photo was deleted successfully!'})
        return JsonResponse(delete_message, safe=False, status=status.HTTP_204_NO_CONTENT)
