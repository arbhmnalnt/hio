from django.shortcuts import redirect, render
from django.urls import is_valid_path, reverse
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required


def home(request):
	return render(request, 'index.html')

def PrintLetter(request, pk):
	letter = Letter.objects.get(id=pk)
	ctx = {'letter':letter, 'today_date':today_date}
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
    if request.method=='POST':
        form = LetterForm(request.POST)
        if form.is_valid():
                myform=form.save()
                formId = myform.id
                return redirect(reverse('PrintLetter',args=(formId,)))
    else:
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
    ctx = {'form1':form, 'randNum':randNum}
    return render(request,'services/new_letter.html',ctx)