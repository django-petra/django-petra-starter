from django_petra.petra_dto import petra_dto
from django_petra.petra_core import Response, ViewSet, status
from django_petra.paginate import paginate
from modules.user.models import User
from modules.user.serializer import UserSerializer
from modules.user.forms import AddUserForm


class UserViewset(ViewSet):
  def get_users(self, request):
    query = User
    query = query.objects.filter().order_by('-created')
    query = query.all()
    data = paginate(request=request, queryset=query, serializer_class=UserSerializer, per_page=4, wrap='users')
    
    return Response(data, status=status.HTTP_200_OK)
    
  @petra_dto(form_class=AddUserForm)
  def add_user(self, request, form):
        # Process valid data
        name = form.cleaned_data['name']
        age = form.cleaned_data['age']
        phone = form.cleaned_data['phone']

        # Perform further actions...
        user = User()
        user.name = name
        user.age = age
        user.phone = phone
        user.save()

        # Retrieve the user object after saving it
        user = User.objects.get(id=user.id)

        # Serialize the user object (you should have a serializer for your User model)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

