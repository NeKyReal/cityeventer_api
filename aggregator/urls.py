from django.urls import path
from . import views

urlpatterns = [
    path('seatgeek/events/', views.SeatGeekEvents.as_view(), name='seatgeek-events'),
    # Другие эндпоинты можно добавить здесь
]
