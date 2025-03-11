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
