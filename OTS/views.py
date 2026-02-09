import random
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.admin.views.decorators import staff_member_required
from OTS.models import Candidate, Question, Result


# ---------------- Welcome ----------------
def welcome(request):
    return render(request, 'welcome.html')


# ---------------- Registration Form ----------------
def candidateRegistrationForm(request):
    return render(request, 'registration_form.html')


# ---------------- Store Candidate ----------------
def candidateRegistration(request):
    if request.method == "POST":
        username = request.POST['username']

        if Candidate.objects.filter(username=username).exists():
            return render(request, 'registration.html', {'userStatus': 1})

        candidate = Candidate(
            username=username,
            password=make_password(request.POST['password']),
            name=request.POST['name']
        )
        candidate.save()
        return render(request, 'registration.html', {'userStatus': 2})

    return render(request, 'registration.html', {'userStatus': 3})


# ---------------- Login ----------------
def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        candidate = Candidate.objects.filter(username=username).first()

        if not candidate or not check_password(password, candidate.password):
            return render(request, 'login.html', {'loginError': 'Invalid credentials'})

        request.session['username'] = candidate.username
        request.session['name'] = candidate.name
        return redirect('OTS:home')

    return render(request, 'login.html')


# ---------------- Home ----------------
def candidateHome(request):
    if 'username' not in request.session:
        return redirect('OTS:login')

    return render(request, 'home.html')


# ---------------- Test Paper ----------------
def testPaper(request):
    if 'username' not in request.session:
        return redirect('OTS:login')

    n = int(request.GET.get('n', 5))
    questions = list(Question.objects.all())
    random.shuffle(questions)

    return render(request, 'test_paper.html', {
        'questions': questions[:n]
    })


# ---------------- Calculate Result ----------------
def calculateTestResult(request):
    if 'username' not in request.session:
        return redirect('OTS:login')

    total_attempt = total_right = total_wrong = 0

    for key in request.POST:
        if key.startswith('q_'):
            qid = int(key.split('_')[1])
            user_ans = request.POST[key]

            question = Question.objects.get(qid=qid)
            total_attempt += 1

            if user_ans == question.ans:
                total_right += 1
            else:
                total_wrong += 1

    points = max(0, (total_right - total_wrong) * 10 / total_attempt)

    candidate = Candidate.objects.get(username=request.session['username'])

    Result.objects.create(
        username=candidate,
        attempt=total_attempt,
        right=total_right,
        wrong=total_wrong,
        points=points
    )

    candidate.test_attempted += 1
    candidate.points = ((candidate.points * (candidate.test_attempted - 1)) + points) / candidate.test_attempted
    candidate.save()

    return redirect('OTS:result')


# ---------------- Result ----------------
def showTestResult(request):
    if 'username' not in request.session:
        return redirect('OTS:login')

    candidate = Candidate.objects.get(username=request.session['username'])
    result = Result.objects.filter(username=candidate).order_by('-resultid')[:1]

    return render(request, 'show_result.html', {'result': result})


# ---------------- History ----------------
def testResultHistory(request):
    if 'username' not in request.session:
        return redirect('OTS:login')

    candidate = Candidate.objects.get(username=request.session['username'])
    results = Result.objects.filter(username=candidate)

    return render(request, 'candidate_history.html', {'results': results})



# ---------------- Add_Question ----------------

@staff_member_required
def add_question(request):
    if request.method == 'POST':
        que = request.POST['que']
        a = request.POST['a']
        b = request.POST['b']
        c = request.POST['c']
        d = request.POST['d']
        ans = request.POST['ans']
        Question.objects.create(que=que, a=a, b=b, c=c, d=d, ans=ans)
        return render(request, 'question_form.html', {'success': True})
    return render(request, 'question_form.html')



# ---------------- Logout ----------------
def logoutView(request):
    request.session.flush()
    return redirect('OTS:login')

