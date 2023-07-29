from django.urls import path
from .views import *

app_name = "services"

urlpatterns = [
	path('', home, name="home"),
	path('new/', NewLetter, name="NewLetter"),
	path('PrintLetter/<int:pk>/',PrintLetter, name='PrintLetter'),
	#
	path('getDesc/', getDesc),
# 	path('getDesc/<str:q>', getDesc),
	#
	path('editLetter/<int:pk>/',EditLetter.as_view(), name='EditLetter'),
	path('cancelLetter/<int:pk>/',cancelLetter.as_view(), name='cancelLetter'),
	path('get_letter_serial/<int:pk>/',get_letter_serial, name='get_letter_serial'),
	path('ServicePriceCreate/', ServicePriceCreateView.as_view(), name='film_create'),
	path('ServicePriceListView/', ServicePriceListView.as_view(), name='all'),
	path('servicePricesCalc/', servicePricesCalc.as_view()),

]
