from django.shortcuts import redirect, render
from django.urls import is_valid_path, reverse
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required



def home(request):
	return render(request, 'index.html')

def PrintLetter(request, pk):
	letter = Letter.objects.get(id=pk)
	ctx = {'letter':letter}
	return render(request,'services/print_letter.html',ctx)

@login_required
def NewLetter(request):
    user = request.user
    if user.groups.filter(name="services_member"):
        return redirect('/services/new')
    else:
        pass
        # for testing only untill making the dashboard 
        # return redirect('/clinics/erorr_page')
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
    ctx = {'form1':form}
    return render(request,'services/new_letter.html',ctx)