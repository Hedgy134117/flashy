from django.urls import path
from cards import views

urlpatterns = [
    path('sets/', views.SetList.as_view()),
    path('sets/<int:pk>/', views.CardList.as_view())
]