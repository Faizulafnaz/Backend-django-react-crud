from django.urls import path
from . import views
from rest_framework.response import Response

from rest_framework_simplejwt.views import (
  
    TokenRefreshView,
)

from .views import MyTokenObtainPairView, UserList, UserDetails

urlpatterns = [
    path('', views.getRoutes),
    path('notes/', views.getNotes),
    path('profile/', views.getProfile),
    path('updateprofile/', views.updateProfile),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-list/',UserList.as_view(),name='user_list'),
    path('user-detail/<int:id>/',UserDetails.as_view(),name='user_details'),
]
