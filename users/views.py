from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, CustomUserCreationForm


@login_required
def profile(request):
    if request.method == 'POST':
        form=CustomUserChangeForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            form = CustomUserChangeForm(instance=request.user)
        return render(request,'users/profile.html',{'form':form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            form = CustomUserCreationForm()
        return render(request,'users/register.html',{'form':form})




