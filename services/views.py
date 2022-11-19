from django.shortcuts import redirect, render
from django.urls import is_valid_path, reverse
from rest_framework.views import APIView
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework.response import Response
import json

class cancelLetter(APIView):
    def get(self, request, pk):
        cancelReason = request.GET['cancelReason']
        Letter.objects.filter(pk=pk).update(is_deleted=True, cancelReason=cancelReason)
        msg = "تم الالغاء"
        data = {'msg': msg}
        return Response(data)

@login_required
def home(request):
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

import random
def rand_unique_number():
    rNum = random.randint(100,100000)
    rNum_count = Letter.objects.filter(serial=rNum).count()
    while rNum_count > 0:
        rNum = random.randint(100,100000)
    else:
        return rNum

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
                return redirect(reverse('PrintLetter',args=(formId,)))
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
            form.fields["ayada"].queryset = Ayadat.objects.filter(id=userArea_id)
        else:
            form.fields["ayada"].queryset = Ayadat.objects.filter(is_letter=True)
    ctx = {'form1':form, 'randNum':randNum, 'naId':naId}
    return render(request,'services/new_letter.html',ctx)