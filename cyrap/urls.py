from django.urls import path
from .views import *

urlpatterns = [
    path("books/", BookApiView.as_view(), name="books"),
    path("books/<int:pk>/", BookApiView.as_view(), name="books"),
    path('categories/', CategoryApiView.as_view()),
    path('categories/<int:pk>/', CategoryApiView.as_view()),
    path('lending_record/', LendingRecordAPIView.as_view()),
    path('lending_record/<int:pk>', LendingRecordAPIView.as_view()),
]