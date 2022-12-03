from django.urls import path
from .views import *

app_name = "services"

urlpatterns = [
	path('', home, name="home"),
	path('new/', NewLetter, name="NewLetter"),
	path('PrintLetter/<int:pk>/',PrintLetter, name='PrintLetter'),
	path('EditLetter/<int:pk>/',EditLetter, name='EditLetter'),
	path('cancelLetter/<int:pk>/',cancelLetter.as_view(), name='cancelLetter'),
	path('ServicePriceCreate/', ServicePriceCreateView.as_view(), name='film_create'),
	path('ServicePriceListView/', ServicePriceListView.as_view(), name='all'),

]
