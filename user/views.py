from django.contrib.auth import login, logout,authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer,UserLoginSerializer, UserSerializer
from rest_framework import permissions, status
from rest_framework.authentication import  TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from .models import UserAccount
class UserRegisterView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(request.data)
            if user:
                token = Token.objects.create(user=user)
                return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginApiView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data = self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(username= username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                print(token)
                login(request, user)
                return Response({'token' : token.key, 'user_id' : user.id})
            else:
                return Response({'error' : "Invalid Credential"})
        return Response(serializer.errors)

class Author(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.request.query_params.get('author_id')
        if author_id:
            queryset = queryset.filter(id=author_id)
        return queryset

class UserView(APIView):
    authentication_classes = [ TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        print(request.user)
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)

class UserLogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        # return redirect('login')
        return Response({'success' : "logout successful"})