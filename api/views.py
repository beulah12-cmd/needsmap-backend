from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import NeedPost, Response
from .serializers import (
    UserSerializer,
    NeedPostSerializer,
    ResponseSerializer,
)

User = get_user_model()


class RegisterUser(APIView):
    """
    API view for user registration.
    """
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new user.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Use create_user to handle password hashing securely
                user = User.objects.create_user(
                    username=serializer.validated_data['username'],
                    email=serializer.validated_data['email'],
                    password=request.data.get('password')
                )
                return Response(
                    UserSerializer(user).data,
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                # Catch potential errors during user creation
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class NeedPostListCreate(generics.ListCreateAPIView):
    """
    API view to list all need posts or create a new one.
    """
    queryset = NeedPost.objects.all()
    serializer_class = NeedPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """
        Saves the new need post, associating it with the current authenticated user.
        """
        serializer.save(user=self.request.user)


class NeedPostRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific need post.
    """
    queryset = NeedPost.objects.all()
    serializer_class = NeedPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ResponseCreate(generics.CreateAPIView):
    """
    API view to create a new response for a specific need post.
    """
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Saves the new response, associating it with the correct need post
        and the current authenticated user.
        """
        try:
            need_post_pk = self.kwargs.get('pk')
            need_post = NeedPost.objects.get(pk=need_post_pk)
            serializer.save(user=self.request.user, need_post=need_post)
        except NeedPost.DoesNotExist:
            # Handle case where the need post doesn't exist
            return Response(
                {"error": "Need post not found."},
                status=status.HTTP_404_NOT_FOUND
            )