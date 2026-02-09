from django.urls import path
from OTS import views
from OTS.views import *
app_name='OTS'


urlpatterns = [
    path('', welcome),
    path('new-candidate/', candidateRegistrationForm, name='registrationForm'),
    path('store-candidate/', candidateRegistration, name='storeCandidate'),
    path('login/', loginView, name='login'),
    path('home/', candidateHome, name='home'),
    path('test-paper/', views.testPaper, name='testpaper'),
    path('calculate-result/', views.calculateTestResult, name='calculateResult'),
    path('test-history/', testResultHistory, name='testHistory'),
    path('result/', showTestResult, name='result'),
    path('admin-add-question', add_question, name='addQuestion'),
    path('logout/', logoutView, name='logout'),
]













# urlpatterns = [
#     path('',welcome),
#     path('new-candidate',candidateRegistrationForm,name='registrationForm'),
#     path('store-candidate',candidateRegistration,name='storeCandidate'),
#     path('login',loginView,name='login'),
#     path('home',candidateHome,name='home'),
#     path('test-paper',testPaper,name='testpaper'),
#     path('calculate-result',calculateTestResult,name='testpaper'),
#     path('test-history',testResultHistory,name="testHistory"),
#     path('result',showTestResult,name='result'),
#     path('logout',logoutView,name='logout')

# ]



