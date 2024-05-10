from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from .forms import TestForm, QuestionForm
from .models import Test, Question, CheckQuestion, CheckTest, TestCategory


class TestView(LoginRequiredMixin, View):
    def get(self, request, category_name):
        category = get_object_or_404(TestCategory, name=category_name)
        products = Test.objects.filter(category=category)
        q = request.GET.get('q', '')
        if q:
            products = products.filter(title__icontains=q)
        return render(request, "test/test_list.html", {'tests': products, "category": category})


@login_required(login_url='users:login')
def testlist(request):
    tests = Test.objects.all()
    q = request.GET.get('q', '')
    if q:
        tests = tests.filter(title__icontains=q)
    return render(request, 'test/test_list.html', {'tests': tests})


@login_required(login_url='login')
def ready_to_test(request, test_id):  # теске дайар
    test = get_object_or_404(Test, id=test_id)
    return render(request, 'test/ready_to_test.html', {'test': test})


@login_required(login_url='users:login')
def test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    attemps = CheckTest.objects.filter(student=request.user, test=test).count()
    if (timezone.now() >= test.start_date and timezone.now() <= test.end_date) and attemps < test.maximum_attemps:
        questions = Question.objects.filter(test=test)
        if request.method == 'POST':
            checktest = CheckTest.objects.create(student=request.user, test=test)
            for question in questions:
                given_answer = request.POST[str(question.id)]
                CheckQuestion.objects.create(checktest=checktest, question=question, given_answer=given_answer,
                                             true_answer=question.true_answer)
            checktest.save()
            return redirect('okuu:checktest', checktest.id)
        context = {'test': test, 'questions': questions}
        return render(request, 'test/test.html', context)
    else:
        return HttpResponse('test not Found!')


@login_required(login_url='users:login')
def checktest(request, checktest_id):
    checktest = get_object_or_404(CheckTest, id=checktest_id, student=request.user)
    return render(request, 'test/checktest.html', {'checktest': checktest})


#add question

@login_required(login_url='users:login')
def new_test(request):
    form = TestForm()
    if request.method == 'POST':
        form = TestForm(data=request.POST)
        if form.is_valid:
            test_id = form.save(request)
            return redirect('okuu:new_question', test_id)
    return render(request, 'test/new_test.html', {'form': form})


@login_required(login_url='users:login')
def new_question(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    if test.author == request.user:
        form = QuestionForm()
        if request.method == 'POST':
            form = QuestionForm(data=request.POST)
            if form.is_valid:
                form.save(test_id)
                if form.cleaned_data['болот_жетишту']:
                    return redirect('okuu:list_test')  #okuu:index
                return redirect('okuu:new_question', test.id)
        return render(request, 'test/new_question.html', {'form': form, 'test': test})
    else:
        return HttpResponse('something went wrong')
