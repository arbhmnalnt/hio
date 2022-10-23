from django.shortcuts import redirect, render
from django.urls import is_valid_path, reverse
from .forms import *


def home(request):
	return render(request, 'index.html')

def PrintLetter(request, pk):
	letter = Letter.objects.get(id=pk)
	ctx = {'letter':letter}
	return render(request,'services/print_letter.html',ctx)

def NewLetter(request):
	if request.method=='POST':
		form = LetterForm(request.POST)
		if form.is_valid():
			myform=form.save()
			return redirect(reverse('PrintLetter'))
	else:
		form = LetterForm()	

	ctx = {'form1':form}
	return render(request,'services/new_letter.html',ctx)