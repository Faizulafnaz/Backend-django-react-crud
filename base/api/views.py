from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.views import APIView
from rest_framework.generics import  ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser

from .serializers import NoteSerializer, UserRegister, ProfileSerializer
from base.models import Note, UserProfile

from django.contrib.auth.models import User

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['is_superuser'] = user.is_superuser

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class Register(APIView):

    def post(self, request, format=None):
        serializer = UserRegister(data=request.data)
        data = {}
        if serializer.is_valid():
            account=serializer.save()
            data['response'] = 'registered'
            data['username'] = account.username
            data['email'] = account.email
        else:
            data=serializer.errors
        return Response(data)
    



    
@api_view(['GET'])
def getRoutes(request):
    routes = [
        'api/token',
        'api/token/refresh',
    ]
    return Response(routes)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getNotes(request):
    user = request.user
    notes = user.note_set.all()
    serializer = NoteSerializer(notes, many = True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):
  
    user = request.user
    profile = UserProfile.objects.get(user_id = user)
    serializer = ProfileSerializer(profile)
    data = serializer.data
   
    data['response'] = 'registered'
    data['username'] = user.username
    data['email'] = user.email
    return Response(data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def updateProfile(request):

    user = request.user
    profile = UserProfile.objects.get(user_id = user)
    print(request.data, 'p')
    if 'profile_img' in request.FILES:
        profile.profile_img = request.FILES['profile_img']
    serializer = ProfileSerializer(instance = profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        user.username = request.data.get('username', user.username)
        user.email = request.data.get('email', user.email)
        user.save()
        data['response'] = 'registered'
        data['username'] = user.username
        data['email'] = user.email
    else:
        data = serializer.errors
    return Response(data)

class UserList(ListCreateAPIView):
    queryset = User.objects.all().exclude(is_superuser=True)
    serializer_class = UserRegister
    filter_backends = [SearchFilter]
    search_fields = ['email', 'username']

class UserDetails(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegister
    lookup_field = 'id'