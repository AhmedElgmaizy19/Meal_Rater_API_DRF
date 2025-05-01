from django.urls import path , include
from rest_framework import routers
from .views import MealViewSet , RaterViewSet , UserViewSet

router = routers.DefaultRouter()

router.register('users',UserViewSet)
router.register('meals',MealViewSet)
router.register('rating',RaterViewSet)


urlpatterns = [
    path('',include(router.urls))
    
]
