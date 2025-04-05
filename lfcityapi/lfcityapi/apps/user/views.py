from rest_framework.generics import CreateAPIView

from .models import User
from .serializers import UserCreateModelSerializer

# Create your views here.
class UserRegisterAPIView(CreateAPIView):
    serializer_class = UserCreateModelSerializer
    authentication_classes = ()
    queryset = User.objects.all()