from django.utils.timezone import now
from .models import User
from django_petra.petra_core import ModelSerializer
from django_petra.raw_query.helpers import exclude_fields
from django_petra.petra_core import serializers

class UserSerializer(ModelSerializer):
    
    class Meta:
        model = User
        #fields = ['name', 'days_since_joined']
        fields = '__all__'

    # update existing value
    def to_representation(self, instance):
        # Modify the representation of the object
        representation = super().to_representation(instance)
        representation = exclude_fields(representation, [ 'password'])
        return representation
        
    def get_days_since_joined(self, obj):
        return (now() - obj.created).days
