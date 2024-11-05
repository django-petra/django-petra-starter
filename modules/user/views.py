from django_petra.petra_dto import petra_dto
from django_petra.petra_core import Response, ViewSet, status
from django_petra.paginate import paginate
from modules.user.models import User
from modules.user.serializer import UserSerializer
from modules.user.forms import AddUserForm
from modules.common.utils.password import generate_password_hash, compare_hashed_password
from modules.common.utils.jwt_utils import create_access_token, create_refresh_token, decode_token

class UserViewset(ViewSet):
  
  def get_permissions(self):
    from modules.user.permissions import Permissions
    the_permission_classes = Permissions()
    return the_permission_classes.get_permissions(self)
      
  def get_users(self, request):
    query = User
    query = query.objects.filter().order_by('-created')
    query = query.all()
    data = paginate(request=request, queryset=query, serializer_class=UserSerializer, per_page=4, wrap='users')
    
    return Response(data, status=status.HTTP_200_OK)
    
  @petra_dto(form_class=AddUserForm)
  def registration(self, request, form):
        # Process valid data
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        hashed_password = generate_password_hash(password)
        
        # Create new user
        user = User.objects.create(
            name=name,
            email=email,
            password=hashed_password
        )

        # Serialize the user object
        serializer = UserSerializer(user)
        return Response({
            'message': 'Registration successful',
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)

  def login(self, request):
    from django_petra.helpers import get_request_data
    
    email = get_request_data(request, 'email')
    password = get_request_data(request, 'password')
    
    if not email or not password:
        return Response({
            'message': 'Email/username and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Try to find user by email or username
        user = (User.objects.filter(email=email) | User.objects.filter(username=email)).first()
        if not user:
            raise User.DoesNotExist
    except User.DoesNotExist:
        return Response({
            'message': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Verify password
    if not compare_hashed_password(password, user.password):
        return Response({
            'message': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Create token payload
    token_payload = {
        'user_id': str(user.uuid),
        'name': user.name,
        'email': user.email,
        'password': str(user.password)
    }
    
    # Generate tokens
    access_token = create_access_token(token_payload)
    refresh_token = create_refresh_token(token_payload)
    
    return Response({
        'message': 'Login successful',
        'user': UserSerializer(user).data,
        'access_token': access_token,
        'refresh_token': refresh_token
    }, status=status.HTTP_200_OK)
  
      
  def the_query_check(self, request):
    from django_petra.helpers import get_request_data, get_all_request_data, get_request_headers
    
    data = get_all_request_data(request)
    the_image = get_request_data(request, 'the_image')
    headers = get_request_headers(request)



    response = {
        'status': 'success',
        'data': {
            'request_data': data.get('the_image').name,
            'image': the_image.name,
            'user': request.the_user,
            'is_auth': request.is_auth,
        },
        'headers': headers
    }
    
    return Response(response, status=status.HTTP_200_OK)


