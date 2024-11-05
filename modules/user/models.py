from django.db import models
from django_petra.models import Extensions

class User(Extensions):
  name = models.CharField(max_length=100, null=False, blank=False)
  email = models.CharField(max_length=100, null=False, blank=False)
  password = models.CharField(max_length=100, null=False, blank=False)
  username = models.CharField(max_length=100, null=True, blank=True)
  is_active = models.BooleanField(default=True)
  
  class Meta:
    db_table = 'the_users'
  