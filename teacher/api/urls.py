from django.urls import path, include

from teacher.api.views import ClassRecordingView, ClassRoomDetailView, ClassRoomListView,ClassNotesView

urlpatterns = [
    path('class/', ClassRoomListView.as_view(), name = 'class'),
    path('class/<str:className>/', ClassRoomDetailView.as_view(), name = 'class'),
    path('class/notes/<str:className>/', ClassNotesView.as_view(), name = 'class notes'),
    path('class/recordings/<str:className>/', ClassRecordingView.as_view(), name = 'class recordings'),
]