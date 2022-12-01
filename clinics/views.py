import json
from logging import exception
from sre_parse import CATEGORIES
from unicodedata import category
from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect, render
from rest_framework.response import Response
from django.urls import is_valid_path, reverse
from django.views.generic.list import ListView
from rest_framework.views import APIView
# from symbol import pass_stmt
from .forms import *
from .models import *
from services.models import *
from django.contrib.auth.decorators import login_required
from datetime import *
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date, parse_datetime



# print(f"today date => ", today_date)
class update_record(APIView):
    def get(self, request):
        day = request.GET.get('dayDate', '-')
        dailyReportId = request.GET.get('dailyReportId', '-')
        categoryId  = request.GET.get('catId', '-')
        user_clinic = request.user.employee.area
        specialist  = request.GET.get('specialist', '-')
        advisory    = request.GET.get('advisory', '-')
        num         = request.GET.get('num', 0)
        papers      = request.GET.get('papers', 0)
        childPapers = request.GET.get('childPapers', 0)
        # `specialist=${specialist_val}&advisory=${advisory}&num=${num}&papers=${papers}`
        if dailyReportId =="-" or day == "-":
            # print(f"erorr here dailyReportId => ${dailyReportId} // day => ${day}")
            data = {'msg':'erorr'}
        else:
            cat = Category.objects.get(pk=categoryId)
            categorySlug = cat.specific.name
            ayadaSlug    = user_clinic.name
            dailyReport = DailyReport.objects.update_or_create(
                pk=dailyReportId,
                defaults={
                    "day":day,"category":cat,"ayada":user_clinic,
                    "specialist":specialist,"advisory":advisory,"num":num,"papers":papers,"childPapers":childPapers,
                    "categorySlug":categorySlug, "ayadaSlug":ayadaSlug
                },
            )
            # print(f"=============\n dailyReport => {dailyReport}")

            data = {'msg':'done'}
        return Response(data)

class get_cat_vals(APIView):
    def get(self, request):
        
        catId = request.GET.get('catId', '-')
        dailyReportId = request.GET.get('dailyReportId', '-')
        # print('catId => ', catId)
        if dailyReportId =="-":
            print("erorr here ")
        else:
            dailyReport = DailyReport.objects.get(pk=dailyReportId)
            specialist = dailyReport.specialist
            advisory = dailyReport.advisory
            papers = dailyReport.papers
            childPapers = dailyReport.childPapers
        data = {'specialist':specialist, 'advisory': advisory, 'papers':papers, 'childPapers':childPapers, 'catId':catId}
        return Response(data)

@login_required
def add_edit_frequency(request):
    today_date = datetime.now().date()
    date = request.GET.get('date', today_date)
    user_clinic = request.user.employee.area
    clinicName = user_clinic.name
    isRecordCount = DailyReport.objects.filter(day=date, ayada=user_clinic).count()
    if isRecordCount ==0:
        is_prev_values = "no"
        return redirect(f'/clinics/addFrequency/?date={date}')
    else:
        daily_records = DailyReport.objects.filter(day=date, ayada=user_clinic)
        is_prev_values = "yes"
    daily_record_id_list = [d.id for d in daily_records]
    print(f"daily_record_id_list => {daily_record_id_list}")
    categories1 = list(Category.objects.filter(ayada=user_clinic))
    categories_obj = [cat.id for cat in categories1]
    categories = zip(categories1, categories_obj, daily_record_id_list)
    ctx = {'date':date, 'is_prev_values':is_prev_values, 'clinicName':clinicName,
    'categories':categories}
    return render(request, './clinics/add_edit_frequency.html', ctx)

def DailyReportListView(request):
    user_clinic = request.user.employee.area
    cats = Category.objects.filter(ayada=user_clinic)
    catList = [cat.specific.name for cat in cats]
    dateFrom =request.GET.get('dateFrom', '0')
    dateTo = request.GET.get('dateTo', '0')
    
    if dateFrom != '0' and dateTo != '0':
        dateFrom = parse_date(dateFrom)
        dateTo = parse_date(dateTo)
        DailyReports = DailyReport.objects.filter(day__range=[dateFrom, dateTo], ayada=user_clinic).order_by('day')
    else:
        DailyReports = DailyReport.objects.filter(ayada=user_clinic).order_by('day')
    counter = DailyReports.count()
    if counter == 0:
        msg = 'لا يوجد ادخال فى التاريخ المحدد'
    else:
        msg=''
    ctx = {'DailyReports':DailyReports, 'msg':msg, 'catList':catList}
    
    return render(request, './clinics/DailyReport_list.html', ctx)

