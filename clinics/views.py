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
    return HttpResponse("حدثت مشكلة الرجاء التواصل مع المسؤول")

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
                addDataToDailyReport(formDict,user_clinic)
                return redirect('thanks')
            except Exception as e:
                print(f"exception {e}")
                # .get('1')
                # new_form = frequency_form.save()
                # new_form.ayada=user_clinic
                # frequency_form.save()
                return redirect('/clinics/thanks')
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
        # for testing only untill making the dashboard
        return redirect('/clinics/addFrequency')
        # return redirect('/clinics/erorr_page')

#=================== FUNCTIONS PART ============
def addDataToDailyReport(data,ayada):
    categories = Category.objects.filter(ayada=ayada)
    print(f"here 2== > ")
    del data['csrfmiddlewaretoken']
    del data['frequency_form']
    # print(f"here == > ")
    for cat in categories:
        cat_num = data[str(cat.id)]
        created = DailyReport.objects.update_or_create(
            category=cat, ayada=ayada, day=today_date,
            defaults={"day": today_date, "category":cat, "ayada":ayada, "num":cat_num},
        )
    return "done"
