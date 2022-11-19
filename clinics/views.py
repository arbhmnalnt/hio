from logging import exception
from sre_parse import CATEGORIES
from unicodedata import category
from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect, render
from django.urls import is_valid_path, reverse
from django.views.generic.list import ListView


# from symbol import pass_stmt
from .forms import *
from .models import *
from services.models import *
from django.contrib.auth.decorators import login_required
from datetime import *
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login


today_date = datetime.now().date()
# print(f"today date => ", today_date)

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

        if user is not None:
            auth_login(request, user)
            return redirect('/clinics/profile')
            # message = f'Hello {user.username}! You have been logged in'
        else:
            message = 'Login failed!'
    return render(request, 'clinics/login.html', context={'message': message})

# الفترة المسائية عيادتان
def m_report(request):
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
    records = DailyReportHistory.objects.all()
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
def home(request):
    user_clinic = request.user.employee.area
    clinicName = user_clinic.name
    if clinicName == "الكل":
        clinicName = "العيادات"
    ctx = {"clinicName":clinicName}
    return render(request, './clinics/index.html' , ctx)

@login_required
def addFrequency(request):
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
            msg = "سبق لك تسجيل البيانات من قبل, الرجاء العلم ان تعديل البيانات يتم من خلال المسؤول فقط"
            return redirect(f'/clinics/erorr_page?msg={msg}')
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
            msg = "سبق لك تسجيل البيانات من قبل, الرجاء العلم ان تعديل البيانات يتم من خلال المسؤول فقط"
            return redirect(f'/clinics/erorr_page?msg={msg}')
        else:
            print(f"user {request.user.username} is pressing save to the record at {datetime.now()}")
            record = DailyReportHistory.objects.create(day=today_date, user=user)
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

        return redirect('/clinics/addFrequency')

    elif user.groups.filter(name="clinic_member"):
        request.session['group'] = "clinic_member"

        return redirect('/clinics/addFrequency')

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
        nums = sp_cat_num + ad_cat_num
        print(f"nums => {nums}")
        created = DailyReport.objects.update_or_create(
            category=cat, ayada=ayada, day=today_date,
            defaults={
                    "day": today_date, "category":cat, "ayada":ayada, "num":nums,
                    "advisory":ad_cat_num,"specialist":sp_cat_num, "papers":papers,
                    "childPapers": childPapers
                },
            )

    return "done"
