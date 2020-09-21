from django.db import models
from django.conf import settings


class Pool(models.Model):
    """Модель опросника"""

    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)

    start = models.DateTimeField(auto_now_add=True, editable=False)
    end = models.DateTimeField()

    def __str__(self):
        return self.title


class Question(models.Model):
    """Модель вопроса"""

    text = models.CharField(max_length=256)

    TEXT_TYPE = 1
    SINGLE_TYPE = 2
    MULTIPLE_TYPE = 3
    TYPES = (
        (TEXT_TYPE, "TEXT"),
        (SINGLE_TYPE, "SINGLE"),
        (MULTIPLE_TYPE, "MULTIPLE"),
    )
    type = models.IntegerField(choices=TYPES)

    pool = models.ForeignKey(Pool, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.text


class AnswerOption(models.Model):
    """Модель варианта ответа на вопрос"""

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answer_options'
        )
    text = models.CharField(max_length=256)

    def __str__(self):
        return self.text


class UserAnswer(models.Model):
    """Модель ответа пользователя на вопрос."""

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='users_answers'
        )
    answer_options = models.ManyToManyField(
        AnswerOption,
        blank=True
        )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
        )
    text = models.CharField(max_length=256, blank=True, null=True)
