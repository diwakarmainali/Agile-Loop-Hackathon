from django.urls import path
from ui.views import landingPage

urlpatterns = [
    path('',landingPage,name='landing')
]
