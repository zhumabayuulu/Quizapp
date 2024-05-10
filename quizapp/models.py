
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import pre_save

from accounts.models import CustomUser


class TestCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Test(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(TestCategory,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    maximum_attemps = models.PositiveIntegerField()  # канча жолу арекет кылса болушун корсотучу болук
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=(timezone.now() + timezone.timedelta(days=10)))
    pass_percentage = models.PositiveIntegerField()  # жооптордун канча просенти откондуугун корсотот

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ('-id',)




class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.CharField(max_length=333)
    a = models.CharField(max_length=151)
    b = models.CharField(max_length=151)
    c = models.CharField(max_length=151)
    d = models.CharField(max_length=151)
    true_answer = models.CharField(max_length=151, help_text='E.x:a')

    def __str__(self):
        return str(self.question)


class CheckTest(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    finded_questions = models.PositiveIntegerField(default=0)
    user_passed = models.BooleanField(default=False)
    percentage = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "test of " + str(self.student.username)


class CheckQuestion(models.Model):
    checktest = models.ForeignKey(CheckTest, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    given_answer = models.CharField(max_length=1, help_text='E.x:a')
    true_answer = models.CharField(max_length=1, help_text='E.x:a')
    is_true = models.BooleanField(default=False)


@receiver(pre_save, sender=CheckQuestion)
def check_answer(sender, instance, *args, **kwargs):
    if instance.given_answer == instance.true_answer:
        instance.is_true = True


@receiver(pre_save, sender=CheckTest)
def check_test(sender, instance, *args, **kwargs):
    checktest = instance
    checktest.finded_questions = CheckQuestion.objects.filter(checktest=checktest, is_true=True).count()
    try:
        checktest.percentage = int(checktest.finded_questions) * 100 // CheckQuestion.objects.filter(
            checktest=checktest).count()
        if checktest.test.pass_percentage <= checktest.percentage:
            checktest.user_passed = True
    except:
        pass
