import graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation

from ..models import Question, Choice


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("id", "question_text", "pub_date", "choices")


class ChoiceType(DjangoObjectType):
    class Meta:
        model = Choice
        fields = ("id", "choice_text", "question", "votes")


class Query(graphene.ObjectType):
    fetch_questions = graphene.List(QuestionType)
    fetch_question = graphene.Field(QuestionType, id=graphene.ID(required=True))

    def resolve_fetch_questions(root, info):
        return Question.objects.all()

    def resolve_fetch_question(root, info, id):
        try:
            return Question.objects.get(pk=id)
        except Question.DoesNotExist:
            return None


class VoteMutation(graphene.Mutation):
    class Arguments:
        question_id = graphene.ID()
        choice_id = graphene.ID()

    question = graphene.Field(QuestionType)
    choice = graphene.Field(ChoiceType)

    @classmethod
    def mutate(cls, root, info, question_id, choice_id):
        question = Question.objects.get(pk=question_id)
        selected_choice = question.choices.get(pk=choice_id)
        selected_choice.votes = selected_choice.votes + 1
        selected_choice.save()

        return VoteMutation(question=question)


class Mutation(graphene.ObjectType):
    vote = VoteMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
