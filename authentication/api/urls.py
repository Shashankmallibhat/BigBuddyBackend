from django.urls import path, include

from authentication.api.views import SignINView, SignOUTView, SignUPView, ProfileView


urlpatterns = [
    path('signup/',SignUPView.as_view(), name = 'register'),
    path('signin/',SignINView.as_view(), name = 'register'),
    path('signout/',SignOUTView.as_view(), name = 'register'),
    path('profile/',ProfileView.as_view(), name = 'profile'),
]