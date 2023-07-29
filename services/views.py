from django.shortcuts import redirect, render
from django.urls import is_valid_path, reverse
from rest_framework.views import APIView
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework.response import Response
import json
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import JsonResponse


import random

@csrf_exempt
def getDesc(request):
    q = request.POST.get('q')
    # Construct a query to search for all Letter objects with a description containing the provided phrase
    query = Q(description__icontains=q)
    # Retrieve all matching Letter objects and return their descriptions as a list
    letters = Letter.objects.filter(query)
    descriptions = [letter.description for letter in letters]
    return JsonResponse({'descriptions': descriptions})


def rand_unique_number():
    rNum = random.randint(100,100000)
    rNum_count = Letter.objects.filter(serial=rNum).count()
    while rNum_count > 0:
        rNum = random.randint(100,100000)
    else:
        return rNum

def get_letter_serial(request, pk):
    letter = Letter.objects.get(pk=pk)
    return letter.serial

class priceBaseView(View):
    model = ServicePrice
    fields = '__all__'
    success_url = reverse_lazy('services:all')

class ServicePriceListView(priceBaseView, ListView):
    "list view"

class ServicePriceCreateView(priceBaseView, CreateView):
    """View to create a new film"""
class ServicePriceUpdateView(priceBaseView, UpdateView):
    """View to update a film"""

class ServicePriceDeleteView(priceBaseView, DeleteView):
    """View to delete a film"""

class EditLetter(UpdateView):
    model = Letter
    fields = '__all__'
    randNum = rand_unique_number()
    template_name_suffix = '_edit_form'
    def get_context_data(self,*args, **kwargs):
        context = super(EditLetter, self).get_context_data(*args,**kwargs)
        context['randNum'] = rand_unique_number()
        return context
    # def get_context_data(self, **kwargs):
    #     data = super(EditLetter, self).get_context_data(**kwargs)
    #     data['letterId']=self.object.id
    #     return data
    # letterId = get_context_data()
    def get_success_url(self, **kwargs):
        return reverse_lazy("services:PrintLetter", args=(self.object.id,))

    # success_url = reverse_lazy('services:PrintLetter/${data.letterId}')

class servicePricesCalc(APIView):
    def get(self, request):
        servicesArray = request.GET['services']
        total = 0
        total += [serv.publicPrice for serv in  servicesArray]
        data = {'total':total}
        return Response(data)

class cancelLetter(APIView):
    def get(self, request, pk):
        cancelReason = request.GET['cancelReason']
        Letter.objects.filter(pk=pk).update(is_deleted=True, cancelReason=cancelReason)
        msg = "تم الالغاء"
        data = {'msg': msg}
        return Response(data)

@login_required
def home(request):
    if request.user.groups.filter(name="services_member"):
        pass

    else:
        return redirect('/clinics/profile/')

    if request.method=='POST':
        naId=request.POST.get('naId')
        print(f"naId => ${naId}")
        if naId == 0:
            msg = "خطأ بالرقم القومى"
            return redirect(f'/clinics/erorr_page?msg={msg}')
        else:
            letters = Letter.objects.filter(naId=naId, is_deleted=False)
            msg = "لا يوجد تحويلات سابقة بهذا الرقم القومى" if letters.count() == 0 else 'تم الاستعلام'
            ctx = {'naId':naId,'letters':letters, 'msg':msg}
    elif request.method=='GET':
        ctx = {'naId':''}

    return render(request, 'services/main_page.html', ctx)

def PrintLetter(request, pk):
	letter = Letter.objects.get(id=pk)
	ctx = {'letter':letter}
	return render(request,'services/print_letter.html',ctx)


@login_required
def NewLetter(request):
    user = request.user
    if user.groups.filter(name="services_member"):
        pass
    else:
        return redirect('/clinics/profile')
    randNum =rand_unique_number()
    naId = 2351123
    if request.method=='POST':
        form = LetterForm(request.POST)
        if form.is_valid():
                myform=form.save()
                formId = myform.id
                return redirect(f'/services/PrintLetter/{formId}')
    else:
        naId = str(request.GET.get('naId', ''))
        print("naid => ",naId)
        form = LetterForm()
        userId = request.user.id
        userArea_id =  User.objects.get(pk=userId).employee.area.id
        print(userArea_id)
        if userArea_id != 7:
            # userAyada =  User.objects.get(pk=userId).employee.area.id
            # print(userAyada)
            form.fields["ayada"].queryset = Ayadat.objects.all()
        else:
            form.fields["ayada"].queryset = Ayadat.objects.filter(is_letter=True)
    ctx = {'form1':form, 'randNum':randNum, 'naId':naId}
    return render(request,'services/new_letter.html',ctx)

################ Functions Part

# def auth_user_custom(request):
#     print("here")
#     user = request.user
#     userGroup = ""
#     request.session.setdefault('group', False)
#     if user.groups.filter(name="admin_all"):
#         request.session['group'] = "admin_all"
#         userGroup = "admin_all"
#         return userGroup

#     elif user.groups.filter(name="clinic_admin"):
#         request.session['group'] = "clinic_admin"
#         userGroup = "clinic_admin"
#         return userGroup

#     elif user.groups.filter(name="clinic_supervisor"):
#         request.session['group'] = "clinic_supervisor"
#         userGroup = "clinic_supervisor"
#         return userGroup
#     elif user.groups.filter(name="clinic_member"):
#         request.session['group'] = "clinic_member"
#         userGroup = "clinic_member"
#         return userGroup
#     elif user.groups.filter(name="services_member"):
#         request.session['group'] = "services_member"
#         userGroup = "services_member"
#         return userGroup

#     else:
#         userGroup = "no group"
#         return userGroup
