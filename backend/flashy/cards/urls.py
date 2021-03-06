from django.urls import path
from cards import views

urlpatterns = [
    path('sets/', views.SetList.as_view(), name='set-list'),
    path('sets/<int:pk>/', views.SetDetail.as_view(), name='set-detail'),
    path('sets/<int:pk>/cards/', views.CardList.as_view(), name='set-card-list'),
    path('cards/<int:pk>/', views.CardDetail.as_view(), name='card-detail'),
]