@login_required
def homePage(request):
    user_clinic = request.user.employee.area
    clinicName = user_clinic.name
    print("clinicName => ", clinicName)
    if 'group' in request.session:
        userGroup = request.session['group']
    else:
        return redirect('/clinics/login')

    if request.user.groups.filter(name="clinic_member"):
        request.session['group'] = "clinic_member"
    else:
        return redirect('/clinics/login')
    if clinicName == "الكل":
        clinicName = "العيادات"
    ctx = {"clinicName":clinicName}
    return render(request, './clinics/homePage.html' , ctx)

def recordManage(request):
    month = datetime.now().month
    print("month => ", month)

    ctx = {'month':month}
    return render(request, 'clinics/record_management.html', ctx)
    
@csrf_exempt
def login(request):
    message = ''
    if request.method == 'POST':
        username=request.POST['username']
        password = request.POST['password']
        user = authenticate(
            username=username,
            password=password
        )
        message = 'post'
        if user is not None:
            auth_login(request, user)
            return redirect('/clinics/profile/')
            # message = f'Hello {user.username}! You have been logged in'
        else:
            message = 'خطأ بإسم المستخدم أو كلمة السر'
    else:
        message = ''
    return render(request, 'clinics/login.html', context={'message': message})

# الفترة المسائية عيادتان
def m_report(request):
    today_date = datetime.now().date()
    month = datetime.now().month
    date = request.POST.get('date', today_date)
    ayada1 = Ayadat.objects.get(pk=16)
    ayada2 = Ayadat.objects.get(pk=17)
    cats1 = list(Category.objects.filter(ayada=ayada1))
    cats2 = Category.objects.filter(ayada=ayada2)
    stCats = cats2
    dailyReport1 = getNums(stCats, cats1)
    dailyReport2 = getNums(stCats, cats2)

    totalNum1 = getTotal(cats1, date)
    totalNum2 = getTotal(cats1, date)
    ctx = {'ayada1':ayada1,'ayada2':ayada2,'cats1':cats1 , 'cats2':cats2, 'date':date, 'totalNum1':totalNum1, 'totalNum2':totalNum2,
    'dailyReport1': dailyReport1, 'dailyReport2': dailyReport1}
    return render(request, './clinics/mreport.html', ctx)


def daily_record(request):
    user = request.user
    if user.groups.filter(name="clinic_supervisor"):
        pass
    else:
        msg = "لا تملك صلاحية الوصول لهذه الصفحة , الرجاء التواص مع المسؤول"
        return redirect(f'/clinics/erorr_page?msg={msg}')
    records = DailyReportHistory.objects.all().order_by('-day')
    ctx = {'records':records}
    return render(request, './clinics/daily_record.html', ctx)


@login_required
def admin(request):
    user = request.user
    if user.groups.filter(name="clinic_admin"):
        ayadat = Ayadat.objects.all()
        ctx={'ayadat':ayadat}
    else:
        msg = "لا تملك صلاحية الوصول لهذه الصفحة , الرجاء التواص مع المسؤول"
        return redirect(f'/clinics/erorr_page?msg={msg}')

    return render(request, './clinics/admin_clinic.html', ctx)

def erorr_page(request):
    default_msg = "حدثت مشكلة الرجاء التواصل مع المسؤول"
    msg=request.GET.get('msg' , default_msg)
    ctx = {"msg":msg}
    return render(request, './clinics/erorr.html', ctx)

def thanks(request):
    user_clinic = request.user.employee.area
    clinicName = user_clinic.name
    ctx = {"clinicName":clinicName}
    return render(request, './clinics/thanks.html', ctx)



