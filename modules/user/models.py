from django.db import models
from django_petra.models import Extensions

class User(Extensions):
  name = models.CharField(max_length=2000)
  email = models.CharField(max_length=2000)
  password = models.CharField(max_length=2000)
  username = models.CharField(max_length=1000)
  is_active = models.BooleanField(default=1)
  
  class Meta:
    db_table = 'the_users'
  