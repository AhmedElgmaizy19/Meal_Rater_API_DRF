from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator , MaxValueValidator


# Create your models here.
class Meal(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=350)
    
    def no_of_rating(self):
        ratings = Rater.objects.filter(meal=self)
        return len(ratings)

    def avg_rating(self):
        sum = 0
        rating = Rater.objects.filter(meal=self)
        for rate in rating:
            sum+=rate.num_stars
            
        if len(rating) > 0:
            return sum / len(rating)
        
    
    def __str__(self):
        return  self.title


class Rater(models.Model):
    num_stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User,  on_delete=models.CASCADE)

    def __str__(self):
        return  str(self.meal)

    
    class Meta:
        unique_together = (('user','meal'),)
        indexes = [
            models.Index(fields=['user', 'meal'])
        ]
