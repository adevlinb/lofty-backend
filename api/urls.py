from django.urls import path
from . import views

urlpatterns = [
    path('api/keys/', views.keys_list),
    path('api/keys/<int:pk>/', views.key_detail),
    path('api/keys/slug/<slug:slug>/', views.key_slug_detail),
    path('api/dogs/', views.dogs_list),
    path('api/dogs/populate/', views.populate_dog_photos),
    path('api/dogs/<int:pk>/', views.dog_photo_detail_with_transformed_photo),
]
