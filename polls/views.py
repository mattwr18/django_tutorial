from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question
from .schema.schema import schema


def index(request):
    result = schema.execute(
        """
            query {
                fetchQuestions {
                    id
                    questionText
                }
            }
            """
    )
    latest_question_list = result.data["fetchQuestions"]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    result = schema.execute(
        """
        query fetchQuestion($id: ID!) {
            fetchQuestion(id: $id) {
                id
                questionText
                choices {
                    id
                    choiceText
                }
            }
        }
        """,
        variables={"id": question_id},
    )
    return render(
        request, "polls/detail.html", {"question": result.data["fetchQuestion"]}
    )


def results(request, question_id):
    result = schema.execute(
        """
        query fetchQuestion($id: ID!) {
            fetchQuestion(id: $id) {
                id
                questionText
                choices {
                    choiceText
                    votes
                }
            }
        }
        """,
        variables={"id": question_id},
    )
    return render(
        request, "polls/results.html", {"question": result.data["fetchQuestion"]}
    )


def vote(request, question_id):
    result = schema.execute(
        """
        mutation Vote($questionId: ID!, $choiceId: ID!) {
            vote(questionId: $questionId, choiceId: $choiceId) {
                question {
                    id
                    questionText
                    choices {
                        id
                        choiceText
                        votes
                    }
                }
            }
        }
        """,
        variables={"questionId": question_id, "choiceId": request.POST["choice"]},
    )
    return HttpResponseRedirect(
        reverse("polls:results", args=(result.data["vote"]["question"]["id"],))
    )
