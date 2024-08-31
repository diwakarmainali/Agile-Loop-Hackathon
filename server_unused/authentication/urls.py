from django.urls import path
from .views import RegisterView, MyTokenObtainPairView ,LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
