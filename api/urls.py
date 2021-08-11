from django.urls import path, include
from rest_framework import routers
from api.views import TestViewSet, QuestionViewSet, TestTotalViewSet, RetrieveUpdateDestroyAPIView, TestFirstThreeViewSet

router = routers.DefaultRouter()
#router.register(r'dishes', TestViewSet)
#router.register(r'ingredients', QuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tests/', TestViewSet.as_view()),
    path('questions/', QuestionViewSet.as_view()),
    path('total/', TestTotalViewSet.as_view()),
    path('total_three/', TestFirstThreeViewSet.as_view()),
    path('tests/<int:pk>/', RetrieveUpdateDestroyAPIView.as_view()),
    path('questions/<int:pk>/', RetrieveUpdateDestroyAPIView.as_view()),
    path('api-auth/',
         include('rest_framework.urls', namespace='rest_framework')),
]
