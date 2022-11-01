from logging import exception
from sre_parse import CATEGORIES
from unicodedata import category
from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect, render
from django.urls import is_valid_path, reverse

# from symbol import pass_stmt
from .forms import *
from .models import *
from services.models import *
from django.contrib.auth.decorators import login_required
from datetime import *
from django.contrib.auth.models import Group

today_date = datetime.now().date()
# print(f"today date => ", today_date)



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
    if clinicName == "الكل":
        clinicName = "العيادات"
        Categories_obj = Category.objects.filter(ayada=Ayadat.objects.get(pk=1))
    else :
        Categories_obj = Category.objects.filter(ayada=user_clinic)
    if request.method == 'POST':
        if 'frequency_form' in request.POST:
            print(f"request.POST\n ==> {request.POST}")
            frequency_form = request.POST
            try:
                print(f"here 1== > ")
                formDict = frequency_form.dict()
                status = addDataToDailyReport(formDict,user_clinic)
                print(f"statue => {status}")
                return redirect('/clinics/thanks')
            except Exception as e:
                print(f"exception {e}")
                msg = e
                return redirect(f'/clinics/erorr_page?msg={msg}')
    else:
        pass
    categories = Categories_obj
    ctx = {"clinicName":clinicName, "categories":categories}

    return render(request, './clinics/add_frequency.html', ctx)


def profile(request):
    user = request.user
    if user.groups.filter(name="clinic_member"):
        return redirect('/clinics/addFrequency')
    elif user.groups.filter(name="services_member"):
        return redirect('/services/new')
    else:
        msg="user has no group"
        return redirect(f'/clinics/erorr_page?={msg}')
        # return redirect('/clinics/erorr_page')

#=================== FUNCTIONS PART ============
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
    #     specialist = models.IntegerField(verbose_name="حالات الاخصائى", default=0)
    # advisory   = models.IntegerField(verbose_name="حالات الاستشارى", default=0)
    # num        = models.IntegerField(verbose_name="الإجمالى", default=0)
    # papers      = models.IntegerField(verbose_name="إجمالى الروشتات", default=0 )
    # childPapers      = models.IntegerField(verbose_name="إجمالى روشتات الاطفال", default=0)
    return "done"
