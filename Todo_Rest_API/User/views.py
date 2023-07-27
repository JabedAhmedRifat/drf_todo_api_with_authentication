from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import *

from knox.auth import TokenAuthentication
# Create your views here.

class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            user = serializer.save()
        return Response({
            'token':AuthToken.objects.create(user)[1]
        })
            
class LoginApi(generics.GenericAPIView):
    serializer_class=LoginUserSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception =True)
        if serializer.is_valid():
            user = serializer.validated_data
            return Response({
                'user':UserSerializer(user, context=self.get_serializer_context()).data,'token':AuthToken.objects.create(user)[1]})
            
            
class UserAPI(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class=UserSerializer
    def get_object(self):
        return self.request.user
    