from django.urls import path, include

from student.api.views import StudentClassesView

urlpatterns = [
    path("class/",StudentClassesView.as_view(),name="Student classes")
]