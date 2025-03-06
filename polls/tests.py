import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        thirty_days_from_now = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=thirty_days_from_now)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_question_older_than_one_day(self):
        yesterday = timezone.now() - datetime.timedelta(days=1, seconds=1)
        question_older_than_one_day = Question(pub_date=yesterday)
        self.assertIs(question_older_than_one_day.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        this_morning = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        question_published_this_morning = Question(pub_date=this_morning)
        self.assertIs(question_published_this_morning.was_published_recently(), True)


def create_question(question_text, days):
    published_date = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=published_date)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        past_question = create_question(
            question_text="This question is in the past", days=-1
        )
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["latest_question_list"], [past_question]
        )

    def test_future_question(self):
        future_question = create_question(
            question_text="I am a future question", days=1
        )
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_and_future_question(self):
        past_question = create_question(
            question_text="This question is in the past", days=-1
        )
        create_question(question_text="I am a future question", days=1)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["latest_question_list"], [past_question]
        )

    def test_multiple_past_questions(self):
        past_question = create_question(
            question_text="This question is in the past", days=-1
        )
        other_past_question = create_question(
            question_text="I am another question from the past", days=-2
        )
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [past_question, other_past_question],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(
            question_text="This question is in the past", days=1
        )
        response = self.client.get(reverse("polls:detail", args=[future_question.id]))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(
            question_text="This question is in the past", days=-1
        )
        response = self.client.get(reverse("polls:detail", args=[past_question.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This question is in the past")
