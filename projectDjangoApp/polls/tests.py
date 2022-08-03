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

def create_question(question_text, days):
    """
    Create a question with the given "question_text", and published the given
    numbre of days offset to now (negative for question published in the past
    positive for questio that have yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """if no question exist, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

    def test_future_question(self):
        """
        Question with a pub_date in the future aren't displayed on the index page.
        """
        create_question("Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])


    def test_past_question(self):
        """
        Question with a pub_date in the future are displayed on the index page.
        """
        question = create_question("Past question", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[question])