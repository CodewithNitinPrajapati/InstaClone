from django.db import models
from user.managers import CustomUserManager
from django.contrib.auth.models import AbstractUser

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('None', 'Prefer not to say.'),
]

class User(AbstractUser):
    picture = models.ImageField(upload_to='photos',null=False,blank=False)
    full_name = models.CharField(max_length=100,default='DEFAULT VALUE')
    email = models.EmailField(max_length=254 ,unique =True)
    
    # Optional fields
    bio = models.TextField(null=True , blank=True)
    website = models.URLField(null=True,blank=True, max_length=200)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    is_private_account = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name','username']

    first_name = None
    last_name = None

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

    @property
    def follower_count(self):
        count = self.follow_followed.count()
        return count

    @property
    def following_count(self):
        count = self.follow_follower.count()
        return count

    @property
    def posts_count(self):
        count = self.post_set.count()
        return count
