import datetime
from urllib import response

from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse

from .models import Question

#Models y vistas
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """was_published_recently returns false questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="¿Quien es el mejor Course Director de Platzi?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """if no question exist, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])