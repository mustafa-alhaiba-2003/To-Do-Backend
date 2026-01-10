from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.serializers import RegisterSerializer, LoginSerializer, UserSerializer, MyProfileSerializer
from apps.user.services import JWTService
from apps.user.models import User

class AuthViewSet(viewsets.GenericViewSet):
    """
    ViewSet for user authentication operations (register, login, logout)
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        """
        Register a new user and return JWT tokens in cookies
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            user_serializer = UserSerializer(user)
            response = Response({
                'message': 'User registered successfully',
                'user': user_serializer.data
            }, status=status.HTTP_201_CREATED)
            
            response = JWTService.set_jwt_cookies(response, access_token, refresh_token)
            
            return response
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        """
        Login user and return JWT tokens in cookies
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            user_serializer = UserSerializer(user)
            response = Response({
                'message': 'Login successful',
                'user': user_serializer.data
            }, status=status.HTTP_200_OK)
            
            response = JWTService.set_jwt_cookies(response, access_token, refresh_token)
            
            return response
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='logout', permission_classes=[IsAuthenticated])
    def logout(self, request):
        """
        Logout user by clearing JWT cookies
        """
        response = Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
        
        response = JWTService.clear_jwt_cookies(response)
        
        return response
    
    @action(detail=False, methods=['get'], url_path='me', permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Get current authenticated user details
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='refresh', permission_classes=[AllowAny])
    def refresh(self, request):
        """
        Refresh JWT tokens using the refresh token in the cookie
        """
        refresh_token = request.COOKIES.get('refresh')
        if not refresh_token:
            return Response({'detail': 'Refresh token not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            new_refresh_token = str(refresh)
            user = User.objects.get(id=refresh['user_id'])
        except Exception as e:
            return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_401_UNAUTHORIZED)
        user_serializer = UserSerializer(user)
        response = Response({
            'message': 'Token refreshed successfully',
            'user': user_serializer.data
        }, status=status.HTTP_200_OK)
        response = JWTService.set_jwt_cookies(response, new_access_token, new_refresh_token)
        return response


class MyProfileViewSet(viewsets.GenericViewSet):
    """
    ViewSet for managing user profile (get and update)
    """
    serializer_class = MyProfileSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get' , 'patch','put'], url_path='me')
    def get_profile(self, request):
        """
        Get current user's profile information
        """
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method in ["PATCH","PUT"]:
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['patch', 'put'])
    def update_profile(self, request):
        """
        Update current user's profile information
        """
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
