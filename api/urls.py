from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path('posts/', views.NeedPostListCreate.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.NeedPostRetrieveUpdateDestroy.as_view(), name='post-detail'),
    path('posts/<int:pk>/respond/', views.ResponseCreate.as_view(), name='post-respond'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]