from django.urls import path
from .views import *

urlpatterns = [
	path('', home),
	path('new/', NewLetter),
	path('PrintLetter/<int:pk>/',PrintLetter, name='PrintLetter')
]
