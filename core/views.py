from django.shortcuts import render, redirect


def home(request):
    if request.user.is_authenticated:
        return redirect('okuu:list_test', )
    else:
        return render(request, 'home.html',)


