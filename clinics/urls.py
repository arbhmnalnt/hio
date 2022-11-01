from django.urls import path
from .views import *

app_name = "clinics"

urlpatterns = [
	path('', home),
	path('profile/', profile, name='profile'),
	path('addFrequency/', addFrequency, name="addFrequency"),
	path('thanks/', thanks, name="thanks"),
	path('erorr_page/', erorr_page, name='erorr_page'),
	path('generate_m_report/', generate_m_report, name='generate_m_report'),
# 	path('m_report/', m_report, name='m_report'),
	# path('PrintLetter/<int:pk>/',PrintLetter, name='PrintLetter')
]
