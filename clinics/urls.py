from django.urls import path
from .views import *

app_name = "clinics"

urlpatterns = [
	path('', homePage, name='home'),
	path('login', login),
	path('profile/', profile, name='profile'),
	path('addFrequency/', addFrequency, name="addFrequency"),
	path('thanks/', thanks, name="thanks"),
	path('erorr_page/', erorr_page, name='erorr_page'),
	path('admin/', admin, name='admin'),
	path('m_report/', m_report, name='m_report'),
	path('daily_record/', daily_record, name='daily_record'),
	path('recordManage/', recordManage, name='recordManage'),
	path('viewRecords/', DailyReportListView, name='allRecords'),
	path('add_edit_frequency/', add_edit_frequency, name='add_edit_frequency'),
	path('get_cat_vals/', get_cat_vals.as_view(), name='get_cat_vals'),
	
	path('update_record/', update_record.as_view(), name='update_record'),
	
	
	# path('PrintLetter/<int:pk>/',PrintLetter, name='PrintLetter')
	# path('makeAuto', makeAuto) # use to make some actions
]
