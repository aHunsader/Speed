from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


from .models import Person
from .forms import MyUserCreationForm, MyAuthenticationForm

def index(request):
	return render(request, 'index.html')


def signup(request):
	if request.method == 'POST':
		form = MyUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			parent = form.cleaned_data.get('parent')
			phone = form.cleaned_data.get('phone')
			is_parent = parent == ""
			newPerson = Person(username=username, user=user, is_parent=is_parent, phone=phone)
			newPerson.save()
			if (not is_parent):
				newPerson.parent_name.add(get_object_or_404(Person, username=parent))
				return redirect('index')
			return redirect('children')
	else:
		form = MyUserCreationForm()

	return render(request, 'signup.html', context={'signup_form': form})

def login_view(request):
	if request.method == 'POST':
		login_form = MyAuthenticationForm(data=request.POST)
		if login_form.is_valid():
			username = login_form.cleaned_data.get('username')
			raw_password = login_form.cleaned_data.get('password')
			user = authenticate(username=username, password=raw_password)
			if(get_object_or_404(Person, username=username).is_parent):
				login(request, user)
				return redirect('children')
	else:
		login_form = MyAuthenticationForm()

	return render(request, 'login.html', context={'login_form': login_form})

def contact(request):
	return render(request, 'contact.html')

def aboutus(request):
	return render(request, 'about.html')

@login_required
def children_view(request):
	return render(request, 'children.html')

@login_required
def logout_view(request):
	logout(request)
	return redirect('index')

