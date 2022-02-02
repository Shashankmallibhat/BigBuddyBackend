from django.urls import path, include

from student.api.views import StudentClassesView, StudentWishlistView

urlpatterns = [
    path("class/",StudentClassesView.as_view(),name="Student classes"),
    path("wishlist/",StudentWishlistView.as_view(),name="")
]