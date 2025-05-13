from .views import MenuView, EatingItemDetailView
from django.urls import path


app_name = 'main'

urlpatterns = [
    path('', MenuView.as_view(), name='menu'),
    path('item/<slug:slug>/', EatingItemDetailView.as_view(),
         name='eating_item_detail')
    
]
