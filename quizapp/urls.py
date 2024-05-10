from django.urls import path
from .views import *


app_name = 'okuu'
urlpatterns = [
    # test url
    path('list/',testlist,name='list_test'),
    path('<int:test_id>/ready_to_test',ready_to_test,name="ready_to_test"),
    path('<int:test_id>/test',test,name="test"),
    path('<int:checktest_id>/checktest',checktest,name='checktest'),
    path('new_test',new_test,name='new_test'),
    path('<int:test_id>/new_question',new_question,name='new_question'),
    # category url
    path('test/<str:category_name>/category', TestView.as_view(), name='category'),
    # end category

]