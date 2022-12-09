from django.shortcuts import redirect,render
from django.contrib.auth import login,logout,authenticate
from .forms import *
from .models import *
from django.http import HttpResponse
from django.views import View

# Create your views here.
class QuizView(View):
    def get(self, request, *args, **kwargs):
        quiz_slug = self.kwargs['quiz']
        answered_quiz = UserAnswer.objects.filter(question__quiz__slug=quiz_slug).count()>0
        print(answered_quiz)
        if answered_quiz:
            
            return render(request,'Quiz/answered.html')
        else:
            questions=QuesModel.objects.filter(quiz__slug=quiz_slug)
            context = {
                'questions':questions
            }
            return render(request,'Quiz/home.html',context)
    
    def post(self, request, *args, **kwargs):
        questions=QuesModel.objects.filter(quiz__slug=self.kwargs['quiz'])
        score=0
        wrong=0
        correct=0
        total=0
        answer_list = []
        for q in questions:
            total+=1
            form_answer = request.POST.get(q.question)
            print(form_answer)
            answer = UserAnswer(user=request.user, question=q, answer=form_answer)
            if q.ans ==  form_answer:
                score+=10
                correct+=1
            else:
                wrong+=1
            answer_list.append(answer)
        percent = score/(total*10) *100
        UserAnswer.objects.bulk_create(answer_list)
        context = {
            'score':score,
            'time': request.POST.get('timer'),
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total
        }
        return render(request,'Quiz/result.html',context)

