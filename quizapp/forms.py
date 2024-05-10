from django import forms

from .models import Test, Question


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('title', 'category', 'maximum_attemps', 'start_date', "end_date", 'pass_percentage')
        labels = {
            "title": " тестин аты",
            'category': "болум",
            "maximum_attemps": "колдонучу канча жолу арекет кылса болот",
            'start_date': "качан башталсын",
            "end_date": "качан бутсун",
            'pass_percentage': "канча просенттен ашса тестен откон болуп эсептелсин",
        }

    def save(self, request, commit=True):
        test = self.instance
        test.author = request.user
        super().save(commit)
        return test.id


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question', 'a', 'b', 'c', 'd', 'true_answer')
        labels = {
            "question": "суроо",
            "true_answer": "туура жооп",
            "submit_and_exit": "g",
        }

    болот_жетишту = forms.BooleanField(required=False)

    def save(self, test_id, commit=True):
        question = self.instance
        question.test = Test.objects.get(id=test_id)
        super().save(commit)
        return question
