from django.urls import path
from .views import ItemCreateView, ItemRetrieveView, ItemUpdateView, ItemDeleteView,ItemListView

urlpatterns = [
    path('additems/', ItemCreateView.as_view(), name='item-create'),
    path('items/', ItemListView.as_view(), name='item-list'),
    path('items/<int:pk>/', ItemRetrieveView.as_view(), name='item-detail'),
    path('items/<int:pk>/update/', ItemUpdateView.as_view(), name='item-update'),
    path('items/<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),
]
