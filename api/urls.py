from django.urls import path, include
from django.conf.urls import url

from . import views

urlpatterns = [
    url('auth/', include('rest_framework.urls')),
    path('pools/', views.PoolViewSet.as_view()),
    path('pools/<int:pk>/', views.PoolView.as_view()),
    path('answers/', views.AnswerView.as_view()),
]
