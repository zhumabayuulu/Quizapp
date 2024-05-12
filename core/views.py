from django.shortcuts import render, redirect


def home(request):
    if request.user.is_authenticated:
        return redirect('test:list_test', )
    else:
        return render(request, 'home.html',)


