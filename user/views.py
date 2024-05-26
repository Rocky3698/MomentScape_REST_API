from django.contrib.auth import login, logout,authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer,UserLoginSerializer, UserSerializer,UserAddressSerializer
from rest_framework import permissions, status
from rest_framework.authentication import  TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from .models import UserAccount,UserAddress
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage, EmailMultiAlternatives


class UserRegisterView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(request.data)
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                current_site = get_current_site(request)
                # Prepare and send email
                confirmation_link = f"https://momentscape-rest-api.onrender.com/user/activate/{uid}/{token}/"  # Replace with your confirmation URL
                email_subject = 'Confirm your email'
                email_body = render_to_string('email.html', {'confirmation_link': confirmation_link})

                email = EmailMultiAlternatives(
                    email_subject, '', to=[user.email]
                )
                email.attach_alternative(email_body, "text/html")
                # send_email.send()
                email.send()

                return Response('Check your email for confirmation.', status=status.HTTP_201_CREATED)
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
                return Response({'error' : "Invalid Credential"},status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = UserAccount._default_manager.get(pk=uid)
    except(UserAccount.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('https://moment-scape.vercel.app/login')
    else:
        return redirect('https://moment-scape.vercel.app/registration')

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
    
    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'user': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserAddressUpdate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        try:
            user_address = UserAddress.objects.get(user=user)  
        except UserAddress.DoesNotExist:
            return Response({'detail': 'User address not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserAddressSerializer(user_address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'user': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        # return redirect('login')
        return Response({'success' : "logout successful"})