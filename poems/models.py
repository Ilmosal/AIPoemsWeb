from random import Random

from django.db import models

# Create your models here.
class PoemSet(models.Model):
    language = models.CharField(max_length=2)
    max_questions = models.IntegerField()

    def __str__(self):
        return self.language

    def get_poems_before_location_with_seed(self, seed, loc):
        poems = list(self.poem_set.all())
        Random(seed).shuffle(poems)
        return poems[:loc+1]

class Poem(models.Model):
    poem_text = models.CharField(max_length=2048)
    author = models.CharField(max_length=128)
    poem_class = models.BooleanField()
    poem_lan = models.ForeignKey(PoemSet, on_delete=models.CASCADE)

    def __str__(self):
        return self.poem_text[:10]

class Questionnaire(models.Model):
    questionnaire_key = models.CharField(max_length=64)

    def __str__(self):
        return self.questionnaire_key

class AnswerSet(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    answerset_key = models.IntegerField()

class Answer(models.Model):
    answerset = models.ForeignKey(AnswerSet, on_delete=models.CASCADE)
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE)
    answer_class = models.BooleanField()

    def __str__(self):
        return "%r" % self.answer_class


