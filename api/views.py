from rest_framework  import viewsets , status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializer import MealSerializer , RaterSerializer , UserSerializer
from .models import Meal , Rater
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated , IsAdminUser ,AllowAny, IsAuthenticatedOrReadOnly



# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    
    @action(methods=['post'], detail=True)
    def rate_meal(self, request, pk=None):
        if 'num_stars' in request.data:
            try:
                meal = Meal.objects.get(pk=pk)
                user_name = request.data['username']
                stars = request.data['num_stars']
                user = User.objects.get(username=user_name)
                
                try:
                    # Update
                    rating = Rater.objects.get(user=user, meal=meal)
                    rating.num_stars = stars
                    rating.save()
                    serializer = RaterSerializer(rating)
                    json = {
                        'message': 'Meal rating updated',
                        'result': serializer.data
                    }
                    return Response(json, status=status.HTTP_202_ACCEPTED)
                except Rater.DoesNotExist:
                    # Create
                    rating = Rater.objects.create(
                        num_stars=stars,
                        meal=meal,
                        user=user,
                    )
                    serializer = RaterSerializer(rating)
                    json = {
                        'message': 'Meal rating created',
                        'result': serializer.data
                    }
                    return Response(json, status=status.HTTP_201_CREATED)
            except Meal.DoesNotExist:
                return Response({'message': 'Meal not found'}, status=status.HTTP_404_NOT_FOUND)
            except User.DoesNotExist:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            json = {
                'message': 'Stars not provided'
            }
            return Response(json, status=status.HTTP_400_BAD_REQUEST)
            
    
class RaterViewSet(viewsets.ModelViewSet):
    queryset = Rater.objects.all()
    serializer_class = RaterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]