@login_required
def addFrequency(request):
    today_date = datetime.now().date()
    month = datetime.now().month
    user_clinic = request.user.employee.area
    clinicName = user_clinic.name
    print(f"user {request.user.username} is start visiting add frequncy page at {datetime.now()}")
    try:
        userGroup = request.session['group']
        if request.user.groups.filter(name="clinic_member"):
            request.session['group'] = "clinic_member"
        else:
            return redirect('/clinics/login')
    except Exception as e:
        print(f"exception {e}")
        msg = e
        return redirect(f'/accounts/login')
    # check if user previously recorded or this is first time
    
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    print(f"today_date => {today_date}")
    prev_record = DailyReportHistory.objects.filter(day=today_date, user=user).count()
    if request.method == 'GET':
        if prev_record >0:
            pass
        else:
            pass
    if clinicName == "الكل":
        clinicName = "العيادات"
        Categories_obj = Category.objects.filter(ayada=Ayadat.objects.get(pk=1))
    else :
        Categories_obj = Category.objects.filter(ayada=user_clinic)
    print(f"user {request.user.username} is pressing save to the record at {datetime.now()}")
    if request.method == 'POST':
        if prev_record >0:
            pass
        else:
            print(f"user {request.user.username} is pressing save to the record at {datetime.now()}")
            record = DailyReportHistory.objects.update_or_create(
                day=today_date, user=user,
                defaults={"day":today_date, "user":user}
                )
        if 'frequency_form' in request.POST:
            frequency_form = request.POST
            try:
                formDict = frequency_form.dict()
                status = addDataToDailyReport(formDict,user_clinic)

                return redirect('/clinics/thanks')
            except Exception as e:
                print(f"exception {e}")
                msg = e
                return redirect(f'/clinics/erorr_page?msg={msg}')
    else:
        pass
    categories = Categories_obj
    ctx = {"clinicName":clinicName, "categories":categories, "userGroup":userGroup}
    return render(request, './clinics/add_frequency.html', ctx)

###  groups
# 	admin_all
# 	clinic_admin
# 	clinic_member
# 	clinic_supervisor
# 	services_member
@login_required
def profile(request):
    user = request.user
    request.session.setdefault('group', False)
    if user.groups.filter(name="admin_all"):
        request.session['group'] = "admin_all"
        return redirect('/clinics/admin')

    elif user.groups.filter(name="clinic_admin"):
        request.session['group'] = "clinic_admin"
        print("admin here => ")
        return redirect('/clinics/admin')

    elif user.groups.filter(name="clinic_supervisor"):
        request.session['group'] = "clinic_supervisor"
        return redirect('/clinics/')

    elif user.groups.filter(name="clinic_member"):
        request.session['group'] = "clinic_member"
        return redirect('/clinics/')

    elif user.groups.filter(name="services_member"):
        return redirect('/services')

    else:
        request.session['group'] = "else"
        msg="user has no group"
        return redirect(f'/clinics/erorr_page?={msg}')

#=================== FUNCTIONS PART ============


def getTotal(cats, date):
    total = 0
    for cat in cats:
        report = DailyReport.objects.filter(category=cat, day=date)
        if report.count() == 0:
            break
        else:
            nums = report.num
            total += nums
    return total

def addDataToDailyReport(data,ayada):
    today_date = datetime.now().date()
    month = datetime.now().month
    categories = Category.objects.filter(ayada=ayada)
    del data['csrfmiddlewaretoken']
    del data['frequency_form']
    for cat in categories:
        sp_cat_input = "sp"+str(cat.id)
        sp_cat_num   = int(data[sp_cat_input])
        ad_cat_input = "ad"+str(cat.id)
        ad_cat_num   = int(data[ad_cat_input])
        papers       = data['papers']
        childPapers  = data['childPapers']
        nums         = sp_cat_num + ad_cat_num
        categorySlug = Category.objects.filter(pk=cat.id)[0].specific.name
        ayadaSlug    = ayada.name
        print(f"nums => {nums}")
        created = DailyReport.objects.update_or_create(
            category=cat, ayada=ayada, day=today_date,
            defaults={
                    "day": today_date, "category":cat, "ayada":ayada, "num":nums,
                    "advisory":ad_cat_num,"specialist":sp_cat_num, "papers":papers,
                    "childPapers": childPapers, "categorySlug":categorySlug, "ayadaSlug":ayadaSlug
                },
            )

    return "done"
