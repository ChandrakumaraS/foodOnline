from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from django.contrib import messages

def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, "Your account is created successfully")
            # print(messages)
            return redirect('registerUser')
        else:
            print('Invalid Form')
            print(form.errors)
    else:
        form = UserForm()
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)



