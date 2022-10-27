from django.urls import path
from .views import *

app_name = "clinics"

urlpatterns = [
	path('', home),
	path('profile/', profile, name='profile'),
	path('addFrequency/', addFrequency, name="addFrequency"),
	path('thanks/', thanks, name="thanks"),
	path('erorr_page/', erorr_page, name='erorr_page'),
	# path('PrintLetter/<int:pk>/',PrintLetter, name='PrintLetter')
]
