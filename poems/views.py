import random

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .utils import decode_answer_code, encode_answer_code
from .models import PoemSet, Poem, Questionnaire, AnswerSet, Answer

# Create your views here.
def index(request):
    template = loader.get_template("poems/index.html")
    poem_langs = PoemSet.objects.all()
    context = {
        "poem_langs": poem_langs,
    }
    return HttpResponse(template.render(context, request))

def poem(request, answer_code):
    language, show_res, questionnaire, answerset, question, answers = decode_answer_code(answer_code)
    template = loader.get_template("poems/poem.html")
    poems = PoemSet.objects.get(language=language).get_poems_before_location_with_seed(answerset, question)
    poems.reverse()

    # Check which answers were correct
    ans = []
    ans_text = []
    accuracy = 0
    temp_ans = answers[-len(poems[1:]):]
    temp_ans.reverse()

    for p, a in zip(poems[1:], temp_ans):
        if p.poem_class == a:
            ans.append("green")
            ans_text.append("Correct")
            accuracy += 1
        else:
            ans.append("red")
            ans_text.append("Incorrect")
    if len(poems) == 1:
        acc_str = "-"
    else:
        acc_str = "{:3.2f}".format(100*(accuracy / (len(poems)-1)))

    context = {
        "cur_poem": poems[0],
        "prev_poems": zip(poems[1:], ans, ans_text),
        "answers": answers,
        "show_res": show_res,
        "title": answer_code,
        "accuracy": acc_str
    }

    return HttpResponse(template.render(context, request))

def results(request, answer_code):
    language, show_res, questionnaire, answerset, question, answers = decode_answer_code(answer_code)
    template = loader.get_template("poems/results.html")
    poems = PoemSet.objects.get(language=language).get_poems_before_location_with_seed(answerset, question-1)
    poems.reverse()

    # Check which answers were correct
    ans = []
    ans_text = []
    accuracy = 0
    temp_ans = answers[-len(poems):]
    temp_ans.reverse()

    for p, a in zip(poems, temp_ans):
        if p.poem_class == a:
            ans.append("green")
            ans_text.append("correct")
            accuracy += 1
        else:
            ans.append("red")
            ans_text.append("incorrect")
    acc_str = "{:3.2f}".format(100*(accuracy / len(poems)))

    context = {
        "poems": zip(poems, ans, ans_text),
        "answers": answers,
        "title": answer_code,
        "accuracy": acc_str,
    }

    return HttpResponse(template.render(context, request))

def start(request):
    try:
        language = request.POST.get("language", None)
        show_res = int("on" == request.POST.get("show_res", "off"))
        #questionnaire_key = request.POST.get("questionnaire_key", None)

        answer_set = random.randint(0, 10000000)

        code = encode_answer_code(language, show_res, 'none', answer_set, 0, [False])
    except Exception as e:
        return render(
                request,
                "poems/index.html",
                {
                    'error_msg': "Incorrect start information: {0}".format(e)
                }
            )
    else:
        return HttpResponseRedirect(reverse('poem', args=(code, )))

def next(request, answer_code):
    language, show_res, questionnaire, answerset, question, answers = decode_answer_code(answer_code)
    #update necessary things for next question

    answer_class = 1 if 'ai' in request.POST else 0
    answers.append(answer_class)
    question += 1

    new_answer_code = encode_answer_code(
            language,
            show_res,
            questionnaire, answerset, question, answers
    )

    if PoemSet.objects.get(language=language).max_questions <= question:
        question -= 1
        return HttpResponseRedirect(reverse('results', args=(new_answer_code, )))

    return HttpResponseRedirect(reverse('poem', args=(new_answer_code, )))

