from django.urls import path
from .views import *

app_name = "clinics"

urlpatterns = [
	path('', home),
	path('login', login),
	path('profile/', profile, name='profile'),
	path('addFrequency/', addFrequency, name="addFrequency"),
	path('thanks/', thanks, name="thanks"),
	path('erorr_page/', erorr_page, name='erorr_page'),
	path('admin/', admin, name='admin'),
	path('m_report/', m_report, name='m_report'),
	path('daily_record/', daily_record, name='daily_record'),

	# path('PrintLetter/<int:pk>/',PrintLetter, name='PrintLetter')
]
